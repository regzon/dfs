# Distributed File System

Innopolis Unversity, 2019 <br>
Distributed Systems <br>


## Team

Andrey Volkov <br>
Madina Gafarova <br>
Gleb Petrakov <br>


## Structure

### `client`

A simple Python package to perform operations to FS from user space.

#### Calls

Create a new instance of client with `Client(nameserver_addr)`, where `nameserver_addr` is nameserver ip address.

### `naming_server`

A Django server for managing storage nodes and to transit filesystem operations to storage servers.

Original Docker image: `regzon/dfs-naming-server`

Port: 6500

## Running

### Environment

Set up all environmental variables within `.env` file (example given).

Execute to export variables manually: <br>
`export $(grep -v '^#' .env | xargs)`


### Docker

Images: <br>

`regzon/dfs-naming-server` - naming server image.
`regzon/dfs-storage-server` - storage server image.

#### Build

To build specific image, run: <br>

`docker build -t <image_name>:<image_tag> ./<context>`

E. g.:
`docker build -t regzon/dfs-naming-server ./naming_server`

#### Run

Execute to run container:
`docker run -d -it --restart=always --name=<name> -p <port>:<port> <image>`


### Docker-Compose

Execute to build and run the whole system within docker-compose environment: <br>
`docker-compose up -d --build`

Execute to stop all containers: <br>
`docker-compose down -v`


### Docker Swarm

Initialize Swarm node: <br>
`docker swarm init --advertise-addr <ip_address>`

Clone this repo: <br>
`git clone https://github.com/regzon/dfs && cd dfs`

Execute to export variables for Docker Swarm: <br>
`export $(grep -v '^#' .env | xargs)`

Deploy stack: <br>
`docker stack deploy --compose-file docker-compose.yml dfs`

