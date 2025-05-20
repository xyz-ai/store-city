from django.urls import path
from .views import LatestProductsList, ProductDetail, CategoryDetail, ProductSearchView

urlpatterns = [
    path("latest-products/", LatestProductsList.as_view(), name='latest-products'),
    path("products/search/", ProductSearchView.as_view(), name='product-search'),
    path("products/<slug:category_slug>/<slug:product_slug>/", ProductDetail.as_view(), name='product-detail'),
    path("products/<slug:category_slug>/", CategoryDetail.as_view(), name='category-detail'),
]