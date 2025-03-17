from typing import Type
from crewai.tools import BaseTool
from pydantic import BaseModel, Field
from .gmail_utility import authenticate_gmail, create_message, create_draft, send_email
import os
from agentops import Record_tool

class GmailToolInput(BaseModel):
    """Input schema for GmailTool."""
    body: str = Field(..., description="The body of the email to send.")
    researchgoal: str = Field(..., description="The research goal to use in the email subject.")
    should_send: bool = Field(default=False, description="Whether to send the email immediately or just create a draft.")

@Record_tool("GmailTool")
class GmailTool(BaseTool):
    name: str = "GmailTool"
    description: str = (
        "A tool to create Gmail draft emails or send emails directly with research reports."
    )
    args_schema: Type[BaseModel] = GmailToolInput

    def _run(self, body: str, researchgoal: str) -> str:
        try:
            service = authenticate_gmail()
            sender = os.getenv("GMAIL_SENDER")
            to = os.getenv("GMAIL_RECIPIENT")
            
            subject = "Research Report on topic: " + researchgoal
            message_text = body

            message = create_message(sender, to, subject, message_text)
            
            should_send = os.getenv("SHOULD_SEND")
            ## if should_send is 'true', send the email
            if should_send == 'true':
                result = send_email(service, "me", message)
                return f"Email sent successfully! Message id: {result['id']}" if result else "Failed to send email"
            else:
                draft = create_draft(service, "me", message)
                return f"Email draft created successfully! Draft id: {draft['id']}" if draft else "Failed to create draft"
        except Exception as e:
            return f"Error: {e}"

    async def _arun(self, body: str, researchgoal: str, should_send: bool = False) -> str:
        return self._run(body, researchgoal, should_send)

