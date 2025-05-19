from django.urls import path
from . import views
from .views import user_logout

urlpatterns = [
    path('', views.review_dashboard, name='review_dashboard'),   # /review/
    path('login/', views.student_login, name='student_login'),    # /review/login/
    path('signup/', views.student_signup, name='student_signup'), # /review/signup/
    path('submit-help/', views.submit_help_request, name='submit_help'),
    path('logout/', user_logout, name='logout'),
]
