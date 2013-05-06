from django import http
from django.template import loader, RequestContext

def get_response(request, Response, template_name):
    resp = Response()
    t = loader.get_template(template_name)
    resp.content = t.render(RequestContext(request))
    return resp

def NotFound(request,tpl='djazz/HttpResponseNotFound.html'):
    return get_response(request, http.HttpResponseNotFound(), tpl)

def Forbidden(request, tpl='djazz/HttpResponseForbidden.html'):
    return get_response(request, http.HttpResponseForbidden, tpl)

def NotAllowed(request, tpl='djazz/HttpResponseNotAllowed.html'):
    return get_response(request, http.HttpResponseNotAllowed, tpl)

def Gone(request, tpl='djazz/HttpResponseGone.html'):
    return get_response(request, http.HttpResponseGone, tpl)

def Error(request, tpl='djazz/HttpResponseServerError.html'):
    return get_response(request, http.HttpResponseServerError, tpl)
