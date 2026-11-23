from django.urls import path
from . import views

urlpatterns = [
    path('', views.CalculationListView.as_view(), name='history'),
    path('new/', views.CalculationCreateView.as_view(), name='calc_new'),
    path('register/', views.RegisterView.as_view(), name='register'), 
    path('edit/<int:pk>/', views.CalculationUpdateView.as_view(), name='calc_edit'),
    path('delete/<int:pk>/', views.CalculationDeleteView.as_view(), name='calc_delete'),
    path('chart/', views.chart_view, name='chart'),
    path('export/', views.export_csv, name='export_csv'),
]