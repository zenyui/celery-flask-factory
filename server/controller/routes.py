import logging
from flask import Flask, jsonify, Blueprint
from server.controller import tasks

bp = Blueprint('tasks', __name__)
logger = logging.getLogger()

@bp.route('/')
def view_base():
    return jsonify({'status': 'success'})

@bp.route('/sleep/', methods=['POST'])
@bp.route('/sleep/<int:sleep_time>', methods=['POST'])
def view_start_task(sleep_time=5):
    '''start task, return task_id'''

    logger.info('start task...')
    task = tasks.wait_task.apply_async(kwargs={'sleep_time':sleep_time})

    logger.info('return task...')
    return jsonify({
        'task_id': task.id,
        'state': task.state,
        'sleep_time': sleep_time
    }), 202

@bp.route('/sleep/<task_id>', methods=['GET'])
def view_check_task(task_id):
    '''return task state'''

    task = tasks.wait_task.AsyncResult(task_id)
    output = {'task_id': task.id, 'state': task.state}
    if task.state == 'SUCCESS':
        output.update({'result': task.result})
    return jsonify(output)
