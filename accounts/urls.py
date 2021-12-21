from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path
from . import views
from .forms import LoginForm

urlpatterns = [
    path('login/', LoginView.as_view(
        form_class=LoginForm,
        template_name='accounts/login_form.html'
    ), name='login'),
    # LogoutView.as_view(next_page='') 리졸브 url을 사용하기 때문에 다음 페이지를 지정해줄 수 있지만
    # https://github.com/django/django/blob/main/django/contrib/auth/views.py
    # global setting에 주소를 세팅해주는 게 더 낫다
    # https://github.com/django/django/blob/main/django/conf/global_settings.py
    path('logout/', LogoutView.as_view(), name='logout'),
    path('profile/', views.profile, name='profile'),
    path('profile/edit/', views.profile_edit, name='profile_edit'),
    path('signup/', views.signup, name='signup'),
]
