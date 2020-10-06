import datetime
import random

from flask import Blueprint, redirect, url_for, render_template
from flask import session as flask_session

from app.blueprints.levels.fernet_crypto import decodeData
from app.crypt import encode_data
from app.database import *
from app.forms import AnswersForm

levels_bp = Blueprint('levels', __name__,
                      template_folder='templates')
flag = 'mctf{Y0U_4R3_B3TT3R_TH4N_G00GL3}'

init_db()

def check_for_cookie_expire(username: str) -> bool:
    """
    /* taking decoded login from user session (more secure then other variants)
    /* login encoded in Fernet (levels/fernet_crypto.py)
    /* if decoded login exists in database - parse time and compare with
    /* maximum cookie expire time (hardcoded)
    :param username:
    :return:
    """
    with session_scope() as session:
        user = session.query(Auth).filter_by(username=username).scalar()
        if user:
            if int(str(datetime.datetime.now().strftime("%H:%M:%S")).replace(':', '')) - int(
                    str(user.timestap).replace(':', '')) < 30:
                return True
    return False


def expire_cookie(username: str):
    # if cookie expired - deleting users row frow database
    with session_scope() as session:
        user = session.query(Auth).filter_by(username=username).scalar()
        if user:
            session.query(Auth).filter_by(username=username).delete()


def get_image_from_db(username: str):
    # getting all imgnums from database
    with session_scope() as session:
        imgdata = session.query(Auth).filter_by(username=username).scalar()
        if imgdata:
            return imgdata.imgnums


def insert_image_data(username: str, data: int):
    # inserting generated number if it's not already in database
    with session_scope() as session:
        update = session.query(Auth).filter_by(username=username).scalar()
        update.imgnums += str(data) + ','


def parse_db_image_last_number(username: str):
    # parsing last value of level numbers
    with session_scope() as session:
        parse = session.query(Auth).filter_by(username=username).scalar()
        if parse:
            data = str(parse.imgnums).split(',')
            return data[len(data) - 2]


def null_db_image_number(username: str):
    with session_scope() as session:
        nll = session.query(Auth).filter_by(username=username).scalar()
        if nll:
            if len(str(nll.imgnums).split(',')) >= 3:
                nll.imgnums = '0,'


def new_level_state(username: str):
    with session_scope() as session:
        state = session.query(Auth).filter_by(username=username).scalar()
        if state:
            state.level = int(state.level) + 1


def get_level(username: str):
    with session_scope() as session:
        level = session.query(Auth).filter_by(username=username).scalar()
        if level:
            return level.level


def generate_level(func):
    def wrapper(*args):
        return_value = func(*args)
        if return_value is not None and 'flag' not in flask_session.keys():
            return encode_data(return_value)
        else:
            return flask_session['flag']

    return wrapper


@generate_level
def levels_logic():
    random_int = random.randint(1, 7)
    while str(random_int) in str(get_image_from_db(decodeData(bytes(flask_session['uname'], 'utf')))).split(','):
        print(random_int)
        null_db_image_number(decodeData(bytes(flask_session['uname'], 'utf')))
        random_int = random.randint(1, 7)
    else:
        insert_image_data(decodeData(bytes(flask_session['uname'], 'utf')), random_int)
    print(parse_db_image_last_number(decodeData(bytes(flask_session['uname'], 'utf'))))
    with open(f"/app/app/task_images/img{random_int}.jpg", "rb") as file:
        data = file.read()
        file.close()
    return data or None


@levels_bp.before_request
def before_requests_check_cookie():
    """
    /* if cookie expires: cleaning session
    /* and redirecting to login form
    :return:
    """
    if 'uname' in flask_session.keys():
        if not check_for_cookie_expire(decodeData(bytes(flask_session['uname'], 'utf'))):
            expire_cookie(decodeData(bytes(flask_session['uname'], 'utf')))
            flask_session.clear()
    if 'uname' not in flask_session.keys():
        return redirect(url_for('cookie.login'))
    if get_level(decodeData(bytes(flask_session['uname'], 'utf'))) == 6:
        if flag not in flask_session.keys():
            flask_session['flag'] = flag


@levels_bp.route('/levels/<int:level_id>', methods=['GET', 'POST'])
def levels(level_id):
    form = AnswersForm()
    answers_dict = {
        'img1.jpg': 'lina dota 2',
        'img2.jpg': 'hack the box',
        'img3.jpg': 'codewars',
        'img4.jpg': 'last week',
        'img5.jpg': 'red flag',
        'img6.jpg' : 'leetcode',
        'img7.jpg' : 'rias gremory',
    }
    if level_id != get_level(decodeData(bytes(flask_session['uname'], 'utf'))):
        return redirect(url_for('levels.levels', level_id=get_level(decodeData(bytes(flask_session['uname'], 'utf')))))
    if form.validate_on_submit():
        if answers_dict[
            f"img{parse_db_image_last_number(decodeData(bytes(flask_session['uname'], 'utf')))}.jpg"] \
                == str(form.answer.data).lower():
            new_level_state(decodeData(bytes(flask_session['uname'], 'utf')))
        return redirect(url_for('levels.levels', level_id=get_level(decodeData(bytes(flask_session['uname'], 'utf')))))
    return render_template('levelstmp.html', keys=get_level(decodeData(bytes(flask_session['uname'], 'utf'))),
                           form=form, leveldata=levels_logic(), session=decodeData(bytes(flask_session['uname'], 'utf')))
