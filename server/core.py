import os
import logging
from flask import Flask
from server.controller import routes, tasks, celery

logger = logging.getLogger()

def create_app(debug=False):
    return entrypoint(debug=debug, mode='app')

def create_celery(debug=False):
    return entrypoint(debug=debug, mode='celery')

def entrypoint(debug=False, mode='app'):
    assert isinstance(mode, str), 'bad mode type "{}"'.format(type(mode))
    assert mode in ('app','celery'), 'bad mode "{}"'.format(mode)

    app = Flask(__name__)

    app.debug = debug

    configure_app(app)
    configure_logging(debug=debug)
    configure_celery(app, tasks.celery)

    # register blueprints
    app.register_blueprint(routes.bp, url_prefix='')

    if mode=='app':
        return app
    elif mode=='celery':
        return celery

def configure_app(app):

    logger.info('configuring flask app')

    app.secret_key = os.environ.get('FLASK_SECRET_KEY')
    app.config['FLASK_PORT'] = os.environ.get('FLASK_PORT')
    app.config['CELERY_BROKER_URL'] = os.environ.get('CELERY_BROKER_URL')
    app.config['CELERY_RESULT_BACKEND'] = os.environ.get('CELERY_RESULT_BACKEND')

def configure_celery(app, celery):

    # set broker url and result backend from app config
    celery.conf.broker_url = app.config['CELERY_BROKER_URL']
    celery.conf.result_backend = app.config['CELERY_RESULT_BACKEND']

    # subclass task base for app context
    # http://flask.pocoo.org/docs/0.12/patterns/celery/
    TaskBase = celery.Task
    class AppContextTask(TaskBase):
        abstract = True
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)
    celery.Task = AppContextTask

    # run finalize to process decorated tasks
    celery.finalize()

def configure_logging(debug=False):

    root = logging.getLogger()
    h = logging.StreamHandler()
    fmt = logging.Formatter(
        fmt='%(asctime)s %(levelname)s (%(name)s) %(message)s',
        datefmt='%Y-%m-%dT%H:%M:%S'
    )
    h.setFormatter(fmt)

    root.addHandler(h)

    if debug:
        root.setLevel(logging.DEBUG)
    else:
        root.setLevel(logging.INFO)
