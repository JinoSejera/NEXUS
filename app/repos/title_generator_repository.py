from semantic_kernel.connectors.ai.open_ai import AzureChatCompletion
from semantic_kernel.functions import KernelArguments
from semantic_kernel import Kernel

from openai import AsyncAzureOpenAI
import os
import sys
import json
from pathlib import Path
from openai import AsyncAzureOpenAI

current_path = Path(__file__).resolve().parent
chat_id = "nexus"

class CapstoneTitleGeneratorRepository:
    def __init__(self, async_azure_openai_client: AsyncAzureOpenAI):
        
        self._kernel = Kernel()
        self._kernel.add_service(AzureChatCompletion(
            service_id=chat_id,
            async_client=async_azure_openai_client
        ))

        plugin_dir = current_path / "../plugins/"
        
        print(plugin_dir)

        self._title_gen = self._kernel.add_plugin(parent_directory=plugin_dir, plugin_name="NexusTextGenerationPlugin")
        
    async def generate_titles(self, query:str):
        result = await self._kernel.invoke(
            self._title_gen['CapstoneTitleGenerator'],
            KernelArguments(query=query)
        )
        
        return json.loads(str(result))