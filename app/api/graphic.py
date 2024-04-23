import swagger_schemas
from exceptions import FileExtensionError, NotTimeSeriesError
from flasgger import swag_from
from flask import Blueprint, request
from flask_login import login_required
from services.graphic_service import GraphicService

bp = Blueprint("graphics", __name__, url_prefix="/graphics")


@bp.get("/")
@swag_from(swagger_schemas.GET_GRAPHIC)
@login_required
def get_graphic():
    graphic_table = request.values["graphic_id"]

    if analyze_type := request.values.get("analyze_type"):
        if analyze_type == "forecasting":
            return GraphicService.get_graphic_prediction(graphic_table)
        elif analyze_type == "anomaly_detection":
            return GraphicService.get_graphic_anomaly(graphic_table)
    return GraphicService.get_graphic(graphic_table)


@bp.post("/")
@swag_from(swagger_schemas.UPLOAD_DATASET)
@login_required
def upload_file():
    uploaded_file = request.files["file"]

    try:
        filename = GraphicService.save_file(uploaded_file)
    except (FileExtensionError, NotTimeSeriesError) as e:
        return e.message, 422

    return f"File {filename} saved successfully", 200
