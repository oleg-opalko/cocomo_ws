from django.urls import path
from . import views
from .views import ProjectDeleteView, ScaleDriverCreateView, CostDriverCreateView, ScaleDriverUpdateView, ScaleDriverDeleteView, CostDriverUpdateView, CostDriverDeleteView

urlpatterns = [
    path('', views.ProjectListView.as_view(), name='project-list'),
    path('project/new/', views.ProjectCreateView.as_view(), name='project-create'),
    path('project/<int:pk>/', views.ProjectDetailView.as_view(), name='project-detail'),
    path('project/<int:pk>/edit/', views.ProjectUpdateView.as_view(), name='project-update'),
    path('projects/<int:pk>/delete/', ProjectDeleteView.as_view(), name='project-delete'),
    path('scale-driver/new/', ScaleDriverCreateView.as_view(), name='scale-driver-create'),
    path('cost-driver/new/', CostDriverCreateView.as_view(), name='cost-driver-create'),
    path('scale-driver/<int:pk>/edit/', ScaleDriverUpdateView.as_view(), name='scale-driver-update'),
    path('scale-driver/<int:pk>/delete/', ScaleDriverDeleteView.as_view(), name='scale-driver-delete'),
    path('cost-driver/<int:pk>/edit/', CostDriverUpdateView.as_view(), name='cost-driver-update'),
    path('cost-driver/<int:pk>/delete/', CostDriverDeleteView.as_view(), name='cost-driver-delete'),
    # path('project/<int:pk>/scale-drivers/', views.ProjectScaleDriverListView.as_view(), name='project-scale-drivers'),
    # path('project/<int:pk>/cost-drivers/', views.ProjectCostDriverListView.as_view(), name='project-cost-drivers'),
] 