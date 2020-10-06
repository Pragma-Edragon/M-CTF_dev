from flask import Flask
from app.config import Config
from app.blueprints.levels.levels_bp import levels_bp
from app.blueprints.users.users import cookie_bp

app = Flask(__name__, static_folder='static', template_folder='templates')

app.config.from_object(Config)
app.register_blueprint(levels_bp)
app.register_blueprint(cookie_bp)
