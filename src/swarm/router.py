from swarm.views import configs_views, nodes_views, services_views, tasks_views


def setup_routes(app):
    # configs
    app.router.add_view('/configs', configs_views.ConfigCollectionView)
    app.router.add_view('/configs/inspect', configs_views.ConfigCollectionInspectView)
    app.router.add_view('/configs/create', configs_views.ConfigCreateView)

    app.router.add_view('/configs/{config_id}', configs_views.ConfigInspectView)

    # secrets
    app.router.add_view('/secrets', configs_views.ConfigCollectionView)
    app.router.add_view('/secrets/inspect', configs_views.ConfigCollectionInspectView)
    app.router.add_view('/secrets/create', configs_views.ConfigCreateView)

    app.router.add_view('/secrets/{secret_id}', configs_views.ConfigInspectView)

    # services
    app.router.add_view('/services', services_views.ServiceCollectionView)
    app.router.add_view('/services/inspect', services_views.ServiceCollectionInspectView)
    app.router.add_view('/services/create', services_views.ServiceCreateView)

    app.router.add_view('/services/{service_id}', services_views.ServiceInspectView)
    app.router.add_view('/services/{service_id}/logs', services_views.ServiceLogsView)

    # tasks
    app.router.add_view('/tasks', tasks_views.TaskCollectionView)
    app.router.add_view('/tasks/inspect', tasks_views.TaskCollectionInspectView)

    app.router.add_view('/tasks/{service_id}', tasks_views.TaskInspectView)
    app.router.add_view('/tasks/{service_id}/logs', tasks_views.TaskLogsView)

    # nodes
    app.router.add_view('/nodes', nodes_views.NodeCollectionView)
    app.router.add_view('/nodes/inspect', nodes_views.NodeCollectionInspectView)

    app.router.add_view('/nodes/{node_id}', nodes_views.NodeInspectView)
    app.router.add_view('/nodes/{node_id}/update', nodes_views.NodeUpdateView)

    # swarm
