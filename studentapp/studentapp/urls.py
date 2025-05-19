from django.urls import path, include
from django.shortcuts import redirect
from review import views as review_views
from django.contrib import admin


urlpatterns = [
    path('admin/', admin.site.urls),
    path('review/', include('review.urls')),
    path('staff/', include('staff.urls')),

    path('signup/', review_views.student_signup, name='student_signup'),
    path('login/', review_views.student_login, name='student_login'),

    path('', lambda request: redirect('review/')),
]
