import logging
from strands import Agent
from strands.session.file_session_manager import FileSessionManager

logging.getLogger("strands").setLevel(logging.DEBUG)
logging.basicConfig(
    format="%(levelname)s | %(name)s | %(message)s",
    handlers=[logging.StreamHandler()],
)

session_manager = FileSessionManager(
    session_id="user-124-session",
    storage_dir="./sessions"   
)
agent = Agent(session_manager=session_manager)

agent("What is strands sdk session management?")