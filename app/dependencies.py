import os
import logging 

from openai import AsyncAzureOpenAI
from fastapi import Depends

from .repos.gscholar_repository import GoogleScholarRepository
from .repos.title_generator_repository import CapstoneTitleGeneratorRepository
from .services.gscholar_service import GoogleScholarService
from .services.capstone_title_gen_service import CapstoneTitleService
from .services.oai_services import get_async_azoai_client

logger = logging.getLogger(__name__)

def get_gscholar_repository():
    return GoogleScholarRepository()

def get_capstone_generator_repository(async_azure_openai_client: AsyncAzureOpenAI = Depends(get_async_azoai_client)):
    try:
        return CapstoneTitleGeneratorRepository(async_azure_openai_client=async_azure_openai_client)
    except Exception as e:
        logger.error(f"Failed to initialize dependencie due to error encountered: {e}")
        raise e

def get_gscholar_service(repository: GoogleScholarRepository = Depends(get_gscholar_repository)):
    return GoogleScholarService(repository)

def get_capstone_title_service(repository: CapstoneTitleGeneratorRepository = Depends(get_capstone_generator_repository)):
    try:
        return CapstoneTitleService(repository)
    except Exception as e:
        logger.error(f"Failed to initialize dependencie due to error encountered: {e}")
        raise e