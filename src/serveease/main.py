from fastapi import FastAPI ,  HTTPException
from fastapi.middleware.cors import CORSMiddleware
from serveease.models.models import Address ,  User, ServiceProvider, Recommendation , RecommendationResponse
from typing import List, cast
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from datetime import datetime, UTC
from fastapi.responses import StreamingResponse
import os
# Import OpenAI Agents SDK
from openai.types.responses import ResponseTextDeltaEvent
from agents import Agent, Runner, function_tool, AsyncOpenAI, OpenAIChatCompletionsModel, RunConfig, ModelProvider
from serveease.prompts.prompts import Recommendation_Agent_instructions

# Load the environment variables from the .env file
load_dotenv()

gemini_api_key = os.getenv("GEMINI_API_KEY")

# Check if the API key is present; if not, raise an error
if not gemini_api_key:
    raise ValueError(
        "GEMINI_API_KEY is not set. Please ensure it is defined in your .env file.")

# Reference: https://ai.google.dev/gemini-api/docs/openai
external_client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=external_client
)

config = RunConfig(
    model=model,
    model_provider=cast(ModelProvider, external_client), # satisfy type checker
    tracing_disabled=True
)

app = FastAPI(
    title="ServeEase API",
    description="API for service provider recommendations",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# Define the agent
agent = Agent(
    name = "RecommendationAgent",
    instructions=Recommendation_Agent_instructions,
    model = model,
    output_type=RecommendationResponse,
)

@app.post("/recommend/", response_model=RecommendationResponse)
async def recommend(user: User, service_providers: List[ServiceProvider])-> RecommendationResponse:
    # Call the agent's run method with the user and service providers
    response = await Runner.run(user=user, service_providers=service_providers)
    return response