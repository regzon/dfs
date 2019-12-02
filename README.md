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

##### `init(self)`
Initialize a filesystem. Completely purge everything and retrieve all metadata.

##### `create_file(self, path)`
Create a new empty file with `path` on a storage server.

##### `read_file(self, path)`
Read existing file at `path` on a storage server.

##### `write_file(self, path, file)`
Write data of `file` on client machine to an existing file on `path` within server.

##### `delete_file(self, path)`
Delete existing file at `path` on a storage server.

##### `get_file_info(self, path)`
Get metadata of a file on `path`

##### `copy_file(self, source_path, destination_path)`
Copy existing file at `source_path` to `destination_path` on a storage server.

##### `read_dir(self, path)`
List directory contents at `path`.

##### `create_dir(self, path)`
Create an empty directory on storage server within `path`.

##### `delete_dir(self, path)`
Delete existing directory on storage server within `path`.


### `naming_server`

A Django server for managing storage nodes and to transit filesystem operations to storage servers.

Original Docker image: `regzon/dfs-naming-server`

#### Endpoints

Port: `80`

<<<<<<< HEAD
More precise documentation in 

=======
>>>>>>> origin/master
##### POST: `/init`
Initialize all connected storage servers.

##### POST: `/create_file`
Create a new empty file. <br>
<<<<<<< HEAD

##### GET: `/read_file`
Read existing file. <br>

##### POST: `/write_file`
Upload file to storage server. <br>

##### POST: `/delete_file`
Delete existing file from storage server. <br>

##### GET: `/get_file_info`
Get file service information. <br>

##### POST: `/copy_file`
Copy file to another path on storage server. <br>

##### GET: `/read_dir`
Get contents of a specific directory on a server. <br>

##### POST: `/create_dir`
Creates a new empty directory on a storage server. <br>

##### POST: `/delete_dir`
Removes existing directory on a storage server. <br>
=======
Params: <br>
` `:

##### GET: `/read_file`
Read existing file. <br>
Params: <br>
` `:

##### POST: `/write_file`
Upload file to storage server. <br>
Params: <br>
` `:

##### POST: `/delete_file`
Delete existing file from storage server. <br>
Params: <br>
` `:

##### GET: `/get_file_info`
Get file service information. <br>
Params: <br>
` `:

##### POST: `/copy_file`
Copy file to another path on storage server. <br>
Params: <br>
` `:

##### GET: `/read_dir`
Get contents of a specific directory on a server. <br>
Params: <br>
` `:

##### POST: `/create_dir`
Creates a new empty directory on a storage server. <br>
Params: <br>
` `:

##### POST: `/delete_dir`
Removes existing directory on a storage server. <br>
Params: <br>
` `:
>>>>>>> origin/master


### `storage_server`

A Flask application to perform operations on filesystem.

Original Docker image: `regzon/dfs-storage-server`

#### Endpoints

Port: `3000`

##### POST: `/initialize_root`
Copy file to another path on storage server. <br>
<<<<<<< HEAD

##### POST: `/create_file`
Get contents of a specific directory on a server. <br>

##### POST: `/upload_file`
Creates a new empty directory on a storage server. <br>

##### POST: `/download_file`
Removes existing directory on a storage server. <br>

##### POST: `/delete_file`
Removes existing directory on a storage server. <br>

##### POST: `/delete_dir`
Removes existing directory on a storage server. <br>

##### POST: `/transfer`
Removes existing directory on a storage server. <br>
=======
Params: <br>
` `:

##### POST: `/create_file`
Get contents of a specific directory on a server. <br>
Params: <br>
` `:

##### POST: `/upload_file`
Creates a new empty directory on a storage server. <br>
Params: <br>
` `:

##### POST: `/download_file`
Removes existing directory on a storage server. <br>
Params: <br>
` `:

##### POST: `/delete_file`
Removes existing directory on a storage server. <br>
Params: <br>
` `:

##### POST: `/delete_dir`
Removes existing directory on a storage server. <br>
Params: <br>
` `:


##### POST: `/transfer`
Removes existing directory on a storage server. <br>
Params: <br>
` `:

>>>>>>> origin/master


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


