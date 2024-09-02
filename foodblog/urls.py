"""
URL configuration for foodblog project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.contrib import admin
from django.conf.urls import handler403, handler404, handler500
from django.urls import path, include
from .views import custom_403, custom_404, custom_500

# Custom error handler
handler403 = 'foodblog.views.custom_403'
handler404 = 'foodblog.views.custom_404'
handler500 = 'foodblog.views.custom_500'

urlpatterns = [
    path("about/", include('about.urls'), name='about-urls'),
    path("accounts/", include("allauth.urls")),
    path('admin/', admin.site.urls),
    path('summernote/', include('django_summernote.urls')),
    path('recipes/', include("recipes.urls")),
    path('', include("home.urls")),

]
