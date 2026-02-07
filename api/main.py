import os
from fastapi import FastAPI
from pydantic import BaseModel
from dotenv import load_dotenv

from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor

from agent.agent import llm_call
from utils.observability import setup_tracing

load_dotenv()

# Setup tracing FIRST
setup_tracing()

app = FastAPI(
    title="Leave Policy Agent API",
    version="1.0.0",
)

# Auto-instrument FastAPI
FastAPIInstrumentor.instrument_app(app)


class ChatRequest(BaseModel):
    message: str


@app.post("/chat")
def chat(request: ChatRequest):
    response = llm_call(request.message)

    return {
        "user_message": request.message,
        "agent_response": response,
    }


@app.get("/health")
def health():
    return {"status": "healthy"}


@app.get("/ready")
def ready():
    return {"status": "ready"}
