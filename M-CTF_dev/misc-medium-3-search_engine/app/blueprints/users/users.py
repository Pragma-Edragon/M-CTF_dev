from flask import Blueprint, flash, redirect, render_template, url_for
from app.blueprints.levels.fernet_crypto import encodeData
from app.forms import LoginForm, RegForm
from flask import session as flask_session
from app.database import *
import datetime

cookie_bp = Blueprint('cookie', __name__,
                      template_folder='templates',
                      static_folder='static',
                      static_url_path='/static')
init_db()


def checkForExistence(username: str, password: str) -> bool:
    with session_scope() as session:
        user = session.query(Auth).filter_by(username=username).scalar()
        if user:
            if user.password == password and user.username == username:
                return True
    return False


def checkForReg(username: str) -> bool:
    with session_scope() as session:
        user = session.query(Auth).filter_by(username=username).scalar()
        if user:
            return True
    return False



@cookie_bp.route('/', methods=['GET', 'POST'])
def index_red():
    return redirect(url_for('cookie.register'))

@cookie_bp.route('/login', methods=['GET', 'POST'])
def login():
    """
    /* checking for user it database
    /* if in database - activating level status
    /* if not - error;
    /* If user already logged in -> redirect on level from database
    :return:
    """
    error = None
    form = LoginForm()
    if form.validate_on_submit():
        if not checkForExistence(form.username.data, form.password.data):
            error = "Can't find this data..."
        else:
            if form.username.data not in flask_session.keys():
                flask_session['uname'] = encodeData(form.username.data)
            return redirect(url_for("levels.levels", level_id=1))
    return render_template("login.html", title='Sign in', form=form, error=error)


@cookie_bp.route('/register', methods=['GET', 'POST'])
def register():
    """
    /* Inserting data in DB if not exists
    /* if exists - throwing error (not with flash)
    :return:
    """
    error = None
    form = RegForm()
    if form.validate_on_submit():
        if not checkForReg(form.username.data):
            with session_scope() as session:
                session.add(Auth(form.username.data, form.password.data, datetime.datetime.now().strftime("%H:%M:%S"), 0))
                flash("Successfully registered")
        else:
            error = "User already exists"
            print(error)
    return render_template("registration.html", title="Register", form=form, error=error)


@cookie_bp.route('/logout')
def logout():
    flask_session.clear()
    return redirect(url_for('cookie.register'))
