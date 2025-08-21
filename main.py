from fastapi import FastAPI
from fastapi.responses import PlainTextResponse

app = FastAPI(
    title="API Ping",
    version="1.0.0",
    description='Une API qui répond "pong" à un ping.'
)

@app.get("/ping", response_class=PlainTextResponse, summary="Vérifie la disponibilité du service")
def ping():
    return "pong"
