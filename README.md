# Dockpier-apy
Dockpier-apy is a personal project to study Docker Container and API usage.
This repository is the backend python component for the main project Dockpier (https://github.com/tduval/Dockpier/)

## Components
Dockpier-apy is composed by the file *app.py* with the following Python modules:
- *Flask*
⋅⋅⋅Main Python frameworks for lightweight web API
- *Flask-Restful*
⋅⋅⋅Extension of Flask by providing native method and routing for advanced HTTP based requests
- *Flask-CORS*
⋅⋅⋅Extension of Flask by providing CORS (Cross-Origin Resource Sharing)
- *Docker-py*
⋅⋅⋅Python wrapper for Docker library

## Try it with Docker
This app is available on Community Docker Hub at the following URL https://hub.docker.com/r/tduval/dockpier/
Launch the container on a Manager Docker node with the following command :
```
docker run -dti --name dockpier-apy -p 5000:5000 -v /var/run/docker.sock:/var/run/docker.sock tduval/dockpier-apy:latest
```
**_WARNING : Deprecated Docker Container_**
