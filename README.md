# Celery in a Flask Application Factory

### Introduction

This repo demonstrates configuring the Celery task queue with Flask in the [application factory pattern](http://flask.pocoo.org/docs/0.12/patterns/appfactories/).


The Flask application factory pattern delays configuration until the WSGI server is started, which allows for secure, dynamic configuration files. The official Celery tutorials assume all configuration is available upon import, so this sample Flask server shows how to configure Celery in a factory pattern.

Specifically, this example provides:
- support for late binding of the Broker URL
- executing all celery tasks within an [app context](http://flask.pocoo.org/docs/0.12/patterns/celery/#configuring-celery)

### Implementation details

This sample aims to simulate a realistic Flask server by employing [Blueprints](http://flask.pocoo.org/docs/0.12/blueprints/) and separate files for view functions and celery task definitions.

The repo is organized as follows:
- `server/` is the app
  - `server/core.py` creates the application factory
  - `server/controller/routes.py` defines the endpoints
  - `server/controller/tasks.py` defines Celery tasks
- `cli.py` is a cli interface for starting the Flask app in debug mode
- `celery_worker.py` is the entrypoint for the Celery worker
- `requirements.txt` is the list of python dependencies for pip
- `docker.env` defines the environment variables for the app
- `docker-compose.yml` defines the services
- `Dockerfile` is the image for the app & celery worker

The Flask app exposes an API that accepts a `POST` request to `/sleep/<seconds>` to start an task and return its ID. To check on the status of that task, issue a `GET` request to `/sleep/<task_id>`. The featured task is a dummy function that sleeps for `<seconds>` time then returns a datetime.

Per the recommendations of Celery documentation, this Flask/Celery app was tested with RabbitMQ as the message broker and Redis as the results backend, although (in theory) it should accept any [supported](http://docs.celeryproject.org/en/latest/getting-started/brokers/index.html#broker-overview) broker/backend.

This sample runs the services as Docker containers (see [./docker-compose.yml](./docker-compose.yml)), but feel free to run locally or in the cloud if it is more convenient for your use case - just make sure you modify your URL's in the configuration file accordingly.

### Configuration

This Flask server accepts configuration as environment variables, which are set by default in the file [./docker.env](./docker.env).

Configuration:
- `FLASK_PORT` is the port that flask will listen to
- `CELERY_BROKER_URL` is the rabbitmq URL
- `CELERY_RESULT_BACKEND` is the redis URL

### Running the services

You can run this example by starting starting the services with `docker-compose`.

Pull and build all images:
```sh
docker-compose build
```

Start all the containers in the background
```sh
docker-compose up -d
```

To check on the state of the containers, run:
```sh
docker-compose ps
```

Observe the API and celery worker logs:
```sh
docker-compose logs -f api worker
```

Create a single 30-second `sleep` task
```sh
curl -X POST http://localhost:8080/sleep/30
```

Above command will return a `<task_id>`, which can be used to check on the status of that task:
```sh
curl -X GET localhost:8080/sleep/<task_id>
```

### Cleanup

You can bring down all containers in this sample app with:
```sh
docker-compose down
```

To make sure they're gone, check with `docker-compose ps`
