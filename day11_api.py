from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()
app = FastAPI(title="GenBot API")
client = Groq(api_key=os.getenv("GROQ_API_KEY"))
MODEL = "llama-3.3-70b-versatile"

# In-memory chat history
chat_histories = {}

# ── REQUEST/RESPONSE MODELS ────────────────────────
class ChatRequest(BaseModel):
    session_id: str
    message: str
    system_prompt: str = "You are a helpful Gen AI assistant."

class ChatResponse(BaseModel):
    session_id: str
    response: str
    message_count: int

# ── ROUTES ─────────────────────────────────────────
@app.get("/")
def root():
    return {"status": "GenBot API is running!", "version": "1.0"}

@app.get("/health")
def health():
    return {"status": "healthy"}

@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    """
    TASK 1: Get or create history for session_id
            from chat_histories dict

    TASK 2: Append user message to history
            {"role": "user", "content": request.message}

    TASK 3: Call Groq API with system prompt + history

    TASK 4: Append assistant response to history

    TASK 5: Return ChatResponse with
            session_id, response text, message count
    """
    # YOUR CODE HERE
    if request.session_id not in chat_histories:
        chat_histories[request.session_id] = []

    # Append user message to history
    chat_histories[request.session_id].append({"role": "user", "content": request.message})

    # Call Groq API with system prompt + history
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": request.system_prompt}
        ] + chat_histories[request.session_id]
    )

    # Append assistant response to history
    chat_histories[request.session_id].append({"role": "assistant", "content": response.choices[0].message.content})

    # Return ChatResponse with session_id, response text, message count
    return ChatResponse(
        session_id=request.session_id,
        response=response.choices[0].message.content,
        message_count=len(chat_histories[request.session_id])
    )

@app.delete("/chat/{session_id}")
def clear_chat(session_id: str):
    """
    TASK 6: Delete session from chat_histories
            Return {"message": "Session cleared"}
            Raise HTTPException 404 if not found
    """
    # YOUR CODE HERE
    if session_id not in chat_histories:
        raise HTTPException(status_code=404, detail="Session not found")
    del chat_histories[session_id]
    return {"message": "Session cleared"}

@app.get("/sessions")
def list_sessions():
    """
    TASK 7: Return all active session IDs
            and their message counts
    """
    # YOUR CODE HERE
    return {
        "sessions": [
            {"session_id": session_id, "message_count": len(history)}
            for session_id, history in chat_histories.items()
        ]
    }