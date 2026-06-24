def success_response(
    message: str,
    data=None
):
    return {
        "success": True,
        "message": message,
        "data": data
    }


def error_response(
    message: str,
    data=None
):
    return {
        "success": False,
        "message": message,
        "data": data
    }

def paginated_response(
        message: str,
        items: list,
        page: int,
        limit: int,
        total: int
):
    return {
        "success": True,
        "message": message,
        "data": {
            "items": items,
            "pagination": {
                "page": page,
                "limit": limit,
                "total": total,
                "pages": (
                    total + limit - 1
                ) // limit
            }
        }
    }