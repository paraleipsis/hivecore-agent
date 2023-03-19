import tarfile
import tempfile
from io import BytesIO

from aiodocker.docker import Docker
from typing import List, Mapping, MutableMapping

from aiodocker.utils import clean_filters


async def list_images(docker_session: Docker, list_all: bool = False, shared_size: bool = False,
                      filters: Mapping = None, digests: bool = False) -> List[Mapping]:
    params = {"filters": clean_filters(filters), "all": list_all, "shared-size": shared_size, "digests": digests}
    images = await docker_session._query_json("images/json", "GET", params=params)
    return images


async def inspect_image(docker_session: Docker, image_id: str) -> List[Mapping]:
    images = docker_session.images
    image = await images.inspect(name=image_id)
    return image


async def get_images(docker_session: Docker) -> List[Mapping]:
    images = docker_session.images
    images_details_list = [await images.inspect(i['Id']) for i in await images.list()]

    return images_details_list


async def tag_image(docker_session: Docker, image_id: str, repo: str, tag: str = None) -> bool:
    await docker_session.images.tag(name=image_id, repo=repo, tag=tag)

    return True


async def remove_image(docker_session: Docker, image_id: str, force: bool = False, noprune: bool = False) -> bool:
    await docker_session.images.delete(name=image_id, force=force, noprune=noprune)

    return True


async def build_image(docker_session: Docker, config: MutableMapping) -> bool:
    if 'fileobj' in config:
        encoding = 'utf-8'
        dockerfile = BytesIO(config['fileobj'].encode(encoding))

        f = tempfile.NamedTemporaryFile()
        t = tarfile.open(mode='w', fileobj=f)

        dfinfo = tarfile.TarInfo('Dockerfile')
        dfinfo.size = len(dockerfile.getvalue())
        dockerfile.seek(0)

        t.addfile(dfinfo, dockerfile)
        t.close()
        f.seek(0)

        config['fileobj'] = f
        config['encoding'] = encoding

    await docker_session.images.build(**config)

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





# import asyncio
# async def main():
#     dockerfile = '''
#         # Shared Volume
#         FROM busybox:buildroot-2014.02
#         VOLUME /data
#         CMD ["/bin/sh"]
#         '''
#     config = {
#         "fileobj": dockerfile,
#         'encoding': 'utf-8'
#     }
#     async with Docker() as session:
#         c = await build_image(docker_session=session, config=config)
#
#     return c
#
# print(asyncio.run(main()))
