#!/usr/bin/env python
from random import randint
from pydantic import BaseModel
from crewai.flow import Flow, listen, start
from crews.doc_conversion_crew.doc_conversion_crew import DocConversionCrew
import agentops
import logging
import os

logger = logging.getLogger(__name__)


class ExtractionState(BaseModel):
    filePath: str
    markdown_content: str = ""


class KnowledgeExtractionFlow(Flow[ExtractionState]):
    def _create_initial_state(self) -> ExtractionState:
        return ExtractionState(filePath="/Users/qianping/Documents/Source/crew-ai/knowledge_extraction_flow/src/knowledge_extraction_flow/incoming/test.pdf")

    @start()
    def upload_and_generate_md(self):
        logger.info(f"Uploading and generating md {self.state.filePath}")
        result = (
            DocConversionCrew()
            .crew()
            .kickoff(inputs={"filePath": self.state.filePath})
        )
        logger.info(f"Result: {result}")

    # @listen(generate_md)
    # def generate_poem(self):
    #     print("Generating poem")
    #     result = (
    #         PoemCrew()
    #         .crew()
    #         .kickoff(inputs={"sentence_count": self.state.sentence_count})
    #     )

    #     print("Poem generated", result.raw)
    #     self.state.poem = result.raw

    # @listen(generate_poem)
    # def save_poem(self):
    #     print("Saving poem")
    #     with open("poem.txt", "w") as f:
    #         f.write(self.state.poem)


def kickoff():
    # 创建并启动flow
    try:
        if os.getenv("AGENTOPS_API_KEY"):
            session = agentops.init(api_key=os.getenv("AGENTOPS_API_KEY"),tags=["mail_crew"])
        else:
            session = None
            logger.warning("AGENTOPS_API_KEY not found, running without AgentOps")
    
        flow = KnowledgeExtractionFlow()
        flow.kickoff()
    except Exception as e:
        logger.error(f"An error occurred while running the flow: {e}", exc_info=True)
        raise
    finally:
        if session:
            logger.info("Ending AgentOps session")
            session.end_session()

# def plot():
#     poem_flow = PoemFlow()
#     poem_flow.plot()


if __name__ == "__main__":
    kickoff()
