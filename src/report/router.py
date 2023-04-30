from report.api import host


def setup_routes(app):
    # snapshot
    app.router.add_view('/report/snapshot/docker', host.HostDockerSnapshotView)
