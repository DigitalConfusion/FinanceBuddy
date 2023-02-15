import os

from flask import Flask, redirect, url_for
from flask_bootstrap import Bootstrap


def createApp(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    bootstrap = Bootstrap(app)

    app.static_folder = "static"
    app.config.from_mapping(
        SECRET_KEY='jSoNxYNvHIRBsBTp7tBeTMsVd6XWIE8Y',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from . import auth, dashboard
    app.register_blueprint(auth.bp)
    app.register_blueprint(dashboard.bp)
    
    from . import db
    db.init_app(app)

    @app.route("/")
    def index():
        return redirect(url_for("auth.login"))
    
    return app


app = createApp()
