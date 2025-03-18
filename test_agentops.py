import agentops
import os
from dotenv import load_dotenv
import logging

# 设置日志级别
logging.basicConfig(
    level=logging.DEBUG,  # 使用 DEBUG 级别以获取更多信息
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# 加载环境变量
load_dotenv()

def test_agentops():
    # 直接使用新的 API key
    api_key = "96803216-81da-4c0f-a09f-55de7a2d2ffb"
    logger.info(f"Testing AgentOps with API key: {api_key}")
    
    try:
        session = agentops.init(api_key=api_key, tags=["Test"])
        logger.info("AgentOps initialized successfully")
        
        # 创建一个简单的测试任务
        logger.info("Test task started")
        
        # 模拟一些工作
        import time
        time.sleep(1)
        
        # 结束任务
        logger.info("Test task completed")
        
        # 结束会话
        session.end_session()
        logger.info("AgentOps session ended successfully")
    except Exception as e:
        logger.error(f"Error during AgentOps test: {str(e)}", exc_info=True)

if __name__ == "__main__":
    test_agentops() 