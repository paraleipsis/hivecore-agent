from typing import Mapping, MutableMapping, List, Optional, Union

from aiodocker import Docker
from aiohttp import web
from aiohttp_pydantic import PydanticView
from aiohttp_pydantic.oas.typing import r200

from docker.client import images
from docker.schemas import schemas, images_schemas
from utils.exceptions_utils import manage_exceptions


class ImageCollectionView(PydanticView):
    @manage_exceptions
    async def get(self, list_all: bool = False, shared_size: bool = False, filters: Mapping = None,
                  digests: bool = False) -> r200[schemas.GenericResponseModel[List[MutableMapping]]]:
        async with Docker() as session:
            images_list = await images.list_images(
                docker_session=session,
                list_all=list_all,
                shared_size=shared_size,
                filters=filters,
                digests=digests
            )
            return web.json_response(
                data=schemas.GenericResponseModel(
                    data=images_list,
                    total=len(images_list)
                ).dict()
            )


class ImageCollectionInspectView(PydanticView):
    @manage_exceptions
    async def get(self) -> r200[schemas.GenericResponseModel[List[MutableMapping]]]:
        async with Docker() as session:
            images_details_list = await images.get_images(
                docker_session=session,
            )
            return web.json_response(
                data=schemas.GenericResponseModel(
                    data=images_details_list,
                    total=len(images_details_list)
                ).dict()
            )


class ImageInspectView(PydanticView):
    @manage_exceptions
    async def get(self, image_id: str, /) -> r200[schemas.GenericResponseModel[MutableMapping]]:
        async with Docker() as session:
            image_details = await images.inspect_image(
                docker_session=session,
                image_id=image_id
            )
            return web.json_response(
                data=schemas.GenericResponseModel(
                    data=image_details,
                ).dict()
            )

    @manage_exceptions
    async def delete(self, image_id: str, /, force: bool = False,
                     noprune: bool = False) -> r200[schemas.GenericResponseModel[bool]]:
        async with Docker() as session:
            data = await images.remove_image(
                docker_session=session,
                image_id=image_id,
                force=force,
                noprune=noprune
            )
            return web.json_response(
                data=schemas.GenericResponseModel(
                    data=data,
                ).dict()
            )


class ImageBuildView(PydanticView):
    @manage_exceptions
    async def post(self, config: images_schemas.ImageBuild) -> r200[schemas.GenericResponseModel[bool]]:
        async with Docker() as session:
            data = await images.build_image(docker_session=session, config=config.dict())
            return web.json_response(
                data=schemas.GenericResponseModel(
                    data=data,
                ).dict()
            )


class ImagePullView(PydanticView):
    @manage_exceptions
    async def post(
            self,
            from_image: str,
            auth: Optional[Union[MutableMapping, str, bytes]] = None,
            tag: str = None,
            repo: str = None,
    ) -> r200[schemas.GenericResponseModel[bool]]:
        async with Docker() as session:
            data = await images.pull_image(
                docker_session=session,
                from_image=from_image,
                tag=tag,
                auth=auth,
                repo=repo,

            )
            return web.json_response(
                data=schemas.GenericResponseModel(
                    data=data,
                ).dict()
            )


class ImageTagView(PydanticView):
    @manage_exceptions
    async def post(self, image_id: str, /, repo: str,
                   tag: str = None) -> r200[schemas.GenericResponseModel[bool]]:
        async with Docker() as session:
            data = await images.tag_image(
                docker_session=session,
                image_id=image_id,
                repo=repo,
                tag=tag
            )
            return web.json_response(
                data=schemas.GenericResponseModel(
                    data=data,
                ).dict()
            )


class ImagePruneView(PydanticView):
    @manage_exceptions
    async def post(self, filters: Mapping = None) -> r200[schemas.GenericResponseModel[MutableMapping]]:
        async with Docker() as session:
            data = await images.prune_images(
                docker_session=session,
                filters=filters,
            )
            return web.json_response(
                data=schemas.GenericResponseModel(
                    data=data,
                ).dict()
            )
