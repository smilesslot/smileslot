from functools import wraps

from slots.utils.error_codes import ErrorCode
from slots.utils.json_context import json_response
from slots.utils.view_helpers import is_ajax


def require_user_authenticated(func):
    """Decorator to require a user to be authenticated.
    Usage: @require_user_authenticated
    """

    @wraps(func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return json_response("Not authorized.", status=401, success=False, error_code=ErrorCode.NOT_AUTHORIZED)
        return func(request, *args, **kwargs)

    return wrapper


def require_staff_or_superuser(func):
    """Decorator to require a user to be a staff or superuser.
    Usage: @require_staff_or_superuser
    """

    @wraps(func)
    def wrapper(request, *args, **kwargs):
        if not (request.user.is_staff or request.user.is_superuser):
            return json_response("Not authorized.", status=403, success=False, error_code=ErrorCode.NOT_AUTHORIZED)
        return func(request, *args, **kwargs)

    return wrapper


def require_superuser(func):
    """Decorator to require a user to be a superuser.
    Usage: @require_superuser
    """

    @wraps(func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_superuser:
            return json_response("Not authorized.", status=403, success=False, error_code=ErrorCode.NOT_AUTHORIZED)
        return func(request, *args, **kwargs)

    return wrapper


def require_ajax(func):
    """Decorator to require a request to be AJAX.
    Usage: @require_ajax
    """

    @wraps(func)
    def wrapper(request, *args, **kwargs):
        if not is_ajax(request):
            return json_response("Not an AJAX request.", status=400, success=False, error_code=ErrorCode.INVALID_DATA)
        return func(request, *args, **kwargs)

    return wrapper
