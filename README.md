# Lib-manager Docker image

This is a private docker image tended to be use as an interface to database docker image.
It is used with maekind/file-observer and webserver docker images.

This is part of a personal develop for a media server.
The lib-manager is the backend ot interface the frontend application with the database.

## Initial setup

The first time the user enters in to the application the initial setup process is launched.
When initial setup is completed, the lib-manager launches a file scanning in to the configured folder, retrives information for each music file from The audio DB (or Spotify if the user credentials have been configured) and saves it in to the database.


## Download

You can download this image by executing the code below:

	docker pull maekind/lib-manager:latest
    
## Usage

Lib-manager docker image launches a python flask application that is listens for file system change events from File-observer image and requests from webserver to access database information.

### Arguments

	- -a, --address: Webservice host address or FQDN.
	- -o, --port: Webservice port.
	- -f, --fresh-db: Set to True to erase database content at initialization a begin with a fresh database instance.

### Running the docker

	$> docker run -ti maekind/lib-manager:latest -a "http://<your_ip_address_or_fqdn>" -o <port> -f True

## Credits

2021 Copyright to Marco Espinosa. 

Say hello!: [hi@marcoespinosa.es](mailto:hi@marcoespinosa.es)
