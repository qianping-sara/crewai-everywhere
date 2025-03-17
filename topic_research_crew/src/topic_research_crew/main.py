#!/usr/bin/env python
import sys
import warnings
import os
from dotenv import load_dotenv
from datetime import datetime
from crewai import Agent
from topic_research_crew.crew import TopicResearchCrew
import agentops
import subprocess

# 加载环境变量
load_dotenv()


# 忽略所有 Pydantic 相关的警告
warnings.filterwarnings("ignore", category=DeprecationWarning, module="pydantic")
warnings.filterwarnings("ignore", category=UserWarning, module="pydantic")
warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

def run():
    """
    Run the crew.
    """
    inputs = {
        'researchgoal': '我想了解招行近两年在AI（尤其关注大模型相关）方面的布局，关注业务与科技两侧的布局',
        'year': '2025',
        'research_domain': '金融、科技、AI、大模型'
    }
    try:
        if os.getenv("AGENTOPS_API_KEY"):
            session = agentops.init(api_key=os.getenv("AGENTOPS_API_KEY"))
        else:
            session = None
        TopicResearchCrew().crew().kickoff(inputs=inputs)
    except Exception as e:
        raise Exception(f"An error occurred while running the crew: {e}")
    finally:
        if session:
            session.end_session()
    

def replay(task_id):
  """
  Replay the crew execution from a specific task.
  """
#   inputs = {"topic": "CrewAI Training"}  # This is optional; you can pass in the inputs you want to replay; otherwise, it uses the previous kickoff's inputs.
  try:
      TopicResearchCrew().crew().replay(task_id=task_id)

  except subprocess.CalledProcessError as e:
      raise Exception(f"An error occurred while replaying the crew: {e}")

  except Exception as e:
      raise Exception(f"An unexpected error occurred: {e}")
  
  
if __name__ == "__main__":
    if len(sys.argv) > 1:
        command = sys.argv[1]
        if command == "run":
            run()
        elif command == "replay":
            replay(sys.argv[2])
    

