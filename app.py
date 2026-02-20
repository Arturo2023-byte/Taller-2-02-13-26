import os
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from config import config

db = SQLAlchemy()

def create_app(config_name=None):
    app = Flask(__name__)

    # Config
    if config_name is None:
        config_name = os.environ.get("FLASK_ENV", "default")

    app.config.from_object(config[config_name])

    # Extensiones
    db.init_app(app)

    # Rutas / controladores
    from controllers.task_controller import register_routes
    register_routes(app)

    # Error handler 404 (DENTRO de create_app)
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template("404.html"), 404

    # Crear tablas
    with app.app_context():
        db.create_all()

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(host="127.0.0.1", port=5000, debug=True)