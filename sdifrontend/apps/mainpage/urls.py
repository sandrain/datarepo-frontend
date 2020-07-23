from django.urls import path
from . import views

app_name = 'mainpage'

urlpatterns = [
    path('dataset/upload', views.BasicUploadView.as_view(), name="upload"),
    path('dataset/', views.DataSetsListView.as_view(), name="dataset-index"),
    path('dataset/create/', views.DatasetCreate.as_view(), name='dataset-create'),
    path('dataset/<int:pk>/', views.DatasetView.as_view(), name="dataset-detail"),
    path('dataset/<int:pk>/update/', views.DatasetUpdate.as_view(), name="dataset-update"),
    path('dataset/<int:pk>/delete/', views.DatasetDelete.as_view(), name="dataset-delete"),
    path('dataset/type/<int:type>/', views.DataSetsListView.as_view(), name="dataset-type"),
    path('basic_upload/', views.BasicUploadView.as_view(), name='basic_upload'),
    # Categories
    path('dataset/category/', views.CategoryView.as_view(), name="category-index"),
    path('dataset/category/<int:category>/', views.DataSetsListView.as_view(), name="dataset-category"),
]
