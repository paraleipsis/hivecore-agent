import functools

from aiodocker import DockerError
from aiohttp import web

from modules.schemas import response_schemas as schemas
from logger.logs import logger


def manage_exceptions(func):
    @functools.wraps(func)
    async def wrap_func(*args, **kwargs):
        try:
            result = await func(*args, **kwargs)
        except DockerError as de:
            logger['debug'].debug(
                f'{type(de).__name__}: {str(de)}'
            )
            return web.json_response(
                status=de.status,
                data=schemas.GenericResponseModel(success=False, error_msg=de.message).dict()
            )
        except Exception as e:
            logger['error'].error(
                f'{type(e).__name__}: {str(e)}'
            )
            return web.json_response(
                status=500,
                data=schemas.GenericResponseModel(success=False, error_msg=str(e)).dict()
            )
        return result

    return wrap_func
