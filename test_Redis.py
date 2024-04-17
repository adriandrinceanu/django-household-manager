import redis

# Assuming Redis is on the same network (redis:6379)
try:
  r = redis.Redis(host='redis', port=6379)
  print("Connected to Redis!")
  r.set('test_key', 'test_value')
  print("Set key 'test_key' with value 'test_value'")
  value = r.get('test_key')
  print(f"Retrieved value: {value}")
except redis.exceptions.ConnectionError as e:
  print(f"Error connecting to Redis: {e}")