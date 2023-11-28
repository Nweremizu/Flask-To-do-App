from flask_login import UserMixin
from app import db, login_manager


class User(UserMixin, db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    email = db.Column(db.String(30), unique=True)
    password = db.Column(db.String(100))
    img = db.Column(db.LargeBinary)
    tasks = db.relationship('Task', backref='user', lazy=True)


class Task(db.Model):
    __tablename__ = 'tasks'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150))
    description = db.Column(db.String(200))
    due_date = db.Column(db.Date)
    completed = db.Column(db.Boolean, default=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', name='fk_task_user'), nullable=False)
    label_id = db.Column(db.Integer, db.ForeignKey('label.id', name='fk_task_label'), nullable=False)


class Label(db.Model):
    __tablename__ = 'label'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(140))
    task_id = db.relationship('Task', backref='label', lazy=True)


@login_manager.user_loader
def user_loader(id):
    return User.query.filter_by(id=id).first()