# prompt.py
from utils.common import set_up_cache, generate_model, generate_memory, save_memory, generate_conversation_summary
from utils.constant import FEEDBACKS, EVENT_CODE
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

# Set up cache and necessary components
set_up_cache(db=1)

llm = generate_model(temperature=0)
llm_chain = LLMChain(
    prompt=PromptTemplate(
        template="write sentiment only (positive, neutral, negative) {feedback}",
        input_variables=["feedback"]
    ),
    llm=llm
)

memory = generate_memory()

# Process feedback data
for text in FEEDBACKS[EVENT_CODE]:
    answer = llm_chain.run(text)
    print(f"Text: {text}, Sentiment: {answer}")
    save_memory(memory, text)

# Generate and print conversation summary
summary = generate_conversation_summary(EVENT_CODE, memory)
print("\nSummary:")
print(summary)
