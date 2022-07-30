from http.server import HTTPServer, BaseHTTPRequestHandler
from http import HTTPStatus
import json
import time
import docker
import urllib.parse
from io import BytesIO
from docker.errors import ImageNotFound

client = docker.APIClient()


class DockerPost:
    # def __init__(self):
    #     self.client = docker.APIClient()

    @staticmethod
    def image_pull(image):
        client.pull(image)
        client.close()

    @staticmethod
    def image_build(fileobj, **kwargs):
        f = BytesIO(fileobj.encode('utf-8'))
        response = [line for line in client.build(fileobj=f, rm=True, **kwargs)]
        client.close()

    @staticmethod
    def create_container(**kwargs):
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
            container = client.create_container(**kwargs, detach=True)
            if len(net_dict) > 0:
                client.connect_container_to_network(container['Id'], **net_dict)
            client.start(container=container.get('Id'))

        try:
            docker_run()
            client.close()
        except ImageNotFound:
            client.pull(kwargs['image'])
            docker_run()
            client.close()

    @staticmethod
    def create_network(**kwargs):
        client.create_network(**kwargs)
        client.close()

    @staticmethod
    def create_volume(**kwargs):
        client.create_volume(**kwargs)
        client.close()

    @staticmethod
    def create_config(**kwargs):
        f = bytes(kwargs.pop('data'), encoding='utf-8')
        client.create_config(data=f, **kwargs)
        client.close()

    @staticmethod
    def create_secret(**kwargs):
        f = bytes(kwargs.pop('data'), encoding='utf-8')
        client.create_secret(data=f, **kwargs)
        client.close()

    @staticmethod
    def create_service(**kwargs):
        client.create_service(**kwargs)
        client.close()


class _RequestHandler(BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(HTTPStatus.OK)
        self.send_header('Content-type', 'application/json')
        # Allow requests from any origin, so CORS policies don't
        # prevent local development.
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()

    def do_GET(self):
        if client.info()['Swarm']['ControlAvailable']:
            get_docker = {
                '/images': [client.inspect_image(i) for i in client.images()],
                '/containers': [client.inspect_container(i) for i in client.containers(all=True)],
                '/networks': [client.inspect_network(i) for i in client.networks()],
                '/volumes': [client.inspect_volume(i['Name']) for i in client.volumes()['Volumes']],
                '/services': [client.inspect_service(i) for i in client.services()],
                '/nodes': [client.inspect_node(i) for i in client.nodes()],
                '/swarm': client.inspect_swarm(),
                '/status': client.info(),
                '/configs': [client.inspect_config(i) for i in client.configs()],
                '/secrets': [client.inspect_secret(i) for i in client.secrets()],
            }
        else:
            get_docker = {
                '/images': [client.inspect_image(i) for i in client.images()],
                '/containers': [client.inspect_container(i) for i in client.containers(all=True)],
                '/networks': [client.inspect_network(i) for i in client.networks()],
                '/volumes': [client.inspect_volume(i['Name']) for i in client.volumes()['Volumes']],
                '/status': client.info(),
            }

        self._set_headers()
        path = urllib.parse.urlparse(self.path)
        data = get_docker
        self.wfile.write(json.dumps(data).encode('utf-8'))

    def do_POST(self):
        data = []
        length = int(self.headers.get('content-length'))
        message = json.loads(self.rfile.read(length))
        message['date_ms'] = int(time.time()) * 1000
        data.append(message)
        # instance = DockerPost()
        method = getattr(DockerPost, data[0]['task'])
        method(**data[0]['params'])
        self._set_headers()
        self.wfile.write(json.dumps({'success': True}).encode('utf-8'))

    def do_OPTIONS(self):
        # Send allow-origin header for preflight POST XHRs.
        self.send_response(HTTPStatus.NO_CONTENT)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST')
        self.send_header('Access-Control-Allow-Headers', 'content-type')
        self.end_headers()


def run_server():
    server_address = ('', 8001)
    httpd = HTTPServer(server_address, _RequestHandler)
    print('serving at %s:%d' % server_address)
    httpd.serve_forever()


if __name__ == '__main__':
    run_server()
