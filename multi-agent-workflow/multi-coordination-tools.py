from strands import Agent
from strands_tools import agent_graph, swarm, workflow, calculator, file_read, file_write, python_repl, http_request

# Master coordinator that can use all coordination patterns
master_coordinator = Agent(
    model="us.anthropic.claude-3-7-sonnet-20250219-v1:0",
    tools=[agent_graph, swarm, workflow, calculator, file_read, file_write, python_repl, http_request],
    system_prompt="""
    You are a master coordinator with access to multiple coordination patterns:

    - agent_graph: For complex routing and decision-making between agents
    - swarm: For parallel processing and dynamic agent selection
    - workflow: For sequential, staged processing

    Choose the appropriate coordination pattern based on the task:
    - Use agent_graph for complex decision trees and conditional routing
    - Use swarm for tasks that can be parallelized or need dynamic agent selection
    - Use workflow for sequential, stage-based processing
    - Combine patterns when needed for complex scenarios
    """
)

# Example of choosing coordination pattern based on task complexity
adaptive_task = """
I have a complex project that involves:
1. Market research (can be done in parallel)
2. Data analysis (sequential processing required)
3. Report generation (needs conditional routing based on analysis results)

Please choose and coordinate the appropriate agent coordination pattern(s) for this task.
"""

result = master_coordinator(adaptive_task)