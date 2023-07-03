from flask import Flask, jsonify
from src.config import Config
from src.user.route import user
from src.cohort.route import cohort
from src.user_cohort.route import user_cohort
from src.database import db
from src.utils.error_handel import TaskException

def create_app():

    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)

    app.register_blueprint(user)
    app.register_blueprint(cohort)
    app.register_blueprint(user_cohort)

    @app.errorhandler(TaskException)
    def invalide_api_usage(e):
        return jsonify(e.to_dict())

    return app

main_app = create_app()


