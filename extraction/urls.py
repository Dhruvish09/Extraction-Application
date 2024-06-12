from django.urls import path
from . import views

app_name = 'extraction'

urlpatterns = [
    path('', views.document_list, name='documents'),
    path('signin', views.signin, name='signin'),
    path('signup', views.signup, name="signup"),
    path('logout', views.logout, name='logout'),
    path('upload/', views.upload_file, name='upload'),
]
