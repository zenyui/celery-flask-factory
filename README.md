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

The Flask app exposes an API that accepts a `POST` request to `/task/` to start an task and return its ID. To check on the status of that task, issue a `GET` request to `/task/<task_id>`. The featured task is a dummy function that sleeps 5 seconds then returns a datetime.

Per the recommendations of Celery documentation, this Flask/Celery app was tested with RabbitMQ as the message broker and Redis as the results backend, although (in theory) it should accept any [supported](http://docs.celeryproject.org/en/latest/getting-started/brokers/index.html#broker-overview) broker/backend.

### Configuration

This Flask server accepts configuration in a YAML/JSON file, which by default is located in `./secrets/api-config.yaml` (an excluded path in the `.gitignore`). This path can be manually overwritten by setting the environment variable `FLASK_CONFIG`.

Sample:
```yaml
port: 8080
secret_key: my_secret_key
celery:
  broker_url: amqp://localhost:5672
  result_backend: redis://localhost:6379
```

### Running the server

You can run this example by starting the message broker, celery worker, and flask app separately.

Make sure your broker and backend are running (Docker is a convenient way to get this running). The following examples use the alpine distribution of rabbitmq and redis and forwards their default ports to `localhost`.
```sh
docker run -d --hostname rabbit --name some-rabbit -p 5672:5672 rabbitmq:alpine
docker run -d --hostname redis --name some-redis -p 6379:6379 redis:alpine
```

Create a Python 3 environment and install dependencies:
```sh
virtualenv env -p `which python3`
. env/bin/activate
pip install -r ./requirements.txt
```

Then start your Celery worker in the new python environment by issuing:
```sh
. env/bin/activate
celery worker -A celery_worker.celery --loglevel=info
```

Finally, in a separate terminal, the Flask app can be started in debug mode with the supplied `cli.py`
```sh
. env/bin/activate
python ./cli.py
```

Once the broker, backend, Celery worker, and Flask server are all running, tasks can be started by issuing:
```sh
curl -X POST localhost:8080/task/
```

Above command will return a `<task_id>`, which can be used to check on the status of that task:
```sh
curl -X GET localhost:8080/task/<task_id>
```

### Cleanup

If you used the above commands to start docker containers for Rabbitmq and Redis, you can kill and delete them by issuing:
```sh
docker kill some-rabbit some-redis && \
docker rm some-rabbit some-redis
```

To make sure they're gone, check with `docker ps -a`
