from fastapi import FastAPI, Request, Depends
from gateway.auth import verify_token
from gateway.rate_limit import rate_limit
from gateway.router import forward_request

app = FastAPI()

@app.api_route("/{service}/{path:.*}", methods=["GET", "POST", "PUT", "DELETE"])
async def gateway(service: str, path: str, request: Request, user= Depends(verify_token), _=Depends(rate_limit)):
    return await forward_request(service, path, request)