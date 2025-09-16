from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel
from agents.run import RunConfig
import chainlit as cl
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()
gemini_api_key = os.getenv("GEMINI_API_KEY")

# Configure Gemini client through OpenAI Agents SDK
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
    model_provider=external_client,
    tracing_disabled=True
)

# Create the agent
agent: Agent = Agent(
    name="Assistant",
    instructions="You are a helpful assistant. Answer clearly and politely."
)


# ------------------ Chainlit Integration ------------------ #
@cl.on_chat_start
async def start():
    await cl.Message(content="Hello 👋 I’m your Gemini-powered AI assistant. How can I help you today?").send()


@cl.on_message
async def main(message: cl.Message):
    # Run the agent with the user input
    result = await Runner.run(agent, message.content, run_config=config)

    # Send the agent’s response back to the UI
    if result and result.final_output:
        await cl.Message(content=result.final_output).send()
    else:
        await cl.Message(content="⚠️ Sorry, I couldn’t generate a response.").send()
