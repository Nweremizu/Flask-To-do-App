from sqlalchemy import or_, and_
from app.home import blueprint
from app.authentication.models import Task, Label
from datetime import datetime
from app import db
from flask import render_template, request, jsonify, redirect, url_for
from flask_login import login_required, current_user


@blueprint.route('/today')
@login_required
def home():
    tasks = Task.query.filter(Task.user_id == current_user.id).filter(
        or_(Task.completed == False, Task.completed.is_(None))).all()
    labels = Label.query.all()

    return render_template('pages/index.html', tasks=tasks,
                           labels=labels)


@blueprint.route('/get_count')
@login_required
def get_count():
    tasks = Task.query.filter(Task.user_id == current_user.id).filter(
        or_(Task.completed == False, Task.completed.is_(None))).all()
    completed_tasks = Task.query.filter(Task.user_id == current_user.id).filter_by(completed=True).all()

    # get all label count with a for loop
    all_labels = []
    labels = Label.query.all()
    for label in labels:
        label_count = len(Task.query.filter(
            and_(Task.user_id == current_user.id, or_(Task.completed.is_(None), Task.completed == False))).filter_by(
            label_id=label.id).all())
        label_dict = {'name': label.name, 'count': label_count}
        all_labels.append(label_dict)

    completed_tasks_count = len(completed_tasks)
    task_count = len(tasks)
    return render_template('pages/count.html', labels=labels, task_count=task_count,
                           completed_tasks_count=completed_tasks_count, l_labels=all_labels)


@blueprint.route('/completed', )
@login_required
def completed():
    completed_tasks = Task.query.filter(Task.user_id == current_user.id).filter_by(completed=True).all()
    return render_template('pages/completed.html', completed_tasks=completed_tasks)


@blueprint.route('/new_completed_tasks', methods=['GET'])
@login_required
def new_completed():
    completed_tasks = Task.query.filter(Task.user_id == current_user.id).filter_by(completed=True).all()
    return render_template('pages/completed_templete.html', completed_tasks=completed_tasks)


@blueprint.route('/add_task', methods=['POST'])
@login_required
def add_task():
    if request.method == 'POST':
        task_name = request.form.get('add_task')

        task = Task(
            name=task_name,
            user_id=current_user.id,
            label_id=1
        )
        db.session.add(task)
        db.session.commit()

        tasks = Task.query.filter(Task.user_id == current_user.id).filter(
            or_(Task.completed == False, Task.completed.is_(None))).all()
        labels = Label.query.all()
        return render_template('pages/today_template.html', tasks=tasks, labels=labels)


@blueprint.route('/complete_task/<int:task_id>', methods=['POST'])
@login_required
def complete_task(task_id):
    if request.method == 'POST':
        task = Task.query.filter_by(id=task_id).first()
        if task is None:
            return jsonify({'message': 'Task not found'}), 404
        else:
            task.completed = True
            db.session.commit()
            return jsonify({'message': 'Task completed successfully'})


@blueprint.route('/update_task/<int:task_id>', methods=['POST'])
@login_required
def update_task(task_id):
    if request.method == 'POST':
        task = Task.query.filter_by(id=task_id).first()
        print(task.id)
        if task is None:
            return jsonify({'message': 'Task not found'}), 404
        else:
            task.name = request.form.get('task_name')
            task.description = request.form.get('task_des')
            label = request.form.get('label')
            task.label_id = int(label)
            task.due_date = datetime.strptime(str(request.form.get('due_date')), '%Y-%m-%d')
            db.session.commit()

            tasks = Task.query.filter(Task.user_id == current_user.id).filter(
                or_(Task.completed == False, Task.completed.is_(None))).all()
            labels = Label.query.all()
            return render_template('pages/today_template.html', tasks=tasks, labels=labels)


@blueprint.route('/delete_task/<int:task_id>', methods=['POST'])
@login_required
def delete_task(task_id):
    if request.method == 'POST':
        task = Task.query.filter_by(id=task_id).first()
        if task is None:
            return jsonify({'message': 'Task not found'}), 404
        else:
            db.session.delete(task)
            db.session.commit()
            return jsonify({'message': 'Task deleted successfully'})


# Restore Task to Be part of the current Day
@blueprint.route('/restore_task/<int:task_id>', methods=['POST'])
@login_required
def restore_task(task_id):
    if request.method == 'POST':
        task = Task.query.filter_by(id=task_id).first()
        if task is None:
            return jsonify({'message': 'Task not found'}), 404
        else:
            task.completed = False
            db.session.commit()
            return jsonify({'message': 'Task restored successfully'})


# Add Labels to the Database
@blueprint.route('/add_label', methods=['POST'])
@login_required
def add_label():
    if request.method == 'POST':
        name = request.form.get('add_label')
        label = Label.query.filter_by(name=name).first()
        if label:
            return redirect(url_for('blueprint.today'))
        else:
            label = Label(
                name=name
            )
            db.session.add(label)
            db.session.commit()
            return jsonify({'message': 'Label added successfully'})
