import os

from config import Config, Disabled
from myTemplate import my_template
from flask import Flask, request, redirect, url_for, render_template_string, render_template, abort

app = Flask(__name__,
            template_folder='templates',
            static_folder='static')
app.config.from_object(Config)


@app.after_request
def make_header(response):
    response.headers['X-Forwarded-For'] = str(request.headers.getlist('X-Forwarded-For')[0]).split(',')[1]
    return response

@app.route('/')
def index_red():
    return redirect('/index')

@app.route('/<path:dir>')
@app.route('/index/<path:dir>')
def getfile(dir):
    check_dir = Disabled(str(dir))
    xff = str(request.headers.getlist('X-Forwarded-For')[0]).split(',')[1]
    check_xff = Disabled(xff)
    if (check_xff.abort_rq()):
        xff = str(request.headers.getlist('X-Forwarded-For')[0]).split(',')[len(xff)-1]
    if not (check_dir.check_blocked()):
        try:
            with open(os.path.join('/app/static', dir), 'r') as file:
                data = file.read()
                file.close()
            return data
        except FileNotFoundError:
            pass
        except PermissionError:
            pass
    return render_template_string(my_template(xff.replace('.', '')))
