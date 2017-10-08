def relative_path(request):
    try:
        request.META['HTTP_HOST']
    except KeyError:
        http_host = request.META['REMOTE_ADDR'] + request.META['SERVER_PORT']
    else:
        http_host = request.META['HTTP_HOST']
    PORTAL_URL = request.META['wsgi.url_scheme'] +'://' + http_host
    return {'PORTAL_URL': PORTAL_URL}
