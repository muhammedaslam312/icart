from django.urls import path
from . import views

urlpatterns = [
    path('shop/',views.shop,name='shop'),
    path('shop/<slug:category_slug>/',views.shop,name='products_by_category'),
    path('shop/<slug:category_slug>/<slug:product_slug>/',views.product_detail,name='products_detail'),
    path('search/',views.search,name='search'),
    path('submit_review/<int:product_id>/', views.submit_review, name="submit_review"),
]