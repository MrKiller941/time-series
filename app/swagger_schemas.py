SWAGGER_SETTINGS = {
    "version": "1.0.0",
    "title": "Analyze dataset API",
}

GET_USERS = {
    "responses": {200: {"description": "List of users"}},
}

UPLOAD_DATASET = {
    "summary": "Upload dataset",
    "consumes": ["multipart/form-data"],
    "parameters": [
        {
            "name": "file",
            "in": "formData",
            "description": "Dataset",
            "required": True,
            "type": "file",
        }
    ],
    "responses": {200: {"description": "Success"}, 400: {"description": "Bad Request"}},
}

GET_GRAPHIC = {
    "summary": "Get upload datasets graphic",
    "consumes": ["multipart/form-data"],
    "parameters": [
        {
            "name": "graphic_id",
            "in": "formData",
            "description": "Dataset name",
            "required": True,
            "type": "string",
        },
        {
            "name": "analyze_type",
            "in": "formData",
            "description": "Type of analysis",
            "required": False,
            "type": "string",
            "enum": ["anomaly_detection", "forecasting"],
        },
    ],
    "responses": {
        200: {
            "description": "Success",
            "schema": {
                "type": "object",
                "properties": {
                    "analysis_id": {"type": "string"},
                    "date": {"type": "string", "format": "date-time"},
                    "data": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "name": {"type": "string"},
                                "values": {
                                    "type": "array",
                                    "items": {
                                        "type": "object",
                                        "properties": {
                                            "time": {
                                                "type": "string",
                                                "format": "date-time",
                                            },
                                            "value": {"type": "number"},
                                        },
                                    },
                                },
                            },
                        },
                    },
                    "meta": {
                        "type": "object",
                        "properties": {
                            "selected_algorithm": {"type": "string"},
                            "target_column": {"type": "string"},
                            "selected_parameters": {
                                "type": "array",
                                "items": {
                                    "type": "object",
                                    "properties": {
                                        "parameter": {"type": "string"},
                                        "value": {"type": ["number", "null"]},
                                    },
                                },
                            },
                            "metrics": {
                                "type": "array",
                                "items": {
                                    "type": "object",
                                    "properties": {
                                        "name": {"type": "string"},
                                        "value": {"type": "string"},
                                    },
                                },
                            },
                            "results": {
                                "type": "array",
                                "items": {
                                    "type": "object",
                                    "properties": {
                                        "name": {"type": "string"},
                                        "value": {"type": "string"},
                                    },
                                },
                            },
                        },
                    },
                },
            },
        },
        400: {"description": "Bad Request"},
    },
}

ANALYZE_DATASET = {
    "summary": "Analyze dataset",
    "parameters": [
        {
            "name": "filename",
            "in": "formData",
            "description": "Dataset to analyze",
            "required": True,
            "type": "string",
        },
    ],
    "responses": {
        200: {"description": "Analysis result"},
        400: {"description": "Bad Request"},
    },
}
