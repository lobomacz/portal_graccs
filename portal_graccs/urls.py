"""hamsterserv URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import include, path
from django.views.generic.base import TemplateView
from portal_graccs.admin import hamster_admin, suir_admin, sispro_admin


urlpatterns = [
    path('admin/', include([
        path('1/', suir_admin.urls),
        path('2/', hamster_admin.urls),
        path('3/', sispro_admin.urls),
        ])),
    path('api/', include([
        path('hamster/', include('hamster.urls')),
        path('sispro/', include('sispro.urls')),
        ])),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('hamster/', TemplateView.as_view(template_name='hamster/index.html'), name='inicio_hamster'),
    path('sispro/', TemplateView.as_view(template_name='sispro/index.html'), name='inicio_sispro'),
    path('', include('suir.urls')),
]


