from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task
from knowledge_extraction_flow.tools import FileMdConversionTool, FileUploadTool
import os

# If you want to run a snippet of code before or after the crew starts,
# you can use the @before_kickoff and @after_kickoff decorators
# https://docs.crewai.com/concepts/crews#example-crew-class-with-decorators


@CrewBase
class DocConversionCrew:
    """Doc Conversion Crew"""

    def __init__(self):
        super().__init__()
        # 设置默认 LLM
        self.llm = LLM(model="gemini/gemini-2.0-flash-lite")
        
        # 确保输出目录存在
        output_dir = os.path.join(os.path.dirname(__file__), "output")
        os.makedirs(output_dir, exist_ok=True)
     
  
    # Learn more about YAML configuration files here:
    # Agents: https://docs.crewai.com/concepts/agents#yaml-configuration-recommended
    # Tasks: https://docs.crewai.com/concepts/tasks#yaml-configuration-recommended
    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    # If you would lik to add tools to your crew, you can learn more about it here:
    # https://docs.crewai.com/concepts/agents#agent-tools
    @agent
    def google_file_processor(self) -> Agent:
        return Agent(
            config=self.agents_config["google_file_processor"],
            tools=[FileUploadTool() ],
            llm=self.llm
        )
        
    @agent
    def md_formatter(self) -> Agent:
        return Agent(
            config=self.agents_config["md_formatter"],
            tools=[FileMdConversionTool()],
            llm=self.llm
        )

    # To learn more about structured task outputs,
    # task dependencies, and task callbacks, check out the documentation:
    # https://docs.crewai.com/concepts/tasks#overview-of-a-task
    @task
    def upload_file_to_google_task(self) -> Task:
        return Task(
            config=self.tasks_config["upload_file_to_google_task"],
            output_file=os.path.join(os.path.dirname(__file__), "output", "01_upload_file_to_google_report.json")
        )
        
    @task
    def format_document_to_markdown_task(self) -> Task:
        return Task(
            config=self.tasks_config["format_document_to_markdown_task"],
            output_file=os.path.join(os.path.dirname(__file__), "output", "02_format_document_to_markdown_report.json")
        )

    @crew
    def crew(self) -> Crew:
        """Creates the Research Crew"""
        # To learn how to add knowledge sources to your crew, check out the documentation:
        # https://docs.crewai.com/concepts/knowledge#what-is-knowledge

        return Crew(
            agents=self.agents,  # Automatically created by the @agent decorator
            tasks=self.tasks,  # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
        )
