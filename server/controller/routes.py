import logging
from flask import Flask, jsonify, Blueprint
from server.controller import tasks

bp = Blueprint('tasks', __name__)
logger = logging.getLogger()

@bp.route('/')
def view_base():
    return jsonify({'status': 'success'})

@bp.route('/ping')
def view_ping():
    return jsonify({'status': 'success', 'type': 'ping'})

@bp.route('/healthy')
def view_healthy():
    logger.info('running health check')
    return jsonify({'status': 'healthy', 'type': 'health_check'})

@bp.route('/testcontext/', methods=['POST'])
def view_test_context():
    task = tasks.test_flask_context.apply_async()
    return jsonify({'task_id': task.id})

@bp.route('/testcontext/<task_id>', methods=['GET'])
def view_check_context(task_id):
    task = tasks.test_flask_context.AsyncResult(task_id)
    output = {'task_id': task.id, 'state': task.state}
    if task.state == 'SUCCESS':
        output.update({'result': task.result})
    return jsonify(output)

@bp.route('/task/', methods=['POST'])
def view_start_task():
    # task = tasks.sample_task.delay(1,2)
    # task = tasks.sample_task.apply_async(args=[1,2])
    logger.info('start task...')
    task = tasks.make_json.apply_async()

    logger.info('return task...')
    return jsonify({
        'task_id': task.id,
        'state': task.state
    }), 202

@bp.route('/task/<task_id>', methods=['GET'])
@bp.route('/task/<task_id>/<int:page>', methods=['GET'])
def view_check_task(task_id, page=1):
    task = tasks.make_json.AsyncResult(task_id)

    if task.state in ('SUCCESS','CACHING'):
        assert task.result['maxpage'] >= page, 'exceeded max page'

        if task.result['loaded_page'] < page:
            return jsonify({
                'task_id': task.id,
                'state': task.state,
                'loaded_page': task.result['loaded_page'],
                'result': 'LOADING'
            })

        data = tasks.get_task_result(task_id, page)

        return jsonify({
            'task_id': task.id,
            'state': task.state,
            'result': task.result,
            'page': page,
            'data': data,
        })

    return jsonify({
        'task_id': task.id,
        'state': task.state,
        'result': task.result,
    })
