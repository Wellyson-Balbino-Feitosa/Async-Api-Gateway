from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from gateway.auth import verify_token
from gateway.rate_limit import rate_limit
from gateway.router import forward_request
import starlette.status as status

app = FastAPI()


@app.middleware("http")
async def gateway_logic_middleware(request: Request, call_next):

    # Rate limit - Redis
    if not await rate_limit(request):
        # Retorna erro 429 Too Many Requests se o rate limit for excedido
        return Response(
            content=orjson.dumps({"detail": "Rate limit excedido."}),
            status_code=429,
            media_type="application/json",
        )

    # Auth - JWT
    auth = request.headers.get("authorization")
    if not auth or not auth.startswith("Bearer "):
        # Retorna erro 401 Unauthorized se o token estiver ausente ou inválido
        return Response(
            content=orjson.dumps({"detail": "Token ausente ou inválido"}),
            status_code=401,
            media_type="application/json",
        )

    try:
        verify_token(auth[7:])
    except Exception:
        # Retorna erro 401 Unauthorized se o token estiver inválido
        return Response(
            content=orjson.dumps({"detail": "Token inválido"}),
            status_code=401,
            media_type="application/json",
        )

    # Retorna a requisição para o router
    return await call_next(request)


@app.api_route("/{service}/{path:.*}", methods=["GET", "POST", "PUT", "DELETE"])
async def gateway(service: str, path: str, request: Request):
    """
    Rota principal do gateway que encaminha as requisições para os microsserviços.
    A segurança e o rate limit agora são tratados via Middleware para maior performance.
    """
    return await forward_request(service, path, request)
