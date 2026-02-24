import aioredis
from fastapi import Request, HTTPException

r = aioredis.from_url("redis://localhost:6379", encoding="utf-8", decode_responses=True)

RATE_LIMIT = 100 # 100 requisições
WINDOW= 60 # 60 segundos

async def rate_limit(request: Request):
    client_ip = request.client.host
    key = f"rate_limit:{client_ip}"
    
    current = await r.get(key)

    if current and int(current) >= RATE_LIMIT:
        raise HTTPException(status_code=429, detail="Rate limit excedido.")

    pipe = r.pipeline()
    pipe.incr(key)
    pipe.expire(key, WINDOW)
    await pipe.execute()

    return True