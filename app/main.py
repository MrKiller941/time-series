import swagger_schemas
from exceptions import (
    DatasetNotFoundError,
    EmptyFileError,
    FileExtensionError,
    NotTimeSeriesError,
    UserNotFoundError,
)
from flasgger import Swagger, swag_from
from flask import Flask
from flask import json as flask_json
from flask import request
from flask_login import LoginManager, current_user, login_required
from services.analyze_service import AnalyzeService
from services.file_service import FileService
from services.user_service import UserService

app = Flask(__name__)
# для авторизации
login_manager = LoginManager()
login_manager.init_app(app)

# автоматическая генерация OpenAPI, доступна по /apidocs
app.config["SWAGGER"] = swagger_schemas.SWAGGER_SETTINGS
swagger = Swagger(app)

app.config["FILE_UPLOAD_FOLDER"] = "/datasets"


@login_manager.user_loader
def load_user(user):
    user = UserService.get_user_by_id(user)
    return user


@app.before_request
def before_request():
    with app.app_context():
        FileService.list_datasets()


if __name__ == "__main__":
    from api.auth import bp as auth_bp
    from api.graphic import bp as graphic_bp
    from api.users import bp as user_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(graphic_bp)

    app.secret_key = "37f2ab79-9be0-4c0b-8c73-8ac63a816629"

    app.run(debug=True, host="0.0.0.0")
