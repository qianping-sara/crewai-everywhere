from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import SerperDevTool
import os
from dotenv import load_dotenv
from crewai.knowledge.source.text_file_knowledge_source import TextFileKnowledgeSource
import shutil

# 加载环境变量
load_dotenv()

# Create a text file knowledge source
research_source_preference = TextFileKnowledgeSource(
    file_paths=["research_source_preference.txt"]
)
research_methodology = TextFileKnowledgeSource(
    file_paths=["research_methodology.txt"]
)

# If you want to run a snippet of code before or after the crew starts, 
# you can use the @before_kickoff and @after_kickoff decorators
# https://docs.crewai.com/concepts/crews#example-crew-class-with-decorators


@CrewBase
class TopicResearchCrew():
	"""TopicResearchCrew crew"""

	# Learn more about YAML configuration files here:
	# Agents: https://docs.crewai.com/concepts/agents#yaml-configuration-recommended
	# Tasks: https://docs.crewai.com/concepts/tasks#yaml-configuration-recommended
	agents_config = 'config/agents.yaml'
	tasks_config = 'config/tasks.yaml'


	# If you would like to add tools to your agents, you can learn more about it here:
	# https://docs.crewai.com/concepts/agents#agent-tools
	
	@agent
	def principal_researcher(self) -> Agent:
		return Agent(
			config=self.agents_config['principal_researcher'],
			verbose=True,
			llm=self.gemini_2_flash_thinking_llm,
			knowledge_sources=[research_methodology, research_source_preference],
		)

	@agent
	def data_extraction_specialist(self) -> Agent:
		return Agent(
			config=self.agents_config['data_extraction_specialist'],
			tools=[SerperDevTool()],
   			knowledge_sources=[research_source_preference],
			verbose=True,
			llm=self.gemini_2_flash_lite_llm
		)
  
	@agent
	def senior_researcher(self) -> Agent:
		return Agent(
			config=self.agents_config['senior_researcher'],
			verbose=True,
			llm=self.gemini_2_flash_lite_llm
		)
 
	# To learn more about structured task outputs, 
	# task dependencies, and task callbacks, check out the documentation:
	# https://docs.crewai.com/concepts/tasks#overview-of-a-task
	@task
	def research_planning_task(self) -> Task:
		return Task(
			config=self.tasks_config['research_planning_task'],
			output_file='output/01_research_planning_report.md'
		)
	@task
	def data_extraction_task(self) -> Task:
		return Task(
			config=self.tasks_config['data_extraction_task'],
			output_file='output/02_data_extraction_report.md'
		)
	@task
	def analysis_task(self) -> Task:
		return Task(
			config=self.tasks_config['analysis_task'],
			output_file='output/03_analysis_report.md'
		)
	@task
	def insight_synthesis_task(self) -> Task:
		return Task(
			config=self.tasks_config['insight_synthesis_task'],
			output_file='output/04_insight_synthesis_report.md'
		)
	# @task
	# def expert_review_task(self) -> Task:
	# 	return Task(
	# 		config=self.tasks_config['expert_review_task'],
	# 		output_file='output/05_expert_review_report.md'
	# 	)

	@crew
	def crew(self) -> Crew:
		"""Creates the TopicResearchCrew crew"""
		return Crew(
			agents=self.agents,
			tasks=self.tasks,
			process=Process.sequential,
			verbose=True,
			language="Chinese",
   			knowledge_sources=[research_methodology, research_source_preference]
		)

	def __init__(self):
		super().__init__()
		# 设置默认 LLM
		self.gemini_2_flash_thinking_llm = LLM(model="gemini/gemini-2.0-flash-thinking-exp-01-21")
		self.gemini_2_flash_lite_llm = LLM(model="gemini/gemini-2.0-flash-lite")
		self.deepseek_llm = LLM(model="deepseek/deepseek-chat")
		# self.gpt_llm = LLM(model="gpt-4o")
  
		# clean up output folder
		if os.path.exists("output"):
			shutil.rmtree("output")
    
