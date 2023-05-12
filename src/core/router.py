from aiohttp import web

from docker.router import setup_routes as setup_docker_routes
from swarm.router import setup_routes as setup_swarm_routes
from report.router import setup_routes as setup_report_routes
from agent.router import setup_routes as setup_agent_routes


def init_routes(application: web.Application) -> None:
    setup_docker_routes(application)
    setup_swarm_routes(application)
    setup_report_routes(application)
    setup_agent_routes(application)
