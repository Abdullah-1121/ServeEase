from uuid import uuid4
from agents import(Agent, AgentOutputSchema, Runner, function_tool, AsyncOpenAI, OpenAIChatCompletionsModel, RunConfig,
ModelProvider, set_trace_processors , RunContextWrapper)
from langsmith.wrappers import OpenAIAgentsTracingProcessor
import os
from dotenv import load_dotenv
import asyncio
from serveease.models.models import Review, ServiceProvider, ServiceProviders , RecommendationResponse





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

def dynamic_instructions(context : RunContextWrapper[ServiceProviders] , agent : Agent[ServiceProviders]) -> str:
    return f'''
# System Prompt: Recommendation Agent

You are a highly skilled **Recommendation Agent**, operating as part of a multi-agent AI system powered by OpenAI Agents SDK. Your primary objective is to analyze customer reviews and generate an accurate, reliable, and well-structured recommendation list of household service providers for a mobile application.

---

## Responsibilities

### 1️⃣ Analyze Reviews
- Carefully assess the provided customer reviews for each service provider.
- Focus on key aspects such as:
  - Customer satisfaction
  - Service quality
  - Timeliness
  - Professionalism
  - Pricing fairness
  - Issue resolution
  - Repeat customer likelihood

### 2️⃣ Scoring
- Assign a **score** to each service provider based on your analysis of the reviews.
- Use a score scale of **1 to 10**, where:
  - `10` = Outstanding, flawless service.
  - `1` = Extremely poor service.
- Normalize the scores across providers to ensure fairness.

### 3️⃣ Ranking
- Sort the service providers in **descending order of score**.
- The highest-scoring provider should be listed first.

---
#Here is the list of SERVICE PROVIDERS :
{context.context.service_providers}

 '''

# Define the agent
recommendation_agent = Agent(
    name = "RecommendationAgent",
    instructions = dynamic_instructions,
    model = model,
    output_type=RecommendationResponse
)

async def test_agent(input_text: str):
    # Create a ServiceProviders instance with some dummy data

    service_providers = ServiceProviders(
    service_providers=[
        ServiceProvider(
            provider_id=str(uuid4()),
            name="Plumber 1",
            rating=4.5,
            customer_reviews=[
                Review(text="Excellent plumbing service! Fixed leak quickly.", date="2023-01-01"),
                Review(text="Very professional and thorough.", date="2023-01-02"),
            ],
            service_type="Plumber",
        ),
        ServiceProvider(
            provider_id=str(uuid4()),
            name="Plumber 2",
            rating=3.8,
            customer_reviews=[
                Review(text="Decent service, good communication.", date="2023-01-01"),
                Review(text="Satisfactory work, could improve speed.", date="2023-01-02"),
            ],
            service_type="Plumber",
        ),
        ServiceProvider(
            provider_id=str(uuid4()),
            name="Plumber 3",
            rating = 2.9,
            customer_reviews=[
                Review(text="Average service, took longer than expected.", date="2023-01-01"),
                Review(text="Not the best, but got the job done.", date="2023-01-02"),
            ],
            service_type="Plumber",
        ),
        ServiceProvider(
            provider_id=str(uuid4()),
            name="Plumber 4",
            rating = 4,
            customer_reviews=[
                Review(text="Great to work with Plumber 4!", date="2023-01-01"),
                Review(text="Skilled and efficient plumber.", date="2023-01-02"),
            ],
            service_type="Plumber",
        ),
        ServiceProvider(
            provider_id=str(uuid4()),
            name="Plumber 5",
            rating = 4.8,
            customer_reviews=[
                Review(text="Arrived promptly, excellent job.", date="2023-01-01"),
                Review(text="Top-notch plumbing service!", date="2023-01-02"),
            ],
            service_type="Plumber",
        ),
    ]
)
    recommendation_agent.output_type = AgentOutputSchema(RecommendationResponse, strict_json_schema=False)
    response = await Runner.run(
        
        starting_agent=recommendation_agent,
        input=input_text,
        context=service_providers,
        )
    print(response.final_output)
# Run Agent Method 
async def run_agent(Providers : ServiceProviders)-> RecommendationResponse:
    recommendation_agent.output_type = AgentOutputSchema(RecommendationResponse, strict_json_schema=False)
    response = await Runner.run(
        
        starting_agent=recommendation_agent,
        input="Recommend me the best service providers",
        context=Providers,
        )
    print(response.final_output)
    return response.final_output
asyncio.run(test_agent("Recommend me the best service providers"))