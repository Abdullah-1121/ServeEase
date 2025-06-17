from fastapi import FastAPI ,  HTTPException
from fastapi.middleware.cors import CORSMiddleware
from serveease.models.models import RecommendationResponse , ServiceProviders , userInput , chatResponse
from typing import List, cast
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from datetime import datetime, UTC
from fastapi.responses import StreamingResponse
from agents import(Agent, AgentOutputSchema, Runner, function_tool, AsyncOpenAI, OpenAIChatCompletionsModel, RunConfig,
ModelProvider, set_trace_processors , RunContextWrapper)
from langsmith.wrappers import OpenAIAgentsTracingProcessor
import os
# Import OpenAI Agents SDK
from openai.types.responses import ResponseTextDeltaEvent
from serveease.agent import recommendation_agent
from serveease.agent2 import Customer_Triage_Agent , UserContext
from agents import Runner, set_trace_processors
import uvicorn


#  Load the environment variables from the .env file
load_dotenv()
gemini_api_key = os.getenv("GEMINI_API_KEY")
# Check if the API key is present; if not, raise an error
if not gemini_api_key:
    raise ValueError(
        "GEMINI_API_KEY is not set. Please ensure it is defined in your .env file.")
# Reference: https://ai.google.dev/gemini-api/docs/openai

set_trace_processors([OpenAIAgentsTracingProcessor()])
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
    model_provider=external_client,  # satisfy type checker
    workflow_name="ServeEase",
)


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
    response = await Runner.run(
        starting_agent=recommendation_agent,
        input="Recommend me the best service providers",
        context=service_providers,
        run_config=config
    )
    return response


@app.post("/chat/" )
async def Chat(input : userInput)-> str:
    user_context = UserContext(username=input.username)
    response = await Runner.run(
        starting_agent=Customer_Triage_Agent,
        input=input.userInput,
        context=user_context,
        run_config=config
    )
    return response.final_output

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000 )