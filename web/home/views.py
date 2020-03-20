from django.shortcuts import render, Http404, HttpResponse
from django.core.paginator import Paginator  # 分布页器

# Create your views here.


# 主页：资源列表
def index(request, p=1):
    return render(request, 'index.html', {'msg': '这里主页！'})





# 搜索逻辑
def search(request):
    search = request.GET.get('search')



def bad_request(request, exception, template_name='400.html'):
    return render(request, template_name)


def permission_denied(request, exception, template_name='403.html'):
    return render(request, template_name)


def page_not_found(request, exception, template_name='404.html'):
    return render(request, template_name)


def server_error(request, template_name='500.html'):
    return render(request, template_name)