import redis
from fastapi import Request, HTTPException

r = redis.Redis(host="localhost", port=6379, db=0)

RATE_LIMIT = 100 # 100 requisições
WINDOW= 60 # 60 segundos

async def rate_limit(request: Request):
    client_ip = request.client.host
    key = f"rate_limit:{client_ip}"
    
    current = r.get(key)

    if current and int(current) >= RATE_LIMIT:
        raise HTTPException(status_code=429, detail="Rate limit excedido.")

    pipe = r.pipeline()
    pipe.incr(key)
    pipe.expire(key, WINDOW)
    pipe.execute()

    return True