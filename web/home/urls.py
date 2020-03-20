from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name='index'),
    path('<int:p>/', index, name='indexpage'),
    path('', index, name='search'),
]

handler400 = bad_request
handler403 = permission_denied
handler404 = page_not_found
handler500 = server_error
