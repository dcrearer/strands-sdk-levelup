import asyncio
from pydantic import BaseModel
from strands import Agent

class PersonInfo(BaseModel):
    name: str
    age: int
    occupation: str

async def structured_output():
    agent = Agent()
    return await agent.structured_output_async(
        PersonInfo,
        "John Smith is a 30-year-old software engineer"
    )

result = asyncio.run(structured_output())

print(f"Name: {result.name}")
print(f"Age: {result.age}")
print(f"Job: {result.occupation}")