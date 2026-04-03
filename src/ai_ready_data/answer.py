import os

from google.adk.models.lite_llm import LiteLlm
from google.adk.agents import LlmAgent

model = LiteLlm(
    model="huggingface/mistralai/Mistral-7B-Instruct-v0.3",
    api_key=os.environ["HF_TOKEN"]
)

agent = LlmAgent(model=model, name="qa_agent", instruction="Answer questions about energy data.")


def get_answer(query: str) -> str:
    # ADK requires async runner setup — adds boilerplate
    return 'yoyowassup'