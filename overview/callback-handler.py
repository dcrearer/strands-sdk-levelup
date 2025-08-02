import logging
from strands import Agent
from strands_tools import shell

logging.getLogger("strands").setLevel(logging.DEBUG)
logging.basicConfig(
    format="%(levelname)s | %(name)s | %(message)s",
    handlers=[logging.StreamHandler()],
)

tool_use_ids = []

def callback_handler(**kwargs):
    if "data" in kwargs:
        logging.info(kwargs["data"], end="")
    elif "current_tool_use" in kwargs:
        tool = kwargs["current_tool_use"]
        if tool["toolUseId"] not in tool_use_ids:
            logging.info(f"\n[Using tool: {tool.get('name')}]")
            tool_use_ids.append(tool["toolUseId"])

agent = Agent(
    tools=[shell],
    callback_handler=callback_handler
)

result = agent("What operating system am I using?")

print(result.message)
