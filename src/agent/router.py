from agent.api.platforms import ActivePlatformsView


def setup_routes(app):
    # platforms
    app.router.add_view('/agent/platforms/active', ActivePlatformsView)
