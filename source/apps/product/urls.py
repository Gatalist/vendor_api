from django.urls import path
from .views import (
    CategoryView,
    SubCategoryView,
    ProductListView,
    ProductDetailView,
    ProductFilesView
)

app_name = 'product'

urlpatterns = [
    path('', CategoryView.as_view(), name="category_list"),
    path('<int:category_id>/', SubCategoryView.as_view(), name="subcategory_list"),
    path('<int:category_id>/<int:subcategory_id>/', ProductListView.as_view(), name="product_list"),
    path('<int:category_id>/<int:subcategory_id>/<int:product_id>/', ProductDetailView.as_view(), name="product_detail"),
    path('product-files/', ProductFilesView.as_view(), name="product_files"),
]
