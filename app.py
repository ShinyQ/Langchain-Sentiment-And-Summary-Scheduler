from utils.common import (generate_model, set_up_cache, generate_conversation_summary, generate_memory,
                          save_memory, set_up_redis, save_text_to_redis)

from flask import Flask, request, jsonify
from utils.constant import EVENT_CODE
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from celery_config import BROKER_URL
from celery import Celery

import json

# Create a Flask application
app = Flask(__name__)

# Configure Celery
celery = Celery('app', broker=BROKER_URL)
celery.config_from_object('celery_config')

# Configure Redis
redis_client = set_up_redis()

@celery.task
def process_sentiment_analysis(feedback):
    """
    Perform sentiment analysis on the given feedback and save the result to Redis.

    Args:
        feedback (str): The feedback text to be analyzed.
    """
    set_up_cache()
    llm = generate_model(temperature=0)
    llm_chain = LLMChain(
        prompt=PromptTemplate(
            template="write sentiment only (positive, neutral, negative) {feedback}",
            input_variables=["feedback"]
        ),
        llm=llm
    )

    # Process feedback data
    answer = llm_chain.run(feedback)
    save_text_to_redis(text=feedback, sentiment=answer)


@celery.task
def process_sentiment_summary():
    """
    Generate sentiment summary and store it in Redis.
    """
    set_up_cache()
    retrieved_data = redis_client.get(f"sentiment-classification:{EVENT_CODE}")
    retrieved_data = json.loads(retrieved_data)

    if retrieved_data is not None:
        memory = generate_memory()

        for text in retrieved_data:
            save_memory(memory, text.get('text'))

        # Generate and print conversation summary
        summary = generate_conversation_summary(EVENT_CODE, memory)
        redis_client.set(f"sentiment-classification-summary:{EVENT_CODE}", summary)


@app.route("/sentiment/predict", methods=['POST'])
def get_sentiment():
    """
    Endpoint to receive feedback, save it to Redis, and trigger sentiment analysis asynchronously.

    Returns:
        JSON: Success or error message.
    """
    feedback = request.get_json().get('feedback')

    if feedback:
        save_text_to_redis(text=feedback)
        process_sentiment_analysis.apply_async(args=[feedback], countdown=0)
        return jsonify({"message": "Success inserting feedback"}), 200
    else:
        return jsonify({"error": "Invalid input"}), 400


@app.route("/sentiment/summary", methods=['GET'])
def get_summary():
    """
    Endpoint to trigger asynchronous generation of sentiment summary.

    Returns:
        JSON: Success message.
    """
    process_sentiment_summary.apply_async(args=[], countdown=0)
    return jsonify({"message": "Generating your sentiment summary in a few moments"}), 200


@app.route("/", methods=['GET'])
def index():
    """
    Default endpoint to check if the server is up.

    Returns:
        JSON: Server status message.
    """
    return jsonify({"message": "Server is up"}), 200


if __name__ == '__main__':
    app.run(debug=True)
