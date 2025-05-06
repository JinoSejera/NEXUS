import json
from pathlib import Path
from typing import Dict, Any

from semantic_kernel.connectors.ai.open_ai import AzureChatCompletion
from semantic_kernel.functions import KernelArguments
from semantic_kernel import Kernel
from openai import AsyncAzureOpenAI
from openai import AsyncAzureOpenAI

from ..contract.title_gen_base import TitleGenBase

current_path = Path(__file__).resolve().parent
chat_id = "nexus"
plugin_dir = current_path / "../plugins/"


class CapstoneTitleGeneratorRepository(TitleGenBase):
    def __init__(self, async_azure_openai_client: AsyncAzureOpenAI):
        
        self.__kernel = Kernel()
        self.__kernel.add_service(AzureChatCompletion(
            service_id=chat_id,
            async_client=async_azure_openai_client
        ))

        self.__title_gen = self.__kernel.add_plugin(parent_directory=plugin_dir, plugin_name="NexusTextGenerationPlugin")
        
    async def generate_titles(self, query:str, course:str) -> Dict[str, Any]:
        result = await self.__kernel.invoke(
            self.__title_gen['CapstoneTitleGenerator'],
            KernelArguments(query=query,course=course)
        )
        
        return json.loads(str(result))