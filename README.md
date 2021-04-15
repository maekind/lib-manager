# Lib-manager Docker image

This is a private image tended to be use as an interface to database docker image.
It is used with maekind/file-observer and webserver docker images.

## Download

You can download this image by executing the code below:

	docker pull maekind/lib-manager:latest
    
## Usage

Lib-manager docker image launches a python flask application that is listens for file system change events from File-observer image and requests from webserver to access database information.

### Arguments

	- -a, --address: Webservice host address or FQDN.
	- -o, --port: Webservice port.

### Running the docker

	$> docker run -ti maekind/lib-manager:latest -a "http://<your_ip_address_or_fqdn>" -o <port>

## Credits

2021 Copyright to Marco Espinosa. 

Say hello!: [hi@marcoespinosa.es](mailto:hi@marcoespinosa.es)
