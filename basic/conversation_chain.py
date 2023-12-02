# conversation_chain.py
import redis
from utils.common import set_up_cache, generate_model, generate_memory, save_memory, load_data_from_redis, generate_conversation_summary
from utils.constant import EVENT_CODE

# Set up cache and necessary components
set_up_cache()

# Create a connection to the Redis server
redis_host, redis_port, redis_db = 'localhost', 6379, 0
redis_conn = redis.StrictRedis(host=redis_host, port=redis_port, db=redis_db)

# Specify the key from which you want to retrieve data
redis_key = f"sentiment-classification:{EVENT_CODE}"

# Get the JSON data from Redis
retrieved_data = load_data_from_redis(redis_conn, redis_key)

if retrieved_data is not None:
    memory = generate_memory()

    for text in retrieved_data:
        save_memory(memory, text.get('text'))

    # Generate and print conversation summary
    summary = generate_conversation_summary(EVENT_CODE, memory)

    print("\nSummary:")
    print(summary)
else:
    print(f"No data found for key: {redis_key}")
