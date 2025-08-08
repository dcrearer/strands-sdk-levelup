from strands import Agent, tool
from strands_tools import agent_graph, calculator, file_read, file_write, python_repl

# Define specialized agents
data_agent = Agent(
    model="us.anthropic.claude-3-7-sonnet-20250219-v1:0",
    tools=[file_read, python_repl],
    system_prompt="You specialize in data collection and preprocessing."
)

analysis_agent = Agent(
    model="us.anthropic.claude-3-7-sonnet-20250219-v1:0",
    tools=[calculator, python_repl],
    system_prompt="You specialize in data analysis and statistical computations."
)

report_agent = Agent(
    model="us.anthropic.claude-3-7-sonnet-20250219-v1:0",
    tools=[file_write],
    system_prompt="You specialize in creating comprehensive reports and documentation."
)

# Coordinator agent that manages the graph
coordinator = Agent(
    model="us.anthropic.claude-3-7-sonnet-20250219-v1:0",
    tools=[agent_graph],
    system_prompt="""
    You are a coordinator that manages a graph of specialized agents.

    Available agents:
    - data_agent: Handles data collection and preprocessing
    - analysis_agent: Performs analysis and calculations
    - report_agent: Creates final reports

    Use the agent_graph tool to route tasks to appropriate agents and manage their interactions.
    """
)

# Example usage
task = """
I need to analyze sales data from a CSV file and create a comprehensive report.
Please coordinate between the data agent, analysis agent, and report agent to:
1. Load and preprocess the data
2. Perform statistical analysis
3. Generate a final report
"""

result = coordinator(task)