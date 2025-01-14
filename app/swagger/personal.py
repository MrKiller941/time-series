CALC_HISTORY = {
    "summary": "Get calculation history",
    "responses": {
        200: {"description": "Calculation history"},
        400: {"description": "Bad Request"},
    },
    "tags": ["user"],
}

CHANGE_USERNAME = {
    "summary": "Change username",
    "parameters": [
        {
            "name": "new_username",
            "in": "formData",
            "description": "New username",
            "required": True,
            "type": "string",
        },
    ],
    "responses": {
        200: {"description": "Successful update"},
        400: {"description": "Bad Request"},
    },
    "tags": ["user"],
}

CHANGE_PASSWORD = {
    "summary": "Change password",
    "parameters": [
        {
            "name": "current_password",
            "in": "formData",
            "description": "Current password",
            "required": True,
            "type": "string",
            "format": "password",
        },
        {
            "name": "new_password",
            "in": "formData",
            "description": "New password",
            "required": True,
            "type": "string",
            "format": "password",
        },
        {
            "name": "repeated_password",
            "in": "formData",
            "description": "Repeat new password",
            "required": True,
            "type": "string",
            "format": "password",
        },
    ],
    "responses": {
        200: {"description": "Successful update"},
        400: {"description": "Bad Request"},
    },
    "tags": ["user"],
}


DELETE_PROFILE = {
    "summary": "Change password",
    "parameters": [
        {
            "name": "password",
            "in": "formData",
            "description": "password",
            "required": True,
            "type": "string",
            "format": "password",
        },
    ],
    "responses": {
        200: {"description": "Successful delete"},
        400: {"description": "Bad Request"},
    },
    "tags": ["user"],
}
