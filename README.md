# Redirect Domain Service

Redirect service allows the configuration of “domain pools” which define the target
domains to redirect to, and weight associated with each domain. 

The redirect endpoint (http://localhost:8006//v1/redirect_domain/{pool_id}) chooses a random domain of the given pool based on its weight and forces an HTTP redirect to it;
Configuration can be done by using the [service OpenAPI page](http://localhost:8006/v1/docs).
Any custom UI is out of scope.

## Tech Stack

- Docker
- FastAPI
- MySQL
- SQLAlchemy

---

## Setup development environment (Docker compose)

Please install [`Docker` and `Docker compose`](https://www.docker.com/) first.

## Manual setup

After installation, run the following command to create a local Docker container.

```sh
docker-compose up --build
```

If Docker is running successfully, the API and DB server will be launched as shown in the following:

- API server: http://localhost:8006
- API Docs: http://localhost:8006/v1/docs
- API ReDoc Docs: http://localhost:8006/v1/redoc
- DB server: http://localhost:3308

_Be careful, it won't work if the port is occupied by another application._

## Setup with the VS Code Dev Containers extension

The above setup can be used for development, but you can also setup dev env with using the [VS Code Dev Containers extension](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers).

- Install VS code and the [Dev Containers extension](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers).
- Run the `Dev Containers: Open Folder in Container...` command from the Command Palette or quick actions Status bar item, and select the project folder.
- Wait until the building of the application is finished, then access the application url

---

## Note

### How to enable Python code formatter (black) and linter (flake8) with VSCode extension

If you're [VS Code](https://code.visualstudio.com/) user, you can easily setup Python code formatter (black) and linter (flake8) by simply installing the extensions.

Automatic formatting settings have already been defined [`.vscode/settings.json`](./.vscode/settings.json).

Just install following:

- [Black Formatter](https://marketplace.visualstudio.com/items?itemName=ms-python.black-formatter)
- [Flake8](https://marketplace.visualstudio.com/items?itemName=ms-python.flake8)

If you are using the Dev Container, this configuration is already done in [the Dev Container settings](./.devcontainer/devcontainer.json), so you can skip it.

### How to check the DB tables in the container

Use following command to go inside of docker container:

```sh
docker-compose exec redirect_db sh
```

Then use `mysql` command to execute a query:

```sh
mysql -u appuser -p
mysql> USE redirect_app;
mysql> SHOW TABLES;
mysql> SELECT * FROM user;
```

Your initial MySQL password is defined in `mysql/local.env`.

To reinitialize the DB, remove the named volumes declared in the "volumes" section of the Compose file.

https://docs.docker.com/engine/reference/commandline/compose_down/

```sh
docker-compose down -v
```

### How to add a library

Python libraries used in this app are defined in `api/requirements.txt`.

Also you may want to add libraries such as requests, in which case follow these steps:

- Add the library to requirements.txt

e.g., if you want to add `requests`:

```
requests==2.32.3
```

Then try a re-build and see.

```sh
docker-compose down; docker-compose build; docker-compose up;
```

### Environment variable

Some environment variables, like a database name and user are defined in `docker-compose.yml` or `Dockerfile`.

Then, run `docker-compose up` to launch the development environment.  
And confirm that your DB changes are reflected.


## How to use the App

![services](https://github.com/edisnake/redirect-service/assets/1470750/6419ba70-b4ca-4158-b0a9-b606d51caaa2)

- Create the pools and domains by using the OpenAPI helper page:
    http://localhost:8006/v1/docs#/Pools/create_pool_resource_v1_pools_post

    You can use this sample payload:
    ```json
    {
      "name": "First Pool",
      "domains": [
        {
          "domain": "http://abc.com",
          "weight": 2
        }, 
        {
          "domain": "http://xyz.com",
          "weight": 6
        },
        {
          "domain": "http://google.com",
          "weight": 8
        }
      ]
    }
    ```
- Confirm the pool and domains were created by using http://localhost:8006/v1/docs#/Pools/get_pools_resource_v1_pools_get
- Once the pools and domains are created you can use the redirect service with the pool id like this:
http://localhost:8006/v1/redirect_domain/1 which will redirect you using the logic in the [service description](#redirect-domain-service).
- Logs for database statements as well as requests and responses are saved into the database thorough a middleware and a logger handler,
you can review them in http://localhost:8006/v1/docs#/Logs/get_logs_resource_v1_logs_get

