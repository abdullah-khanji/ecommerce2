from django.urls import path
from . import views
app_name = 'api'
urlpatterns = [
    path('', views.ProductListApi.as_view(), name='product_list'),
    path('<int:pk>/', views.ProductDetailApi.as_view(), name='product_detail'),
    path('order/', views.OrderAPI.as_view(), name='order'),
    path('bot_search_api/', views.bot_search, name='bot_search'),
]
