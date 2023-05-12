from docker.views import containers_views, images_views, networks_views, volumes_views, plugins_views, system_views


def setup_routes(app):
    # containers
    app.router.add_view('/docker/containers', containers_views.ContainerCollectionView)
    app.router.add_view('/docker/containers/inspect', containers_views.ContainerCollectionInspectView)
    app.router.add_view('/docker/containers/prune', containers_views.ContainerPruneView)
    app.router.add_view('/docker/containers/run', containers_views.ContainerRunView)

    app.router.add_view('/docker/containers/{container_id}', containers_views.ContainerInspectView)
    app.router.add_view('/docker/containers/{container_id}/kill', containers_views.ContainerKillView)
    app.router.add_view('/docker/containers/{container_id}/stop', containers_views.ContainerStopView)
    app.router.add_view('/docker/containers/{container_id}/pause', containers_views.ContainerPauseView)
    app.router.add_view('/docker/containers/{container_id}/restart', containers_views.ContainerRestartView)
    app.router.add_view('/docker/containers/{container_id}/start', containers_views.ContainerStartView)
    app.router.add_view('/docker/containers/{container_id}/unpause', containers_views.ContainerUnpauseView)

    app.router.add_view('/docker/containers/{container_id}/logs', containers_views.ContainerLogsView)
    app.router.add_view('/docker/containers/{container_id}/terminal', containers_views.ContainerTerminalView)
    app.router.add_view('/docker/containers/{container_id}/stats', containers_views.ContainerStatsView)

    # images
    app.router.add_view('/docker/images', images_views.ImageCollectionView)
    app.router.add_view('/docker/images/inspect', images_views.ImageCollectionInspectView)
    app.router.add_view('/docker/images/prune', images_views.ImagePruneView)
    app.router.add_view('/docker/images/build', images_views.ImageBuildView)
    app.router.add_view('/docker/images/pull', images_views.ImagePullView)

    app.router.add_view('/docker/images/{image_id}', images_views.ImageInspectView)
    app.router.add_view('/docker/images/{image_id}/tag', images_views.ImageTagView)

    # networks
    app.router.add_view('/docker/networks', networks_views.NetworkCollectionView)
    app.router.add_view('/docker/networks/inspect', networks_views.NetworkCollectionInspectView)
    app.router.add_view('/docker/networks/prune', networks_views.NetworkPruneView)
    app.router.add_view('/docker/networks/create', networks_views.NetworkCreateView)

    app.router.add_view('/docker/networks/{network_id}', networks_views.NetworkInspectView)
    app.router.add_view('/docker/networks/{network_id}/connect', networks_views.NetworkConnectContainerView)
    app.router.add_view('/docker/networks/{network_id}/disconnect', networks_views.NetworkDisconnectContainerView)

    # volumes
    app.router.add_view('/docker/volumes', volumes_views.VolumeCollectionView)
    app.router.add_view('/docker/volumes/inspect', volumes_views.VolumeCollectionInspectView)
    app.router.add_view('/docker/volumes/prune', volumes_views.VolumePruneView)
    app.router.add_view('/docker/volumes/create', volumes_views.VolumeCreateView)

    app.router.add_view('/docker/volumes/{volume_id}', volumes_views.VolumeInspectView)

    # plugins
    app.router.add_view('/docker/plugins', plugins_views.PluginCollectionView)
    app.router.add_view('/docker/plugins/inspect', plugins_views.PluginCollectionInspectView)
    app.router.add_view('/docker/plugins/install', plugins_views.PluginInstallView)

    app.router.add_view('/docker/plugins/{plugin_id}', plugins_views.PluginInspectView)
    app.router.add_view('/docker/plugins/{plugin_id}/enable', plugins_views.PluginEnableView)
    app.router.add_view('/docker/plugins/{plugin_id}/disable', plugins_views.PluginDisableView)

    # system
    app.router.add_view('/docker/system', system_views.SystemInfoView)
    app.router.add_view('/docker/system/df', system_views.SystemDataUsageView)
    app.router.add_view('/docker/system/prune', system_views.SystemPruneView)
    app.router.add_view('/docker/system/events', system_views.SystemEventsView)
    app.router.add_view('/docker/system/version', system_views.VersionView)
    app.router.add_view('/docker/system/auth', system_views.AuthView)
    app.router.add_view('/docker/system/ping', system_views.PingView)
