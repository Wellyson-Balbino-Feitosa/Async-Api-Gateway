import httpx
from fastapi import Request, HTTPException, Response

SERVICES= {
     "users": "http://localhost:8001",
     "orders": "http://localhost:8002",
     "payments": "http://localhost:8003"
}

client = httpx.AsyncClient(
    limits=httpx.Limits(
        max_connections=500,
        max_keepalive_connections=200
    ),
    timeout=5.0
)

async def forward_request(service: str, path: str, request: Request):
    if service not in SERVICES:
        raise HTTPException(status_code=404, detail="Serviço não encontrado")

    url= f"{SERVICES[service]}/{path}"

    response= await client.request(
        method=request.method,
        url=url,
        headers=request.headers.raw,
        content=await request.body(),
        timeout=httpx.Timeout(5.0, connect=1.0)
    )

    return Response(content=response.content, status_code=response.status_code, headers=dict(response.headers))