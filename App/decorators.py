from django.shortcuts import redirect
from functools import wraps

def role_required(expected_role):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if hasattr(request.user, 'profile') and request.user.profile.role == expected_role:
                return view_func(request, *args, **kwargs)
            else:
                return redirect('login')  # or show 403 page
        return _wrapped_view
    return decorator
