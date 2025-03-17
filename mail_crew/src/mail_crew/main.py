#!/usr/bin/env python
import sys
import warnings
from dotenv import load_dotenv
from datetime import datetime
import agentops
from mail_crew.crew import MailCrew
import os
import logging

# 设置日志级别
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# 加载环境变量
load_dotenv()

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

# This main file is intended to be a way for you to run your
# crew locally, so refrain from adding unnecessary logic into this file.
# Replace with inputs you want to test with, it will automatically
# interpolate any tasks and agents information

def run():
    """
    Run the crew.
    """
    logger.info("Starting MailCrew execution...")
    inputs = {
        'body': 'this is a body',
        'should_send': 'true'
    }
    logger.info(f"Using inputs: {inputs}")
    os.environ["SHOULD_SEND"] = inputs['should_send']
    
    try:
        if os.getenv("AGENTOPS_API_KEY"):
            session = agentops.init(api_key=os.getenv("AGENTOPS_API_KEY"))
        else:
            session = None
            logger.warning("AGENTOPS_API_KEY not found, running without AgentOps")
        
        logger.info("Creating and starting crew...")
        result = MailCrew().crew().kickoff(inputs=inputs)
        logger.info(f"Crew execution completed with result: {result}")
    except Exception as e:
        logger.error(f"An error occurred while running the crew: {e}", exc_info=True)
        raise
    finally:
        if session:
            logger.info("Ending AgentOps session")
            session.end_session()
    
if __name__ == "__main__":
    run()
