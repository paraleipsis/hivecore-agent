from aiodocker.docker import Docker
from typing import List, Mapping, BinaryIO, MutableMapping

from aiodocker.utils import clean_filters


async def get_images(docker_session: Docker) -> List[Mapping]:
    images = docker_session.images
    images_details_list = [await images.inspect(i['Id']) for i in await images.list()]

    return images_details_list


async def tag_image(docker_session: Docker, name: str, repo: str, tag: str = None) -> bool:
    await docker_session.images.tag(name=name, repo=repo, tag=tag)

    return True


async def remove_image(docker_session: Docker, name: str, force: bool = False, noprune: bool = False) -> bool:
    await docker_session.images.delete(name=name, force=force, noprune=noprune)

    return True


async def build_image_from_fileobj(docker_session: Docker, fileobj: BinaryIO = None, **kwargs) -> bool:
    await docker_session.images.build(fileobj=fileobj, **kwargs)

    return True


async def pull_image(docker_session: Docker, from_image: str, tag: str = None, **kwargs) -> bool:
    if tag is None:
        tag = 'latest'

    await docker_session.images.pull(from_image=from_image, tag=tag, **kwargs)

    return True


async def prune_images(docker_session: Docker, filters: Mapping = None) -> MutableMapping:
    params = {"filters": clean_filters(filters)}
    response = await docker_session._query_json("images/prune", method="POST", params=params)
    return response


async def prune_images_builds(docker_session: Docker):
    pass


async def push_image(docker_session: Docker):
    pass


async def search_image(docker_session: Docker):
    pass






# import asyncio
#
#
# async def main():
#     # async with Docker() as session:
#     #     c = await pull_image(docker_session=session, from_image='nginx', tag='alpine')
#     image = 'nginx'
#     c = image.split(":")[1]
#     return c
#
# print(asyncio.run(main()))
