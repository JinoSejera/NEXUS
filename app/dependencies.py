from .repos.gscholar_repository import GoogleScholarRepository
from .repos.title_generator_repository import CapstoneTitleGeneratorRepository
from .services.gscholar_service import GoogleScholarService
from .services.capstone_title_gen_service import CapstoneTitleService

from azure.identity.aio import DefaultAzureCredential, get_bearer_token_provider
from openai import AsyncAzureOpenAI
from fastapi import Depends
import os
import logging 

logger = logging.getLogger(__name__)

def get_gscholar_repository():
    return GoogleScholarRepository()

def get_capstone_generator_repository():
    try:
        azure_openai_endpoint = os.getenv('AZURE_OPENAI_ENDPOINT') or (lambda:(_ for _ in ()).throw(ValueError("AZURE_OPENAI_ENDPOINT is not set")))()
        azure_openai_api_version = os.getenv('AZURE_OPENAI_API_VERSION') or (lambda:(_ for _ in ()).throw(ValueError("AZURE_OPENAI_API_VERSION is not set")))()
        
        _token_provider = get_bearer_token_provider(DefaultAzureCredential(),
                                                            'https://cognitiveservices.azure.com/.default')
        async_client = AsyncAzureOpenAI(azure_endpoint=azure_openai_endpoint,
                        azure_ad_token_provider=_token_provider,
                        api_version=azure_openai_api_version)
        print(os.getenv('AZURE_OPENAI_API_VERSION'))
        return CapstoneTitleGeneratorRepository(async_azure_openai_client=async_client)
    except Exception as e:
        logger.error(f"Failed to initialize dependencie due to error encountered: {e}")
        raise e

def get_gscholar_service(repository: GoogleScholarRepository = Depends(get_gscholar_repository)):
    return GoogleScholarService(repository)

def get_capstone_title_service(repository: CapstoneTitleGeneratorRepository = Depends(get_capstone_generator_repository)):
    return CapstoneTitleService(repository)