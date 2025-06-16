from fastapi import FastAPI ,  HTTPException
from fastapi.middleware.cors import CORSMiddleware
from serveease.models.models import RecommendationResponse , ServiceProviders
from typing import List, cast
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from datetime import datetime, UTC
from fastapi.responses import StreamingResponse
import os
# Import OpenAI Agents SDK
from openai.types.responses import ResponseTextDeltaEvent
from serveease.agent import run_agent
from agents import Runner
import uvicorn

# Load the environment variables from the .env file
load_dotenv()


app = FastAPI(
    title="ServeEase API",
    description="API for service provider recommendations",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# Define the agent


@app.post("/recommend/", response_model=RecommendationResponse)
async def recommend(service_providers: ServiceProviders)-> RecommendationResponse:
    response = await run_agent(service_providers)
    return response


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)