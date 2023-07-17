def set_profile_middleware(get_response):
    def middleware(request, *args, **kwargs):
        if request.user.is_authenticated:
            request.current_user = request.user
        else:
            request.current_user = None
        return get_response(request, *args, **kwargs)

    return middleware