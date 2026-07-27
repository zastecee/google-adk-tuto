import os
import uuid

from fastapi import FastAPI
from fastapi.responses import JSONResponse
from google.adk.runners import InMemoryRunner
from google.genai import types
from pydantic import BaseModel

from agent import root_agent

app = FastAPI(title="Google ADK Demo")
runner = InMemoryRunner(agent=root_agent, app_name="adk-demo")
runner.auto_create_session = True


class ChatRequest(BaseModel):
    message: str
    user_id: str = "default-user"


async def run_agent(message: str, user_id: str) -> str:
    if not os.getenv("GOOGLE_API_KEY"):
        return "Agent is unavailable because GOOGLE_API_KEY is not configured."

    session_id = f"{user_id}-{uuid.uuid4().hex[:8]}"
    await runner.session_service.create_session(
        app_name=runner.app_name,
        user_id=user_id,
        session_id=session_id,
    )

    new_message = types.Content(
        role="user",
        parts=[types.Part.from_text(text=message)],
    )

    reply_text = ""
    async for event in runner.run_async(
        user_id=user_id,
        session_id=session_id,
        new_message=new_message,
    ):
        if event.content:
            for part in event.content.parts:
                if getattr(part, "text", None):
                    reply_text = part.text.strip()

    return reply_text or "I couldn't generate a response."


@app.get("/")
def read_root() -> JSONResponse:
    return JSONResponse(
        {
            "status": "ok",
            "agent": root_agent.name,
            "message": "ADK agent is ready to serve requests.",
        }
    )


@app.get("/health")
def healthcheck() -> JSONResponse:
    return JSONResponse({"status": "healthy"})


@app.post("/chat")
async def chat(request: ChatRequest) -> JSONResponse:
    reply = await run_agent(request.message, request.user_id)
    return JSONResponse(
        {
            "reply": reply,
            "agent": root_agent.name,
        }
    )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=int(os.getenv("PORT", "8080")))
