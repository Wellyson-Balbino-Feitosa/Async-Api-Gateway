import httpx
from fastapi import Request, HTTPException

SERVICES= {
     "users": "http://localhost:8001",
     "orders": "http://localhost:8002",
     "payments": "http://localhost:8003"
}

client= httpx.AsyncClient() 

async def forward_request(service: str, path: str, request: Request):
    if service not in SERVICES:
        raise HTTPException(status_code=404, detail="Serviço não encontrado")

    url= f"{SERVICES[service]}/{path}"

    response= await client.request(
        method=request.method,
        url=url,
        headers=request.headers.raw,
        content=await request.body()
    )

    return response.json()