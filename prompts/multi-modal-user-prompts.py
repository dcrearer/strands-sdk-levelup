import logging
from strands import Agent

logging.getLogger("strands").setLevel(logging.DEBUG)
logging.basicConfig(
    format="%(levelname)s | %(name)s | %(message)s",
    handlers=[logging.StreamHandler()],
)

agent = Agent()

with open("image.png", "rb") as fp:
    image_bytes = fp.read()

response = agent([
    {"text": "What is in this image?"},
    {"image": {
        "format": "png",
        "source": {
            "bytes": image_bytes
        }
    }}
])