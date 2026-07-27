from typing import Any

from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from fastapi.middleware.cors import CORSMiddleware

from graph.workflow import graph

app = FastAPI(
    title="GrantGuard API",
    version="1.0.0",
)

# Allow your frontend to call the API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Restrict this in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def health():
    return {"status": "running"}


@app.post("/evaluate")
def evaluate(application: dict[str, Any]):

    state = {
        "application": application,
        "plan": None,
        "tool_results": {},
        "review": None,
        "security_review": None,
        "worker_result": "",
        "final_decision": "",
    }

    result = graph.invoke(state)

    return jsonable_encoder(result)