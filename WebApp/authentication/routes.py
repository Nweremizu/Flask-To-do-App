from WebApp.authentication import blueprint
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from flask import render_template, request, redirect, url_for, flash, Response
from WebApp.authentication.models import User
from WebApp.authentication.util import create_image
from WebApp import login_manager, db
import os

# get the assets folder from the config file
ASSETS_ROOT = os.getenv('ASSETS_ROOT')


@blueprint.route('/')
def route_default():
    return redirect(url_for('auth_blueprint.login'))


@blueprint.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        # Locate User
        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(pwhash=user.password, password=password):
            login_user(user)
            return redirect(url_for('auth_blueprint.route_default'))

        flash('Wrong user or password')
        return render_template('accounts/login.html')

    if not current_user.is_authenticated:
        return render_template('accounts/login.html', )
    return redirect(url_for('home_blueprint.home'))


@blueprint.route('/get_image/<int:m_id>', methods=['GET'])
@login_required
def get_image(m_id):
    user = User.query.filter_by(id=m_id).first()
    if user:
        return Response(user.img, mimetype='image/png')


@blueprint.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        image = create_image(user_name=name)
        # Check if user exists
        user = User.query.filter_by(email=email).first()
        if user:
            flash('User already exists')
            return redirect(url_for('auth_blueprint.register'))

        if image is False:
            flash('Error, Try again later')
            return redirect(url_for('auth_blueprint.register'))
        # Create new user
        user = User(
            name=name,
            email=email,
            password=generate_password_hash(password=password, method='pbkdf2:sha256', salt_length=8),
            img=image
        )
        db.session.add(user)
        db.session.commit()
        login_user(user)
        return redirect(url_for('home_blueprint.home'))

    return render_template('accounts/register.html')


@blueprint.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth_blueprint.route_default'))


# Error Handlers
@login_manager.unauthorized_handler
def unauthorized_handler():
    return render_template('home/page-403.html'), 403


@blueprint.errorhandler(403)
def access_forbidden(error):
    return render_template('home/page-403.html'), 403


@blueprint.errorhandler(404)
def not_found_error(error):
    return render_template('home/page-404.html'), 404


@blueprint.errorhandler(500)
def internal_error(error):
    return render_template('home/page-500.html'), 500
