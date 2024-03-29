"""
URL configuration for HFDLSP project.

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
from django.urls import path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from data_transformer.views import answer_view
from data_retriever.views import fetch_dataset_view
from django.views.generic.base import RedirectView

urlpatterns = [
    path('', RedirectView.as_view(url='https://aitrenches.github.io/HFDLSP/'), name='redirect-to-target'),
    path("admin/", admin.site.urls),
    path("answer/", answer_view, name="answer"),
    path("fetch_dataset/", fetch_dataset_view, name="fetch_dataset"),
    path("schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "swagger-ui/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
]
