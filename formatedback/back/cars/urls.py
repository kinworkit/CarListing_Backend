from django.urls import path
from . import views as vi
from .views import ComplectListView, ComplectDetailView

urlpatterns = [
    path('cars/', vi.car_list, name='car_list'),
    path('cars/<int:pk>/', vi.car_detail, name='car_detail'),
    path('cars/search/', vi.car_search, name='car_search'),
    path('marks/', vi.get_marks, name='get_marks'),
    path('years/', vi.get_years, name='get_years'),
    path('models/', vi.get_models, name='get_models'),
    path('kpps/', vi.get_kpp, name='get_kpp'),
    path('complects/', ComplectListView.as_view(), name='complect_list'),
    path('complects/<int:pk>/', ComplectDetailView.as_view(), name='complect_detail')
]