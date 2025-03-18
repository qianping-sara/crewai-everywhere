from typing import Type, Dict, Any, Optional
import os
from google import genai
import logging

from crewai.tools import BaseTool
from pydantic import BaseModel, Field

# 设置logger
logger = logging.getLogger(__name__)


class FileUploadToolInput(BaseModel):
    """Input schema for FileUploadToolInput."""

    filePath: str = Field(..., description="Path to the document to be uploaded.")
    api_key: Optional[str] = Field(None, description="Google AI API Key，如不提供将从环境变量GEMINI_API_KEY获取")


class FileUploadResponse(BaseModel):
    """FileUploadTool的响应模型"""
    
    success: bool = Field(..., description="操作是否成功")
    name: Optional[str] = Field(None, description="文件唯一标识符")
    uri: Optional[str] = Field(None, description="文件URI，用于后续API调用引用该文件")
    display_name: Optional[str] = Field(None, description="文件显示名称")
    mime_type: Optional[str] = Field(None, description="文件MIME类型")
    state: Optional[str] = Field(None, description="文件处理状态")
    size_bytes: Optional[int] = Field(None, description="文件大小（字节）")
    error: Optional[str] = Field(None, description="如果操作失败，包含错误信息")


class FileUploadTool(BaseTool):
    name: str = "File Upload Tool"
    description: str = (
        "上传文件到Google AI服务，支持各种格式的文件(图片、PDF、文本等)，并返回文件信息用于后续操作"
    )
    args_schema: Type[BaseModel] = FileUploadToolInput

    def _run(self, filePath: str, api_key: Optional[str] = None) -> FileUploadResponse:
        """
        上传文件到Google AI服务
        
        Args:
            filePath: 要上传的文件路径
            api_key: Google AI API密钥，如不提供则从环境变量获取
            
        Returns:
            FileUploadResponse对象，包含文件信息
        """
        
        logger.info("Uploading file to google API: %s", filePath)
        
        try:
            
                
            # 初始化客户端
            client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))
            
            # 上传文件
            file_obj = client.files.upload(file=filePath)
            logger.info("File uploaded successfully: %s", file_obj.uri)
            
            # 返回文件信息
            return FileUploadResponse(
                success=True,
                name=file_obj.name,
                uri=file_obj.uri,
                display_name=file_obj.display_name,
                mime_type=file_obj.mime_type,
                state=file_obj.state,
                size_bytes=file_obj.size_bytes
            )
            
        except Exception as e:
            logger.error("Error uploading file: %s", str(e))
            return FileUploadResponse(
                success=False,
                error=str(e)
            )
