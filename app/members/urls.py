from django.urls import path

from . import views

app_name = 'members'
urlpatterns = [
    path('login/',views.login_view, name='login_view'),
    path('logout/', views.logout_view, name='logout_view'),
    path('signup/', views.signup_view, name='signup_view'),

]