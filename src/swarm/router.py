from swarm.views import configs_views, nodes_views, services_views, tasks_views, swarm_views


def setup_routes(app):
    # configs
    app.router.add_view('/swarm/configs', configs_views.ConfigCollectionView)
    app.router.add_view('/swarm/configs/inspect', configs_views.ConfigCollectionInspectView)
    app.router.add_view('/swarm/configs/create', configs_views.ConfigCreateView)

    app.router.add_view('/swarm/configs/{config_id}', configs_views.ConfigInspectView)

    # secrets
    app.router.add_view('/swarm/secrets', configs_views.ConfigCollectionView)
    app.router.add_view('/swarm/secrets/inspect', configs_views.ConfigCollectionInspectView)
    app.router.add_view('/swarm/secrets/create', configs_views.ConfigCreateView)

    app.router.add_view('/swarm/secrets/{secret_id}', configs_views.ConfigInspectView)

    # services
    app.router.add_view('/swarm/services', services_views.ServiceCollectionView)
    app.router.add_view('/swarm/services/inspect', services_views.ServiceCollectionInspectView)
    app.router.add_view('/swarm/services/create', services_views.ServiceCreateView)

    app.router.add_view('/swarm/services/{service_id}', services_views.ServiceInspectView)
    app.router.add_view('/swarm/services/{service_id}/logs', services_views.ServiceLogsView)

    # tasks
    app.router.add_view('/swarm/tasks', tasks_views.TaskCollectionView)
    app.router.add_view('/swarm/tasks/inspect', tasks_views.TaskCollectionInspectView)

    app.router.add_view('/swarm/tasks/{task_id}', tasks_views.TaskInspectView)
    app.router.add_view('/swarm/tasks/{task_id}/logs', tasks_views.TaskLogsView)

    # nodes
    app.router.add_view('/swarm/nodes', nodes_views.NodeCollectionView)
    app.router.add_view('/swarm/nodes/inspect', nodes_views.NodeCollectionInspectView)

    app.router.add_view('/swarm/nodes/{node_id}', nodes_views.NodeInspectView)
    app.router.add_view('/swarm/nodes/{node_id}/update', nodes_views.NodeUpdateView)

    # swarm
    app.router.add_view('/swarm', swarm_views.SwarmInspectView)
    app.router.add_view('/swarm/init', swarm_views.SwarmInitView)
    app.router.add_view('/swarm/join', swarm_views.SwarmJoinView)
    app.router.add_view('/swarm/leave', swarm_views.SwarmLeaveView)
    app.router.add_view('/swarm/update', swarm_views.SwarmUpdateView)
