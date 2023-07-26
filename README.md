![Image alt](https://github.com/paraleipsis/repo_images/raw/main/hivecore/7.png)

## Overview

Hivecore Agent provides an API for almost complete coverage of Docker and Swarm APIs on the local host. Access to the Hivecore API server is made via the [Rest Reverse SSH](https://github.com/paraleipsis/rrssh) proxy service. Built using Aiohttp, Pydantic, AsyncSSH.

## Installation

- Install Docker
- Install [Hivecore API server](https://github.com/paraleipsis/hivecore) on manager host
- Clone this repository and navigate to it:
  
```bash
git clone https://github.com/paraleipsis/hivecore-agent.git && cd hivecore-agent
```

- Configure host credentials with UUID and JWT token generated on server:

```bash
nano configs/agent_config.yml
```

### Docker

- Deploy agent with Docker and change second -v option to your local configs path:

```bash
docker run -d \
    -p 8080:8080 \
    -v /var/run/docker.sock:/var/run/docker.sock \
    -v /hivecore-agent/configs:/hivecore-agent/configs \
    --name hivecore-agent \
    --restart unless-stopped \
    paraleipsis/hivecore-agent \
    python3 src/core/hivecore_agent.py 
```

### Swarm

- Deploy agents stack in existing Swarm cluster and change configs path:

```bash
docker service create -d \
    -p 8080:8080 \
    --mount=type=bind,src=/var/run/docker.sock,dst=/var/run/docker.sock \
    --mount=type=bind,src=/hivecore-agent/configs,dst=/hivecore-agent/configs \
    --name hivecore-agent \
    --mode global \
    paraleipsis/hivecore-agent \
    python3 src/core/hivecore_agent.py 
```

### Stack

Deploy with stack file:

```bash
docker stack deploy -c stack.yml hivecore-agent
```

Hivecore agent by default expose port 8080 which provides API access for local control.

## Configuration 

All configs located in /configs yaml files

If you do not need to connect to the server and you just want to have access to local control over the agent, set the False flag for RRSSH_PROXY in the configs/server_config.yml.

Logger config located in src/logger/config.yml
