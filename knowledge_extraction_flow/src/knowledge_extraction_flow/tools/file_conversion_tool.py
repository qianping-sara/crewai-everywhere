from typing import Type, Dict, Any, Optional
import os
from google import genai
import logging

from crewai.tools import BaseTool
from pydantic import BaseModel, Field

# 设置logger
logger = logging.getLogger(__name__)


class FileConversionToolInput(BaseModel):
    """Input schema for FileConversionToolInput."""

    file_uri: str = Field(..., description="已上传文件的URI，通过FileUploadTool获取")
    api_key: Optional[str] = Field(None, description="Google AI API Key，如不提供将从环境变量GEMINI_API_KEY获取")
    model_name: Optional[str] = Field(None, description="要使用的Gemini模型名称，不提供则从环境变量GEMINI_DOC_MODEL获取")


class FileConversionResponse(BaseModel):
    """FileConversionTool的响应模型"""
    
    success: bool = Field(..., description="操作是否成功")
    markdown_content: Optional[str] = Field(None, description="转换后的markdown内容")
    original_file_uri: Optional[str] = Field(None, description="原始文件的URI")
    error: Optional[str] = Field(None, description="如果操作失败，包含错误信息")
    model_used: Optional[str] = Field(None, description="实际使用的模型名称")


class FileConversionTool(BaseTool):
    name: str = "File Conversion Tool"
    description: str = (
        "将上传到Google AI服务的文件内容转换为规范的Markdown格式。此工具需要接收已上传文件的URI，然后使用Gemini模型进行内容转换。"
    )
    args_schema: Type[BaseModel] = FileConversionToolInput

    def _run(self, file_uri: str, api_key: Optional[str] = None, model_name: Optional[str] = None) -> FileConversionResponse:
        """
        将文件转换为markdown格式
        
        Args:
            file_uri: 已上传文件的URI
            api_key: Google AI API密钥，如不提供则从环境变量获取
            model_name: 要使用的Gemini模型名称，不提供则从环境变量获取
            
        Returns:
            FileConversionResponse对象，包含转换结果
        """
        
        logger.info("Converting file to md: %s", file_uri)
        
        try:
            # 获取API密钥
            if api_key:
                api_key_value = api_key
            elif os.environ.get("GEMINI_API_KEY"):
                api_key_value = os.environ.get("GEMINI_API_KEY")
            else:
                raise ValueError("未提供API密钥，请通过参数传入或设置GEMINI_API_KEY环境变量")
            
            # 获取文档转换模型名称
            if model_name:
                doc_model = model_name
            elif os.environ.get("GEMINI_DOC_MODEL"):
                doc_model = os.environ.get("GEMINI_DOC_MODEL")
            else:
                # 默认模型
                doc_model = "gemini-2.0-flash-lite"
                
            # 初始化客户端
            client = genai.Client(api_key=api_key_value)
            
            # 创建markdown转换提示词
            markdown_prompt = """
            请将给定的<需求文档>整理为 markdown 代码格式。你需要严格遵循以下<Rules>和<Instructions>进行整理输出。

            <Rules>
            1. 认真仔细，严格根据<Instructions>中的步骤要求仔细整理
            2. **禁止改变原来内容、措辞和语义**
            3. **禁止添加、杜撰内容**
            4. **Markdown表格中**禁止加空格**，保持精炼节约token
            5. **禁止加空行和分隔符(---)**，保持精炼以节约token
            6. **输出语言与给定需求文档语言一致**，禁止翻译
            </Rules>

            <Instructions>
            你需要按照以下步骤，一步步分析输出：
            #1. 先通读<需求文档>内容，理解主要内容
            #2. 识别并删除无效内容：
                - 仔细阅读原文，如果原文中章节标题后明确标注了**（先不做）**、**(不需要）**，在整理输出时把这个章节删除；
                - 如果原文中中某一行内容标注了**（先不做）**、**(不需要）**，则整理输出时把这行内容移除。
            #3. 逐句阅读文档内容，做格式整理：
                - **除了2中删除的内容，禁止遗漏文档中的任何依据原文和细节文字**
            #4. 格式整理要求
            ##4.1 层次结构：
                - 标题层次：根据内容逻辑调整标题层级（一级标题#，二级标题##，三级标题###，四级标题####等），尽量与原文层次保持一致。
                - 标题内部层次结构：使用合适的列表（如-、1.等）标注层级关系，子项应以缩进或嵌套列表体现，尽量与原文层次保持一致。
                - 章节序号：对照原有内容，整理章节序号，确保每层内的内容序号正确合理。
            ##4.2 表格处理：
                - 将文档中的表格内容整理为Markdown表格，确保表头、列对齐清晰。
                - Markdownd表格中**禁止加空格**，保持精炼节约token
            ##4.3 关键内容突出：
                - 使用加粗（**）或斜体（*）格式化文档中的重点内容或关键字。
            ##4.4 图片、代码、URL等处理：
                - 路径及代码格式：对操作路径、指令等内容使用反引号（``）进行代码格式化
                - 对图片、资源等保留占位符，使用![Image](#)形式标记
            ##4.5 错别字、笔误处理：
                - 对文档中可能的错别字、拼写错误、笔误，在其后加(?)表示提醒
                - 对文档中提到的参考XXX、参照XXX，但给定文档中又未能找到的，也在其后加(?)表示提醒
            #5. 整理检查，使用markdown代码格式输出
                - 对照整理结果和原文文档，确保除了标注不要的内容之外，没有遗漏任何细节
                - 确保遵守原文内容、措辞和语义
                - 根据<Rules>做检查和纠正
            </Instructions>

            请以Markdown文档格式化专家的身份，严格按照以上规则和指令对文档内容进行处理并输出。你的目标是将原始文档转换为清晰、规范的Markdown格式，同时准确保留原文内容。
            """
            
            # 调用Gemini模型处理文件
            response = client.models.generate_content(
                model=doc_model,
                contents=[
                    {
                        "fileData": {
                            "fileUri": file_uri,
                            "mimeType": "application/pdf"  # 默认为PDF，实际上API会自动检测
                        }
                    },
                    "\n\n",
                    markdown_prompt
                ]
            )
            
            # 提取转换后的markdown内容
            markdown_content = response.text
            
            return FileConversionResponse(
                success=True,
                markdown_content=markdown_content,
                original_file_uri=file_uri,
                model_used=doc_model
            )
            
        except Exception as e:
            logger.error("Error converting file: %s", str(e))
            return FileConversionResponse(
                success=False,
                error=str(e)
            )
