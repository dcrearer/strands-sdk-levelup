from strands import Agent
from strands_tools import workflow, file_read, calculator, file_write, python_repl

# Define workflow stages with specialized agents
intake_agent = Agent(
    model="us.anthropic.claude-3-7-sonnet-20250219-v1:0",
    tools=[file_read],
    system_prompt="""
    You are the intake agent - the first stage in our workflow.
    Your job is to:
    1. Understand the incoming request
    2. Gather initial data and requirements
    3. Prepare information for the next stage
    4. Clearly document what needs to be passed forward
    """
)

processing_agent = Agent(
    model="us.anthropic.claude-3-7-sonnet-20250219-v1:0",
    tools=[calculator, python_repl],
    system_prompt="""
    You are the processing agent - the middle stage in our workflow.
    Your job is to:
    1. Take processed requirements from the intake stage
    2. Perform the core analysis or computation work
    3. Generate intermediate results
    4. Prepare findings for the final stage
    """
)

delivery_agent = Agent(
    model="us.anthropic.claude-3-7-sonnet-20250219-v1:0",
    tools=[file_write],
    system_prompt="""
    You are the delivery agent - the final stage in our workflow.
    Your job is to:
    1. Take analysis results from the processing stage
    2. Format and package the final deliverables
    3. Create output files and documentation
    4. Ensure quality and completeness of final output
    """
)

# Workflow orchestrator
workflow_orchestrator = Agent(
    model="us.anthropic.claude-3-7-sonnet-20250219-v1:0",
    tools=[workflow],
    system_prompt="""
    You orchestrate a sequential workflow with three stages:

    Stage 1 - Intake: Requirements gathering and initial data collection
    Stage 2 - Processing: Core analysis and computation
    Stage 3 - Delivery: Final output generation and packaging

    Use the workflow tool to:
    1. Ensure proper sequential execution
    2. Manage state between stages
    3. Handle handoffs between agents
    4. Monitor workflow progress and completion
    """
)

# Example workflow execution
workflow_task = """
Please execute a workflow to analyze customer feedback data:

1. Intake stage: Read customer feedback files and understand requirements
2. Processing stage: Analyze sentiment and extract key insights
3. Delivery stage: Create a summary report with recommendations

The workflow should process files in the 'feedback' directory and output a final report.
"""

result = workflow_orchestrator(workflow_task)