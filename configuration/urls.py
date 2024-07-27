from django.contrib import admin
from django.urls import path
from ckeditor_uploader import views as ckeditor_view
from ckeditor_uploader import views as ckeditor_views
from django.conf import settings
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from django.urls import include, path, re_path
from django.views.decorators.cache import never_cache
from django.views.static import serve
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/',  include('users.urls')),
    path('core/',  include('core.urls')),
    path("", TemplateView.as_view(template_name="base/inicio.html"), name='inicio'),
    path("infosistema", TemplateView.as_view(template_name="base/infosistema.html"), name='infosistema'),
    path('login/', auth_views.LoginView.as_view(template_name='users/users/login.html'), name='login'),
    # path('logout/', auth_views.LogoutView.as_view(template_name='users/users/logout.html'), name='logout'),
    path('ckeditor/upload/', login_required(ckeditor_views.upload), name='ckeditor_upload'),
    path('ckeditor/browse/', never_cache(login_required(ckeditor_views.browse)), name='ckeditor_browse'),

    re_path(r'^media/(?P<path>.*)$', serve,{'document_root': settings.MEDIA_ROOT}), 
    re_path(r'^static/(?P<path>.*)$', serve,{'document_root': settings.STATIC_ROOT}),
]
