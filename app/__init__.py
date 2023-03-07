# Importē bibliotēkas
import os
from flask import Flask, redirect, url_for
from flask_bootstrap import Bootstrap

# Importē nepieciešamos python moduļu failus
from . import auth, dashboard, db

# Funkcija, kas izveido Flask objektu un nokonfigurē visu nepieciešamo
def create_app():
    app = Flask(__name__, instance_relative_config=True)
    bootstrap = Bootstrap(app)

    app.static_folder = "static"
    # Datubāzes iestatījumi
    app.config.from_mapping(
        SECRET_KEY='jSoNxYNvHIRBsBTp7tBeTMsVd6XWIE8Y',
        DATABASE=os.path.join(app.instance_path, 'financebuddy.sqlite'),
    )
    # Izveido nepieciešamo failu uzbūves struktūru
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    
    # Flask applikācijai piesaista attiecīgos blueprints,
    # ko izmanto priekš individuālo lapu identifikācijas un kopīgām funkcijām    
    app.register_blueprint(auth.bp)
    app.register_blueprint(dashboard.bp)
    
    # Izveido datubāzi
    db.init_app(app)

    # Piesaista default saiti login lapai
    @app.route("/")
    def index():
        return redirect(url_for("auth.login"))
    
    # Atgriež Flask objektu
    return app

# App mainīgais ir Flask applikācijas objekts
app = create_app()
