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
import logging
from agentops import Record_tool

# 设置日志级别
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

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
        'researchgoal': '我想了解招行科技侧25年在大模型方面的布局和举措',
        'year': '2025',
        'research_domain': '金融科技、大模型'
    }
    try:
        agentops_api_key = os.getenv("AGENTOPS_API_KEY")
        if agentops_api_key:
            logger.info("Initializing AgentOps with API key...")
            try:
                # 初始化 AgentOps
                session = agentops.init(api_key=agentops_api_key, tags=["TopicResearchCrew"])
                logger.info("AgentOps initialized successfully")
            except Exception as e:
                logger.error(f"Failed to initialize AgentOps: {str(e)}")
        else:
            logger.warning("AGENTOPS_API_KEY not found in environment variables")
            
        logger.info("Starting TopicResearchCrew execution...")
        TopicResearchCrew().crew().kickoff(inputs=inputs)
        logger.info("TopicResearchCrew execution completed successfully")
       
    except Exception as e:
        logger.error(f"An error occurred while running the crew: {str(e)}", exc_info=True)
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
    

