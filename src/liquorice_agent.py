from aiohttp import web
from docker.views import (ContainerCollectionView, ContainerInspectView, ContainerLogsView, ContainerStatsView,
                          ContainerCollectionInspectView, ContainerPruneView, ContainerRunView, ContainerTerminalView,
                          ContainerKillView, ContainerStopView, ContainerPauseView, ContainerRestartView,
                          ContainerStartView, ContainerUnpauseView)

app = web.Application()

app.router.add_view('/containers', ContainerCollectionView)
app.router.add_view('/containers/inspect', ContainerCollectionInspectView)
app.router.add_view('/containers/prune', ContainerPruneView)
app.router.add_view('/containers/run', ContainerRunView)
app.router.add_view('/containers/{container_id}', ContainerInspectView)

app.router.add_view('/containers/{container_id}/', ContainerKillView)
app.router.add_view('/containers/{container_id}/', ContainerStopView)
app.router.add_view('/containers/{container_id}/', ContainerPauseView)
app.router.add_view('/containers/{container_id}/', ContainerRestartView)
app.router.add_view('/containers/{container_id}/', ContainerStartView)
app.router.add_view('/containers/{container_id}/', ContainerUnpauseView)

app.router.add_view('/containers/{container_id}/logs', ContainerLogsView)
app.router.add_view('/containers/{container_id}/terminal', ContainerTerminalView)
app.router.add_view('/containers/{container_id}/stats', ContainerStatsView)

web.run_app(app)
