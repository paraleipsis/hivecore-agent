import docker
from io import BytesIO
from docker.errors import ImageNotFound


class DockerStuff:
    def __init__(self):
        self.client = docker.APIClient()

    def docker_get_stuff(self):
        if self.client.info()['Swarm']['ControlAvailable']:
            get_docker = {
                '/images': [self.client.inspect_image(i) for i in self.client.images()],
                '/containers': [self.client.inspect_container(i) for i in self.client.containers(all=True)],
                '/networks': [self.client.inspect_network(i) for i in self.client.networks()],
                '/volumes': [self.client.inspect_volume(i['Name']) for i in self.client.volumes()['Volumes']],
                '/services': [self.client.inspect_service(i) for i in self.client.services()],
                '/nodes': [self.client.inspect_node(i) for i in self.client.nodes()],
                '/swarm': self.client.inspect_swarm(),
                '/status': self.client.info(),
                '/configs': [self.client.inspect_config(i) for i in self.client.configs()],
                '/secrets': [self.client.inspect_secret(i) for i in self.client.secrets()],
            }
        else:
            get_docker = {
                '/images': [self.client.inspect_image(i) for i in self.client.images()],
                '/containers': [self.client.inspect_container(i) for i in self.client.containers(all=True)],
                '/networks': [self.client.inspect_network(i) for i in self.client.networks()],
                '/volumes': [self.client.inspect_volume(i['Name']) for i in self.client.volumes()['Volumes']],
                '/status': self.client.info(),
            }

        self.client.close()
        return get_docker

    def image_pull(self, image):
        self.client.pull(image)
        self.client.close()

    def image_build(self, fileobj, **kwargs):
        f = BytesIO(fileobj.encode('utf-8'))
        response = [line for line in self.client.build(fileobj=f, rm=True, **kwargs)]
        self.client.close()

    def create_container(self, **kwargs):
        """
        container will not run if image does not exist on local machine,
        so use try/except and if it's ImageNotFound pull image and repeat
        """

        # if 'ports' in kwargs.keys():
        #     # example: 6000:6000, 6002 (there host port will be random)
        #     # 'xxxx:xxxx, xxxx:xxxx' to ['xxxx:xxxx', 'xxxx:xxxx']
        #     lst_of_ports = [i.split(':') for i in kwargs['ports'].split(',')]
        #     # ['xxxx:xxxx', 'xxxx:xxxx'] to [{xxxx:xxxx}, {xxxx:xxxx}]
        #     lst_of_dicts_of_ports = [{int(i[0]): int(i[1])} if len(i) > 1 else {int(i[0]): None} for i in lst_of_ports]
        #     # [{xxxx:xxxx}, {xxxx:xxxx}] to [xxxx, xxxx] of keys - ports to open inside container
        #     ports = [[int(k) for k in i][0] for i in lst_of_dicts_of_ports]
        #     # list of dicts to one dict
        #     port_bindings = {k: v for d in lst_of_dicts_of_ports for k, v in d.items()}
        #     kwargs['ports'] = ports
        #     kwargs['host_config'] = client.create_host_config(port_bindings=port_bindings)

        # # ls, /usr/bin/nginx -t
        # if 'command' in kwargs.keys():
        #     kwargs['command'] = [i.strip() for i in kwargs['command'].split(',')]

        # # /home/user1/:/mnt/vol2:rw, /var/www:/mnt/vol1:ro
        # if 'volumes' in kwargs.keys():
        #     lst_of_volumes = [i.split(':') for i in kwargs['volumes'].split(',')]
        #     lst_of_list_of_volumes = [[f'{i[0]}:{i[1]}:{i[2]}'] for i in lst_of_volumes]
        #     binds = [x.strip() for xs in lst_of_list_of_volumes for x in xs]
        #     volumes = [i[1] for i in lst_of_volumes]
        #     kwargs['volumes'] = volumes
        #     kwargs['host_config'] = client.create_host_config(binds=binds)

        net_dict = {}
        if 'network' in kwargs.keys():
            net_dict['net_id'] = kwargs.pop('network')

        if 'ipv4_address' in kwargs.keys():
            net_dict['ipv4_address'] = kwargs.pop('ipv4_address')

        print(kwargs)

        def docker_run():
            container = self.client.create_container(**kwargs, detach=True)
            if len(net_dict) > 0:
                self.client.connect_container_to_network(container['Id'], **net_dict)
            self.client.start(container=container.get('Id'))

        try:
            docker_run()
            self.client.close()
        except ImageNotFound:
            self.client.pull(kwargs['image'])
            docker_run()
            self.client.close()

    def create_network(self, **kwargs):
        self.client.create_network(**kwargs)
        self.client.close()

    def create_volume(self, **kwargs):
        self.client.create_volume(**kwargs)
        self.client.close()

    def create_config(self, **kwargs):
        f = bytes(kwargs.pop('data'), encoding='utf-8')
        self.client.create_config(data=f, **kwargs)
        self.client.close()

    def create_secret(self, **kwargs):
        f = bytes(kwargs.pop('data'), encoding='utf-8')
        self.client.create_secret(data=f, **kwargs)
        self.client.close()

    def create_service(self, **kwargs):
        self.client.create_service(**kwargs)
        self.client.close()
