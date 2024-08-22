url_module_mapping = {
    "/docs": ("custom", "document", "docs"),
    "/openapi.json": ("custom", "document", "docs2")
}

status_code_rules = {
    "401": {"message": "Unauthorized", "message_code": "401"},
    "422": {"message": "Unprocessable Entity", "message_code": "422"},
    "500": {"message": "Internal Server Error", "message_code": "500"},
}