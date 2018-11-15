# app.py - a minimal flask api using flask_restful
from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from flask_cors import CORS
from docker.errors import APIError
import docker
import logging

app = Flask(__name__)
api = Api(app)
CORS(app, resources={r"/*": {"origins": "*"}})

parser = reqparse.RequestParser()

class Index(Resource):
    def get(self):
        return "Index page"

class Sys_Info(Resource):
    def get(self):
        return client.info()

class Sys_Version(Resource):
    def get(self):
        return client.version()

class Sys_Df(Resource):
    def get(self):
        return client.df()

class Sys_Events(Resource):
    def get(self):
        return client.events()

## Image Section ##
class Images(Resource):
    def get(self):
        imagetable = []
        for image in client.images.list():
            imagetable.append(image.attrs)
        return imagetable

    def post(self):
        parser.add_argument('name', help='Package name')
        parser.add_argument('tag', help='Package Tag/Version')
        args = parser.parse_args()
        if args.tag == "":
            args.tag="latest"
        img = client.images.pull(args.name, args.tag)
        return img.attrs, 201

class Image(Resource):
    def get(self, image_id):
        return client.images.get(image_id).attrs

    def delete(self, image_id):
        delImg = 0
        try:
            delImg = client.images.remove(image_id)
        except APIError as err:
            app.logger.info('Delete Image : %s', err.__str__)
            return err.__str__, err.response.status_code
        return delImg, 204

class ImageHistory(Resource):
    def get(self, image_id):
        return client.images.get(image_id).history()

class ImageTag(Resource):
    def post(self, image_id):
        parser.add_argument('repository', help='Repository name')
        parser.add_argument('tag', help='tag name')
        args = parser.parse_args()
        img = client.images.get(image_id).tag(args.repository, args.tag)
        return img, 201

class ImageSearch(Resource):
    def post(self):
        parser.add_argument('name', help='Package name')
        args = parser.parse_args()
        img = client.images.serch(args.name)
        return img, 201

## Container Section ##
class Containers(Resource):
    def get(self):
        containertable = []
        for container in client.containers.list(all=True):
            containertable.append(container.attrs)
        return containertable

class Container(Resource):
    def get(self, container_id):
        return client.containers.get(container_id).attrs

    def delete(self, container_id):
        return client.containers.remove(container_id), 204

class ContainerStatus(Resource):
    def get(self, container_id):
        return client.containers.get(container_id).status

    def put(self, container_id):
        parser.add_argument('status', help='actions type')
        args = parser.parse_args()
        container = client.containers.get(container_id)
        if args.status == "start":
            return container.start(), 201
        elif args.status == "restart":
            return container.restart(), 201
        elif args.status == "stop":
            return container.stop(), 201
        elif args.status == "pause":
            return container.pause(), 201
        elif args.status == "unpause":
            return container.unpause(), 201
        else:
            return False, 400

class ContainerLogs(Resource):
    def get(self, container_id):
        return client.containers.get(container_id).logs()

## Networks Section ##
class Networks(Resource):
    def get(self):
        networktable = []
        for network in client.networks.list():
            networktable.append(network.attrs)
        return networktable

class Network(Resource):
    def get(self, net_id):
        return client.networks.get(net_id)

    def delete(self, net_id):
        return client.networks.remove(net_id), 204

## Volumes Section ##
class Volumes(Resource):
    def get(self):
        volumetable = []
        for volume in client.volumes.list():
            volumetable.append(volume.attrs)
        return volumetable

class Volume(Resource):
    def get(self, vol_id):
        return client.volumes.get(vol_id)

    def delete(self, vol_id):
        return client.volumes.remove(vol_id), 204


client = docker.from_env()
api.add_resource(Index, '/')

api.add_resource(Sys_Info, '/system/info')
api.add_resource(Sys_Version, '/system/version')
api.add_resource(Sys_Df, '/system/df')
api.add_resource(Sys_Events, '/system/events')

api.add_resource(Images, '/images')
api.add_resource(Image, '/images/<image_id>')
api.add_resource(ImageHistory, '/images/<image_id>/history')
api.add_resource(ImageTag, '/images/<image_id>/tag')
api.add_resource(ImageSearch, '/images/search')

api.add_resource(Containers, '/containers')
api.add_resource(Container, '/containers/<container_id>')
api.add_resource(ContainerStatus, '/containers/<container_id>/status')
api.add_resource(ContainerLogs, '/containers/<container_id>/logs')

api.add_resource(Networks, '/networks')
api.add_resource(Network, '/networks/<net_id>')

api.add_resource(Volumes, '/volumes')
api.add_resource(Volume, '/volumes/<vol_id>')

if __name__ == '__main__':
    print("############ Docker docking status ############")
    print("Docker Initialized and Connected ? " + str(client.ping()))
    print("###############################################")
    app.run(debug=True, host='0.0.0.0')
