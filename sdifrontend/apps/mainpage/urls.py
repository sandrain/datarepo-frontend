from django.urls import path
from . import views

app_name = 'mainpage'

urlpatterns = [
    path('data/', views.index.IndexView.as_view(), name="dataset-index"),
    path('dataset/create/', views.DatasetCreate.as_view(), name='dataset-create'),
    path('dataset/<int:pk>/', views.DatasetView.as_view(), name="dataset-detail"),
    path('dataset/<int:pk>/update/', views.DatasetUpdate.as_view(), name="dataset-update"),
    path('dataset/<int:pk>/delete/', views.DatasetDelete.as_view(), name="dataset-delete"),
    path('dataset/category/<int:category>/', views.DataSetsTypeView.as_view(), name="dataset-category"),
    path('dataset/type/<int:type>/', views.DataSetsTypeView.as_view(), name="dataset-type"),
    path('basic_upload/', views.BasicUploadView.as_view(), name='basic_upload'),
    path('ajax/get_similar_datasets/', views.get_similar_datasets, name='get_similar_datasets'),
]
