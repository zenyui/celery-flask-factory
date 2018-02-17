import os
import logging
import yaml
from flask import Flask
from server.controller import routes, tasks, celery

logger = logging.getLogger()

def create_app(debug=False):
    return entrypoint(debug=debug, mode='app')

def create_celery(debug=False):
    return entrypoint(debug=debug, mode='celery')

def entrypoint(debug=False, mode='app'):
    assert mode in ('app','celery'), 'bad mode "{}"'.format(mode)

    app = Flask(__name__)

    app.debug = debug

    configure_app(app)
    configure_logging(debug=debug)
    configure_celery(app, tasks.celery)

    app.register_blueprint(routes.bp, url_prefix='')

    if mode=='app':
        return app
    elif mode=='celery':
        return celery

def configure_app(app):
    
    logger.info('configuring flask app')

    if not os.environ.get('FUNNEL_API_CONFIG'):
        config_fp = './secrets/api-config-dev.yaml'
    else:
        config_fp = os.environ.get('FUNNEL_API_CONFIG')

    assert os.path.exists(config_fp), '"{}" not found'.format(config_fp)
    logger.info('reading config\n{}'.format(config_fp))

    with open(config_fp, 'r') as f:
        conf_obj = yaml.load(f)

    # app.config['SQLALCHEMY_DATABASE_URI'] = conf_obj['sqlalchemy']['database_uri']
    app.config['CELERY_BROKER_URL'] = conf_obj['celery']['broker_url']
    app.config['CELERY_RESULT_BACKEND'] = conf_obj['celery']['result_backend']

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
