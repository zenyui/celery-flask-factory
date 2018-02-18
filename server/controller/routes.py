import logging
from flask import Flask, jsonify, Blueprint
from server.controller import tasks

bp = Blueprint('tasks', __name__)
logger = logging.getLogger()

@bp.route('/')
def view_base():
    return jsonify({'status': 'success'})

@bp.route('/task/', methods=['POST'])
def view_start_task():
    '''start task, return task_id'''
    
    logger.info('start task...')
    task = tasks.sample_task.apply_async()

    logger.info('return task...')
    return jsonify({
        'task_id': task.id,
        'state': task.state
    }), 202

@bp.route('/task/<task_id>', methods=['GET'])
def view_check_task():
    '''return task state'''

    task = tasks.test_flask_context.AsyncResult(task_id)
    output = {'task_id': task.id, 'state': task.state}
    if task.state == 'SUCCESS':
        output.update({'result': task.result})
    return jsonify(output)
