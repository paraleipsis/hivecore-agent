from aiohttp import web
from docker.views.containers_views import (ContainerCollectionView, ContainerInspectView,
                                           ContainerLogsView, ContainerStatsView,
                                           ContainerCollectionInspectView, ContainerPruneView,
                                           ContainerRunView, ContainerTerminalView,
                                           ContainerKillView, ContainerStopView,
                                           ContainerPauseView, ContainerRestartView,
                                           ContainerStartView, ContainerUnpauseView)

app = web.Application()

app.router.add_view('/containers', ContainerCollectionView)
app.router.add_view('/containers/inspect', ContainerCollectionInspectView)
app.router.add_view('/containers/prune', ContainerPruneView)
app.router.add_view('/containers/run', ContainerRunView)
app.router.add_view('/containers/{container_id}', ContainerInspectView)

app.router.add_view('/containers/{container_id}/kill', ContainerKillView)
app.router.add_view('/containers/{container_id}/stop', ContainerStopView)
app.router.add_view('/containers/{container_id}/pause', ContainerPauseView)
app.router.add_view('/containers/{container_id}/restart', ContainerRestartView)
app.router.add_view('/containers/{container_id}/start', ContainerStartView)
app.router.add_view('/containers/{container_id}/unpause', ContainerUnpauseView)

app.router.add_view('/containers/{container_id}/logs', ContainerLogsView)
app.router.add_view('/containers/{container_id}/terminal', ContainerTerminalView)
app.router.add_view('/containers/{container_id}/stats', ContainerStatsView)

web.run_app(app)
