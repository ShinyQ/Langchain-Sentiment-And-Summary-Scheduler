import json
import redis
from redis import Redis
from langchain.cache import RedisCache
from langchain.llms.openai import OpenAI
from langchain.globals import set_llm_cache
from langchain.chat_models import ChatOpenAI
from langchain.chains import ConversationChain
from langchain.memory import ConversationSummaryBufferMemory
from utils.constant import OPENAI_API_KEY, MODEL_MAIN, MODEL_MEMORY, SUMMARY_MESSAGE, EVENT_CODE


def set_up_redis():
    return redis.StrictRedis(db=1, host='localhost', port=6379, decode_responses=True)


def set_up_cache(db=0):
    """
    Set up the cache with a Redis backend.

    Args:
        db (int): The Redis database index.
    """
    set_llm_cache(RedisCache(redis_=Redis(db=db), ttl=3600))


def save_text_to_redis(text, sentiment=""):
    """
    Save text and sentiment to Redis.

    Args:
        text (str): The text to be saved.
        sentiment (str): The sentiment associated with the text.
    """
    data = {"text": text, "sentiment": sentiment}

    # Get existing data from Redis
    redis_client = set_up_redis()
    existing_data_str = redis_client.get(f"sentiment-classification:{EVENT_CODE}")
    existing_data = json.loads(existing_data_str) if existing_data_str else []

    # Check if the key (text) already exists
    existing_text_keys = [item["text"] for item in existing_data]
    if text in existing_text_keys:
        # Update the existing data with the new sentiment
        for item in existing_data:
            if item["text"] == text:
                item["sentiment"] = sentiment
    else:
        # Append the new data to the existing data
        existing_data.append(data)

    # Store the updated data in Redis
    redis_client.set(f"sentiment-classification:{EVENT_CODE}", json.dumps(existing_data))


def generate_model(temperature=0):
    """
    Generate a chat model for main conversations.

    Args:
        temperature (float): The sampling temperature.

    Returns:
        ChatOpenAI: The generated chat model.
    """
    return ChatOpenAI(
        model=MODEL_MAIN,
        temperature=temperature,
        openai_api_key=OPENAI_API_KEY,
        max_tokens=100,
        cache=True
    )


def generate_memory():
    """
    Generate a memory model for storing conversation summaries.

    Returns:
        ConversationSummaryBufferMemory: The generated memory model.
    """
    return ConversationSummaryBufferMemory(
        llm=OpenAI(
            model=MODEL_MEMORY,
            temperature=0,
            openai_api_key=OPENAI_API_KEY,
            max_tokens=100
        )
    )


def generate_conversation_summary(event_code, memory):
    """
    Generate a conversation summary using the main model and memory.

    Args:
        event_code (str): The event code for customizing the model.
        memory (ConversationSummaryBufferMemory): The memory model.

    Returns:
        str: The generated conversation summary.
    """
    conversation_summary = ConversationChain(
        llm=ChatOpenAI(
            model=MODEL_MAIN,
            temperature=1.2,
            openai_api_key=OPENAI_API_KEY,
            tiktoken_model_name=event_code
        ),
        memory=memory,
    )
    return conversation_summary.predict(input=SUMMARY_MESSAGE)


def save_memory(memory, question):
    """
    Save a question and an empty response in the memory.

    Args:
        memory (ConversationSummaryBufferMemory): The memory model.
        question (str): The input question to be saved.
    """
    memory.save_context(
        {"input": question},
        {"output": ""}
    )


def load_data_from_redis(redis_conn, redis_key):
    """
    Load JSON data from Redis using a given connection and key.

    Args:
        redis_conn (Redis): The Redis connection.
        redis_key (str): The key to retrieve data from Redis.

    Returns:
        dict or None: The loaded JSON data or None if not found.
    """
    retrieved_json_data = redis_conn.get(redis_key)

    if retrieved_json_data is not None:
        return json.loads(retrieved_json_data)

    return None
