import logging 
import asyncio
from strands import Agent
from strands_tools import calculator

logging.getLogger("strands").setLevel(logging.DEBUG)
logging.basicConfig(
    format="%(levelname)s | %(name)s | %(message)s",
    handlers=[logging.StreamHandler()],
)

agent = Agent(
    tools=[calculator],
    callback_handler=None
)

async def process_streaming_response():
    prompt = "What is 25 * 48 and expain calculation"
    
    agent_stream = agent.stream_async(prompt)
    
    async for event in agent_stream:
        if "data" in event:
            print(event["data"], end="", flush=True)
        elif "current_tool_use" in event and event["current_tool_use"].get("name"):
            print(f"\n[Tool use delta for: {event['current_tool_use']['name']}]")
            

asyncio.run(process_streaming_response())
