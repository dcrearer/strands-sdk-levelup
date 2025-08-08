from strands import Agent, tool
from strands_tools import calculator, file_read, file_write, python_repl, shell
import json
import logging

# Configure logging for debugging
logging.getLogger("strands").setLevel(logging.DEBUG)
logging.basicConfig(format="%(levelname)s | %(name)s | %(message)s")

# Shared state for agents to communicate
workflow_state = {
    "tasks": [],
    "results": {},
    "current_step": 0
}

@tool
def update_workflow_state(key: str, value: str) -> str:
    """Update the shared workflow state"""
    workflow_state[key] = value
    return f"Updated {key} in workflow state"

@tool
def get_workflow_state(key: str = None) -> str:
    """Get current workflow state or specific key"""
    if key:
        return str(workflow_state.get(key, "Key not found"))
    return json.dumps(workflow_state, indent=2)

@tool
def handoff_to_agent(agent_name: str, task: str) -> str:
    """Hand off a task to another agent"""
    workflow_state["tasks"].append({
        "agent": agent_name,
        "task": task,
        "status": "pending"
    })
    return f"Task handed off to {agent_name}: {task}"

# Agent 1: Research Agent - Gathers information
research_agent = Agent(
    model="us.anthropic.claude-3-7-sonnet-20250219-v1:0",
    tools=[file_read, shell, update_workflow_state, get_workflow_state, handoff_to_agent],
    system_prompt="""
    You are a Research Agent specialized in gathering and analyzing information.
    Your role is to:
    1. Research topics and gather data
    2. Read files and analyze content
    3. Use shell commands to explore the system
    4. Update the workflow state with your findings
    5. Hand off tasks to other agents when appropriate

    Always update the workflow state with your findings and coordinate with other agents.
    """
)

# Agent 2: Analysis Agent - Processes and analyzes data
analysis_agent = Agent(
    model="us.anthropic.claude-3-7-sonnet-20250219-v1:0",
    tools=[calculator, python_repl, update_workflow_state, get_workflow_state, handoff_to_agent],
    system_prompt="""
    You are an Analysis Agent specialized in data processing and analysis.
    Your role is to:
    1. Analyze data provided by other agents
    2. Perform calculations and statistical analysis
    3. Run Python code for complex analysis
    4. Generate insights and recommendations
    5. Update workflow state with analysis results

    Always check the workflow state for data to analyze and coordinate with other agents.
    """
)

# Agent 3: Output Agent - Creates final deliverables
output_agent = Agent(
    model="us.anthropic.claude-3-7-sonnet-20250219-v1:0",
    tools=[file_write, update_workflow_state, get_workflow_state],
    system_prompt="""
    You are an Output Agent specialized in creating final deliverables.
    Your role is to:
    1. Take analysis results and create reports
    2. Write files with final outputs
    3. Format results for presentation
    4. Ensure all deliverables are complete

    Always check the workflow state for results to compile into final outputs.
    """
)

# Workflow Orchestrator
class MultiAgentWorkflow:
    def __init__(self):
        self.agents = {
            "research": research_agent,
            "analysis": analysis_agent,
            "output": output_agent
        }

    def execute_workflow(self, initial_task: str):
        """Execute the multi-agent workflow"""
        print(f"🚀 Starting multi-agent workflow: {initial_task}")

        # Step 1: Research phase
        print("\n📊 Phase 1: Research")
        research_result = self.agents["research"](
            f"Research the following topic and gather relevant information: {initial_task}. "
            f"Update the workflow state with your findings and hand off analysis tasks to the analysis agent."
        )

        # Step 2: Analysis phase
        print("\n🔍 Phase 2: Analysis")
        analysis_result = self.agents["analysis"](
            "Check the workflow state for research data. Analyze the data and generate insights. "
            "Update the workflow state with your analysis results and hand off report creation to the output agent."
        )

        # Step 3: Output phase
        print("\n📝 Phase 3: Output Generation")
        output_result = self.agents["output"](
            "Check the workflow state for analysis results. Create a comprehensive report "
            "and save it to a file. Include all research findings and analysis insights."
        )

        print("\n✅ Workflow completed!")
        return {
            "research": research_result,
            "analysis": analysis_result,
            "output": output_result,
            "final_state": workflow_state
        }

# Example usage
if __name__ == "__main__":
    workflow = MultiAgentWorkflow()

    # Execute a sample workflow
    results = workflow.execute_workflow(
        "Analyze the current directory structure and provide insights about the project organization"
    )

    print("\n🎯 Final Results:")
    print(f"Workflow State: {json.dumps(workflow_state, indent=2)}")

