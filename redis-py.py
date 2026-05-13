import redis

client = redis.from_url("redis://localhost:6379/0", decode_responses=True)

"""
client = redis.Redis(
    host="localhost",
    port=6379,
    db=0,
    decode_responses=True
)
"""

try:
    print("Conectado:", client.ping())
    client.set("saludo", "hola redis")
    print("Valor:", client.get("saludo"))
except Exception as e:
    print("Error:", e)



