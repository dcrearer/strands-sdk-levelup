import logging
from strands import Agent
from strands.agent.conversation_manager import SlidingWindowConversationManager

logging.getLogger("strands").setLevel(logging.DEBUG)
logging.basicConfig(
    format="%(levelname)s | %(name)s | %(message)s",
    handlers=[logging.StreamHandler()],
)

conversation_manager = SlidingWindowConversationManager(window_size=10)

agent = Agent(
    conversation_manager=conversation_manager,
)

agent("What is a sliding window?")