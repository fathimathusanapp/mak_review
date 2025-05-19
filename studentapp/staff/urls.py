from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.staff_login, name='staff_login'),  # /staff/login/
    path('', views.help_requests_view, name='staff_help_requests'),  # /staff/
    path('accept/<int:request_id>/', views.accept_help_request, name='accept_help_request'),
    path('handle/<int:request_id>/', views.mark_request_handled, name='mark_request_handled'),
]
