import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

from werkzeug.security import check_password_hash, generate_password_hash

from flaskr.db import get_db

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db
        error = None

        if not username:
            error = 'fill'
        elif not password:
            error = 'fill'

        if error is None:
            try:
                db.execute(
                    "INSERT INTO user (username, password) VALUES (?, ?)",
                    (username, generate_password_hash(password)), #escapes values to prevent SQLInjection
                )
            except db.IntegrityError: #Integrity error means some unique value already exists
                error = f"User {username} is already registered"
            else:
                return redirect(url_for("auth.login"))
            
        flash(error)

    return render_template('auth/register.html')

@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None 
        user = db.execute(
            'SELECT * FROM user WHERE username = ?', (username,)
        ).fetchone()

        if user is None:
            error = 'wrong username'
        elif not check_password_hash(user['password'], password):
            error = 'wrong password'

        if error is None:
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('index'))
        
        flash(error)

    return render_template('auth/login.html')

@bp.before_app_request
def load_logged_in_user():

    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = get_db.execute(
            'SELECT * FROM user where ID = ?', (user_id,)
        ).fetchone()

@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

