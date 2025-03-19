def type_convertor(doc):
    """Convert types for MongoDB documents"""
    if "api_version" in doc:
        doc["api_version"] = str(doc["api_version"])

    if "show_recommendation" in doc:
        doc["show_recommendation"] = (
            True if str(doc["show_recommendation"]).lower() == "true" else False
        )

    if "recommendation" in doc:
        doc["recommendation"] = (
            True if str(doc["recommendation"]).lower() == "true" else False
        )

    if "utm_source" in doc:
        doc["utm_source"] = True if str(doc["utm_source"]).lower() == "true" else False

    if "utm_medium" in doc:
        doc["utm_medium"] = True if str(doc["utm_medium"]).lower() == "true" else False

    if "cart_products" in doc:
        for cart_product in doc.get("cart_products", []):
            if cart_product["option"] == "":
                cart_product["option"] = []

    return doc
