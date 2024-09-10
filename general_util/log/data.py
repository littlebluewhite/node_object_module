url_module_mapping = {
    "/docs": ("custom", "document", "docs"),
    "/openapi.json": ("custom", "document", "docs2")
}

status_code_rules = {
    "401": {"message": "Unauthorized", "message_code": "401"},
    "403": {"message": "Forbidden", "message_code": "403"},
    "422": {"message": "Unprocessable Entity", "message_code": "422"},
}
