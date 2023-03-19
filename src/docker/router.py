from docker.views import containers_views, images_views, networks_views, volumes_views, plugins_views, system_views


def setup_routes(app):
    # containers
    app.router.add_view('/containers', containers_views.ContainerCollectionView)
    app.router.add_view('/containers/inspect', containers_views.ContainerCollectionInspectView)
    app.router.add_view('/containers/prune', containers_views.ContainerPruneView)
    app.router.add_view('/containers/run', containers_views.ContainerRunView)

    app.router.add_view('/containers/{container_id}', containers_views.ContainerInspectView)
    app.router.add_view('/containers/{container_id}/kill', containers_views.ContainerKillView)
    app.router.add_view('/containers/{container_id}/stop', containers_views.ContainerStopView)
    app.router.add_view('/containers/{container_id}/pause', containers_views.ContainerPauseView)
    app.router.add_view('/containers/{container_id}/restart', containers_views.ContainerRestartView)
    app.router.add_view('/containers/{container_id}/start', containers_views.ContainerStartView)
    app.router.add_view('/containers/{container_id}/unpause', containers_views.ContainerUnpauseView)

    app.router.add_view('/containers/{container_id}/logs', containers_views.ContainerLogsView)
    app.router.add_view('/containers/{container_id}/terminal', containers_views.ContainerTerminalView)
    app.router.add_view('/containers/{container_id}/stats', containers_views.ContainerStatsView)

    # images
    app.router.add_view('/images', images_views.ImageCollectionView)
    app.router.add_view('/images/inspect', images_views.ImageCollectionInspectView)
    app.router.add_view('/images/prune', images_views.ImagePruneView)
    app.router.add_view('/images/build', images_views.ImageBuildView)
    app.router.add_view('/images/pull', images_views.ImagePullView)

    app.router.add_view('/images/{image_id}', images_views.ImageInspectView)
    app.router.add_view('/images/{image_id}/tag', images_views.ImageTagView)

    # networks
    app.router.add_view('/networks', networks_views.NetworkCollectionView)
    app.router.add_view('/networks/inspect', networks_views.NetworkCollectionInspectView)
    app.router.add_view('/networks/prune', networks_views.NetworkPruneView)
    app.router.add_view('/networks/create', networks_views.NetworkCreateView)

    app.router.add_view('/networks/{network_id}', networks_views.NetworkInspectView)
    app.router.add_view('/networks/{network_id}/connect', networks_views.NetworkConnectContainerView)
    app.router.add_view('/networks/{network_id}/disconnect', networks_views.NetworkDisconnectContainerView)

    # volumes
    app.router.add_view('/volumes', volumes_views.VolumeCollectionView)
    app.router.add_view('/volumes/inspect', volumes_views.VolumeCollectionInspectView)
    app.router.add_view('/volumes/prune', volumes_views.VolumePruneView)
    app.router.add_view('/volumes/create', volumes_views.VolumeCreateView)

    app.router.add_view('/volumes/{volume_id}', volumes_views.VolumeInspectView)

    # plugins
    app.router.add_view('/plugins', plugins_views.PluginCollectionView)
    app.router.add_view('/plugins/inspect', plugins_views.PluginCollectionInspectView)
    app.router.add_view('/plugins/install', plugins_views.PluginInstallView)

    app.router.add_view('/plugins/{plugin_id}', plugins_views.PluginInspectView)
    app.router.add_view('/plugins/{plugin_id}/enable', plugins_views.PluginEnableView)
    app.router.add_view('/plugins/{plugin_id}/disable', plugins_views.PluginDisableView)

    # system
    app.router.add_view('/system', system_views.SystemInfoView)
    app.router.add_view('/system/df', system_views.SystemDataUsageView)
    app.router.add_view('/system/prune', system_views.SystemPruneView)
    app.router.add_view('/system/events', system_views.SystemEventsView)
    app.router.add_view('/version', system_views.VersionView)
    app.router.add_view('/auth', system_views.AuthView)
