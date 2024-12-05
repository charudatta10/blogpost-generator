from langgraph import LangGraph
from langgraph.agents import Agent, Supervisor

# Define agent classes
class ContentWriterAgent(Agent):
    def create_content(self):
        return "This month, we've seen significant advancements in AI technology..."

class ProofreaderAgent(Agent):
    def proofread(self, content):
        return content + " (Proofread and edited)"

class FinalizerAgent(Agent):
    def finalize(self, content):
        return content + "\n\nThank you for reading our monthly newsletter!"

# Initialize agents
content_writer = ContentWriterAgent(name="ContentWriter")
proofreader = ProofreaderAgent(name="Proofreader")
finalizer = FinalizerAgent(name="Finalizer")

# Initialize supervisor
supervisor = Supervisor()

# Add agents to supervisor
supervisor.add_agents([content_writer, proofreader, finalizer])

# Define tasks
content_task = content_writer.create_task(content_writer.create_content)
proofread_task = proofreader.create_task(proofreader.proofread)
finalize_task = finalizer.create_task(finalizer.finalize)

# Assign tasks to agents and set dependencies
supervisor.assign_task(content_task, content_writer)
supervisor.assign_task(proofread_task, proofreader)
supervisor.assign_task(finalize_task, finalizer)

# Set task dependencies
proofread_task.set_dependency(content_task)
finalize_task.set_dependency(proofread_task)

# Run the supervisor
supervisor.run()

# Collect the final content
final_content = supervisor.get_task_result(finalize_task)
print(final_content)
