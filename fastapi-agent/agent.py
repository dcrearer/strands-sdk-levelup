from fastapi import FastAPI, Request, Response
from pydantic import BaseModel
from typing import Dict, Any
from datetime import datetime
from strands import Agent

app = FastAPI(title="Agent Server", version="1.0.0")

# Initialize agent with Bedrock model
strands_agent = Agent(
    model="anthropic.claude-3-haiku-20240307-v1:0",
    system_prompt="You are a helpful AI assistant. Respond to user queries in a clear and concise manner."
)

"""
1. Request Validation: Pydantic's BaseModel automatically validates incoming JSON requests. It ensures that the prompt field is present and is a string type. If someone sends invalid
data, FastAPI will automatically return a 422 error with details about what's wrong.

2. Type Safety: It provides type hints that help with IDE autocompletion and static type checking. Your function parameter request: InvokeRequest tells FastAPI exactly what structure
to expect.

3. Automatic Documentation: FastAPI uses this model to generate OpenAPI/Swagger documentation automatically. When you visit /docs, it will show the expected request format with the
prompt field.

4. JSON Parsing: FastAPI automatically parses the incoming JSON request body into this structured object, so you can access request.prompt instead of manually parsing raw JSON.

5. API Contract: It defines a clear contract for your API endpoint - clients know they need to send a JSON object with a prompt string field.

Without this class, you'd have to:
• Manually parse the request body
• Handle validation errors yourself
• Write more code to extract the prompt value
• Lose automatic API documentation

The class essentially transforms this endpoint from accepting raw, unstructured data to accepting a well-defined, validated data structure that matches your /invocations endpoint
requirements.
"""
class InvokeRequest(BaseModel):
    prompt: str

@app.post("/invocations")
async def invoke_agent(request: InvokeRequest) -> Response:
    user_message = request.prompt
    
    # Validate that the message is not empty
    if not user_message or not user_message.strip():
        return Response(
            content="Error: Empty prompt provided",
            status_code=400
        )
    
    try:
        result = strands_agent(user_message)
        
        # Extract text content from the result
        if hasattr(result, 'message') and isinstance(result.message, dict):
            content = result.message.get('content', [])
            if content and isinstance(content, list) and len(content) > 0:
                response_text = content[0].get('text', str(result.message))
            else:
                response_text = str(result.message)
        else:
            response_text = str(result)
            
        response = Response(
            content=response_text,
            status_code=200,
            media_type="text/plain"
        )
    except Exception as e:
        return Response(
            content=f"Error: {str(e)}",
            status_code=500,
            media_type="text/plain"
        )
    
    return response

@app.get("/ping")
def ping():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)