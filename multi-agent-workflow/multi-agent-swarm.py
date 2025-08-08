from strands import Agent
from strands_tools import swarm, calculator, file_read, http_request, shell, python_repl

# Create specialized agents for the swarm
research_agent = Agent(
    model="us.anthropic.claude-3-7-sonnet-20250219-v1:0",
    tools=[http_request, file_read],
    system_prompt="You are a research specialist. You excel at gathering information from various sources."
)

computation_agent = Agent(
    model="us.anthropic.claude-3-7-sonnet-20250219-v1:0",
    tools=[calculator, python_repl],
    system_prompt="You are a computation specialist. You excel at mathematical analysis and data processing."
)

system_agent = Agent(
    model="us.anthropic.claude-3-7-sonnet-20250219-v1:0",
    tools=[shell, file_read],
    system_prompt="You are a system specialist. You excel at system administration and file operations."
)

# Swarm coordinator
swarm_coordinator = Agent(
    model="us.anthropic.claude-3-7-sonnet-20250219-v1:0",
    tools=[swarm],
    system_prompt="""
    You coordinate a swarm of specialized agents:

    Agent Capabilities:
    - research_agent: Web research, API calls, information gathering
    - computation_agent: Mathematical calculations, data analysis
    - system_agent: File operations, system commands, infrastructure tasks

    Use the swarm tool to:
    1. Distribute tasks across appropriate agents
    2. Coordinate parallel execution when possible
    3. Aggregate results from multiple agents
    4. Handle complex multi-step workflows
    """
)

# Example: Complex task requiring multiple agents
complex_task = """
I need to:
1. Research current market trends for electric vehicles
2. Analyze the financial data in the 'quarterly_reports' directory
3. Check system resources and available disk space
4. Generate a comprehensive market analysis report

Please coordinate the swarm to handle these tasks efficiently.
"""

result = swarm_coordinator(complex_task)