import logging
import uuid
from strands import Agent
from strands.session.s3_session_manager import S3SessionManager

logging.getLogger("strands").setLevel(logging.DEBUG)
logging.basicConfig(
    format="%(levelname)s | %(name)s | %(message)s",
    handlers=[logging.StreamHandler()],
)

# Create a session manager that stores data in S3
session_manager = S3SessionManager(
    session_id=f"{uuid.uuid4()}",
    bucket="crearerd-demo",
    prefix="production/",  # Optional key prefix
    region_name="us-east-1"  # Optional AWS region (if boto_session not provided)
)

# Create an agent with the session manager
agent = Agent(session_manager=session_manager)

# Use the agent normally - state and messages will be persisted to S3
agent("Tell me about AWS S3")