from .repos.gscholar_repository import GoogleScholarRepository
from .repos.title_generator_repository import CapstoneTitleGeneratorRepository
from .services.gscholar_service import GoogleScholarService
from .services.capstone_title_gen_service import CapstoneTitleService

from azure.identity.aio import DefaultAzureCredential, get_bearer_token_provider
from openai import AsyncAzureOpenAI
from fastapi import Depends
import os

def get_gscholar_repository():
    return GoogleScholarRepository()

def get_capstone_generator_repository():
    _token_provider = get_bearer_token_provider(DefaultAzureCredential(),
                                                        'https://cognitiveservices.azure.com/.default')
    async_client = AsyncAzureOpenAI(azure_endpoint=os.getenv('AZURE_OPENAI_ENDPOINT'),
                    azure_ad_token_provider=_token_provider,
                    api_version=os.getenv('AZURE_OPENAI_API_VERSION'))
    print(os.getenv('AZURE_OPENAI_API_VERSION'))
    return CapstoneTitleGeneratorRepository(async_azure_openai_client=async_client)

def get_gscholar_service(repository: GoogleScholarRepository = Depends(get_gscholar_repository)):
    return GoogleScholarService(repository)

def get_capstone_title_service(repository: CapstoneTitleGeneratorRepository = Depends(get_capstone_generator_repository)):
    return CapstoneTitleService(repository)