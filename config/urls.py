"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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

from main import views
from main.views import CostDriverCreateView, ProjectDeleteView, ScaleDriverCreateView, index

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('', index, name='idex'),
    path('', views.ProjectListView.as_view(), name='project-list'),
    path('project/new/', views.ProjectCreateView.as_view(), name='project-create'),
    path('project/<int:pk>/', views.ProjectDetailView.as_view(), name='project-detail'),
    path('project/<int:pk>/edit/', views.ProjectUpdateView.as_view(), name='project-update'),
    path('projects/<int:pk>/delete/', ProjectDeleteView.as_view(), name='project-delete'),
    path('scale-driver/new/', ScaleDriverCreateView.as_view(), name='scale-driver-create'),
    path('cost-driver/new/', CostDriverCreateView.as_view(), name='cost-driver-create'),
]
