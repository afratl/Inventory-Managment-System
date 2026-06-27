from django.contrib import admin
from django.urls import include, path
from app import views

urlpatterns = [
    path ('',views.index, name='index'),
    path('/admin/', admin.site.urls),
    path('categories/',views.category_list, name='category_list'),
    path('categories/<int:category_id>/products/', views.category_products, name='category_products'),
    path('brands/',views.brand_list, name='brand_list'),
    path('products/',views.product_list, name='product_list'),
    path('products/<int:product_id>/', views.product_detail, name='product_detail'),
    path('firms/',views.firm_list, name='firm_list'),
    path('purchases/',views.purchases_list, name='purchases_list'),
    path('sales/',views.sales_list, name='sales_list'),
    path('api/',include('app.api.urls')) 

   ]