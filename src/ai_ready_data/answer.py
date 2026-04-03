import os

from google.adk.agents import LlmAgent
from google.adk.models.lite_llm import LiteLlm
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

from .retriever import Retriever

model = LiteLlm(
    model="huggingface/Qwen/Qwen2.5-72B-Instruct",
    api_key=os.environ["HF_TOKEN"]
)

agent = LlmAgent(model=model, name="qa_agent", instruction="Answer questions.")

session_service = InMemorySessionService()
runner = Runner(agent=agent, app_name="ai_ready_data", session_service=session_service)


async def get_answer(query: str, retriever: Retriever) -> str:
    context = retriever(query)
    text = f"Context:\n{context}\n\nQuestion: {query}" if context else query
    session = await session_service.create_session(app_name="ai_ready_data", user_id="user")
    message = types.Content(role="user", parts=[types.Part(text=text)])

    async for event in runner.run_async(user_id="user", session_id=session.id, new_message=message):
        if event.is_final_response():
            return event.content.parts[0].text

    return (
        "Apologies; there has been an error in the Data Answering Factory. "
        "Our Oompa-loompas are working on fixing it."
    )
