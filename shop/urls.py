from django.urls import path
from . import views

app_name = 'shop'

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('products/', views.ProductListView.as_view(), name='product_list'),
    path('product/<slug:slug>/', views.ProductDetailView.as_view(), name='product_detail'),
    path('category/<slug:slug>/', views.category_detail, name='category_detail'),
]
