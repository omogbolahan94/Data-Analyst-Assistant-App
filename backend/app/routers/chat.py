from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter, UploadFile, File
from .. import agent_workflow
from .. import data_store.DATA_STORE as DATA_STORE

from .. import schemas


router = APIRouter(
    prefix="/chat",
    tags=["Chat"]
)

UPLOAD_DIR = "uploaded_files"
os.makedirs(UPLOAD_DIR, exist_ok=True)


# @router.get("/chat", response_model=ChatResponse)
# def post(request: schemas.ChatRequest):
#     """
#     Handle incoming chat messages from frontend.
#     """
#     reply = agent_workflow.chat(request.message)
#     return ChatResponse(reply=reply)

@router.post("/chat", response_model=schemas.ChatResponse)
def chat(request: schemas.ChatRequest):
    """
    Accepts JSON: { "message": "...", "file_id": "<optional-file-id>" }
    Invokes the LangGraph state graph, passing the messages and the file_id
    so tools (e.g. data_summary) can fetch the uploaded dataframe.
    """
    if getattr(request, "file_id", None):
        if request.file_id not in DATA_STORE:
            raise HTTPException(status_code=404, detail="Dataset (file_id) not found. Please upload first.")

    # Build the message list in the same format you used in notebooks
    messages = [HumanMessage(content=request.message)]

    # Build the state for graph.invoke - include file_id so tools can access it
    # You can add other state keys here if your State TypedDict requires them.
    state = {
        "messages": messages,
        "file_id": request.file_id  # may be None
    }

    try:
        result = graph.invoke(state)
    except Exception as e:
        # convert graph errors into HTTP 500 with message
        raise HTTPException(status_code=500, detail=f"Agent execution error: {e}")

    # Extract assistant reply from returned messages (same pattern you used in Jupyter)
    try:
        assistant_message = result["messages"][-1]
        reply = assistant_message.content
    except Exception:
        # fallback: stringify result so client always gets something
        reply = str(result)

    return schemas.ChatResponse(reply=reply)