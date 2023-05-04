from rssh_server.views import get_resource, post_resource, ws_resource, delete_resource


def setup_routes(rserver):
    rserver.add_callback('GET', '/get_resource', get_resource)
    rserver.add_callback('POST', '/post_resource', post_resource)
    rserver.add_callback('DELETE', '/delete_resource', delete_resource)
    rserver.add_callback('STREAM', '/ws_resource', ws_resource)
