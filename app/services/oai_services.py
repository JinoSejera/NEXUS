import os
from dotenv import load_dotenv

from openai import AsyncAzureOpenAI

load_dotenv()
azure_openai_endpoint = os.getenv('AZURE_OPENAI_ENDPOINT') or (lambda:(_ for _ in ()).throw(ValueError("AZURE_OPENAI_ENDPOINT is not set")))()
azure_openai_api_version = os.getenv('AZURE_OPENAI_API_VERSION') or (lambda:(_ for _ in ()).throw(ValueError("AZURE_OPENAI_API_VERSION is not set")))()
azure_openai_key = os.getenv('AZURE_OPENAI_API_KEY') or (lambda:(_ for _ in ()).throw(ValueError("AZURE_OPENAI_API_KEY is not set")))()

def get_async_azoai_client() -> AsyncAzureOpenAI:
    return AsyncAzureOpenAI(
        azure_endpoint=azure_openai_endpoint,
        api_key=azure_openai_key,
        api_version=azure_openai_api_version
    )

