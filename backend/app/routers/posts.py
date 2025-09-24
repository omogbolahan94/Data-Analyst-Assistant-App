from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter


from ..agent_workflow.build_graph import graph
from ..agent_workflow.chat import chat

from .. import schemas


router = APIRouter(
    prefix="/chat",
    tags=["Chat"]
)


@router.get("/", response_model=ChatResponse)
def post(request: schemas.ChatRequest):
    """
    Handle incoming chat messages from frontend.
    """
    reply = run_workflow(request.message)
    return ChatResponse(reply=reply)


print("Hi post router")