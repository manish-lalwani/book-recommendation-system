def common_error_responses():
    return {
        400: {
            "description": "Bad Request - The server could not understand the request due to invalid syntax.",
            "content": {
                "application/json": {
                    "example": {
                        "success": False,
                        "error": {
                            "message": "Invalid request data provided.",
                            "status_code": 400,
                        },
                    }
                }
            },
        },
        401: {
            "description": "Unauthorized - The client must authenticate itself to get the requested response.",
            "content": {
                "application/json": {
                    "example": {
                        "success": False,
                        "error": {
                            "message": "Authentication credentials were not provided.",
                            "status_code": 401,
                        },
                    }
                }
            },
        },
        403: {
            "description": "Forbidden - The client does not have access rights to the content.",
            "content": {
                "application/json": {
                    "example": {
                        "success": False,
                        "error": {
                            "message": "You do not have permission to access this resource.",
                            "status_code": 403,
                        },
                    }
                }
            },
        },
        404: {
            "description": "Not Found - The server can not find the requested resource.",
            "content": {
                "application/json": {
                    "example": {
                        "success": False,
                        "error": {
                            "message": "The requested resource was not found.",
                            "status_code": 404,
                        },
                    }
                }
            },
        },
        422: {
            "description": "Unprocessable Entity - The request was well-formed but was unable to be followed due to semantic errors.",
            "content": {
                "application/json": {
                    "example": {
                        "success": False,
                        "error": {
                            "message": "Validation error occurred.",
                            "status_code": 422,
                            "details": [
                                {
                                    "loc": ["body", "field_name"],
                                    "msg": "field required",
                                    "type": "value_error.missing",
                                }
                            ],
                        },
                    }
                }
            },
        },
        500: {
            "description": "Internal Server Error - The server has encountered a situation it doesn't know how to handle.",
            "content": {
                "application/json": {
                    "example": {
                        "success": False,
                        "error": {
                            "message": "An unexpected error occurred on the server.",
                            "status_code": 500,
                        },
                    }
                }
            },
        },
    }
