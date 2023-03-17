from aiohttp import web
from docker.views import (ContainerCollectionView, ContainerInspectView,
                          ContainerCollectionInspectView, ContainerPruneView)

app = web.Application()

app.router.add_view('/containers', ContainerCollectionView)
app.router.add_view('/containers/inspect', ContainerCollectionInspectView)
app.router.add_view('/containers/prune', ContainerPruneView)
app.router.add_view('/containers/{container_id}', ContainerInspectView)
for resource in app.router.resources():
    print(resource)
web.run_app(app)
