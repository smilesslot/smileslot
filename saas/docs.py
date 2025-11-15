try:
    from drf_spectacular.utils import extend_schema, OpenApiResponse
except ImportError:
    from functools import wraps
    from .compat import available_attrs

    def extend_schema(function=None, **kwargs):
        """
        Dummy decorator when drf_spectacular is not present.
        """
        def decorator(view_func):
            @wraps(view_func, assigned=available_attrs(view_func))
            def _wrapped_view(request, *args, **kwargs):
                return view_func(request, *args, **kwargs)
            return _wrapped_view

        if function:
            return decorator(function)
        return decorator

    class OpenApiResponse(object):
        """
        Dummy response object to document API.
        """
        def __init__(self, *args, **kwargs):
            pass
