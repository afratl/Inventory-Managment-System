from django.shortcuts import render,HttpResponse
from .models import *

# Create your views here.
def index(request):
    return render(request, 'index.html')
def category_list(request):
    query = request.GET.get('q')  # Arama sorgusu
    category_id = request.GET.get('category', '')
    categories = Category.objects.all()

    if query:
        categories = categories.filter(name__icontains=query)  # Sadece isimde arama yap

    if category_id:
        categories = categories.filter(id=category_id)

    context = {
        'categories': categories,
    }
    return render(request, 'category_list.html', context)

def category_products(request, category_id):
    category = Category.objects.get(id=category_id)
    products = Product.objects.filter(category=category)
    context = {
        'category': category,
        'products': products,
    }
    return render(request, 'category_products.html', context)

def brand_list(request):
    query = request.GET.get('q')  # Arama sorgusunu al
    if query:
        brands = Brand.objects.filter(name__icontains=query)  # Marka adında arama yap
    else:
        brands = Brand.objects.all()  
    context = {
        'brands': brands,
    }
    return render(request, 'brand_list.html', context)

def product_list(request):
    query = request.GET.get('q')  # Arama sorgusu
    category_id = request.GET.get('category')  # Kategori filtresi
    

    products = Product.objects.all()

    if query:
        products = products.filter(name__icontains=query)  # Ürün adında arama yap
    if category_id:
        products = products.filter(category_id=category_id)  # Kategoriye göre filtrele
    

    categories = Category.objects.all()  # Tüm kategoriler
    

    context = {
        'products': products,
        'categories': categories,
        'selected_category_id': category_id
        
    }
    return render(request, 'product_list.html', context)

def product_detail(request, product_id):
    try:
    
        product = Product.objects.get(id=product_id)
        context = {
            'product': product,
        }
        return render(request, 'product_detail.html', context)
    except:
        return HttpResponse("Product not found")


def firm_list(request):
    query = request.GET.get('q')  # Arama sorgusunu al
    if query:
        firms = Firm.objects.filter(name__icontains=query)  # Firma adında arama yap
    else:
        firms = Firm.objects.all()  
    context = {
        'firms': firms,
    }
    return render(request, 'firm_list.html', context)

def purchases_list(request):
    query = request.GET.get('q')  # Arama sorgusu
    firm_id = request.GET.get('firm')  # Firma filtresi
    purchases = Purchases.objects.all()
    if query:
        purchases = purchases.filter(product__name__icontains=query)  # Ürün adında arama yap
    if firm_id:
        purchases = purchases.filter(firm_id=int(firm_id))  # Firmaya göre filtrele
    
           
    firms = Firm.objects.all()  # Tüm firmalar
    context = {
        'purchases': purchases,
        'firms': firms,
        'selected_firm_id': firm_id,
    }
    return render(request, 'purchases_list.html', context)

def sales_list(request):
    query = request.GET.get('q')  # Arama sorgusu
    brand_id = request.GET.get('brand')  # Marka filtresi
    sales = Sales.objects.all()
    if query:
        sales = sales.filter(product__name__icontains=query)  # Ürün adında arama yap
    if brand_id:
        sales = sales.filter(brand_id=brand_id)  # Markaya göre filtrele
    brands = Brand.objects.all()  # Tüm markalar        
    
    context = {
        'sales': sales,
        'brands': brands,
        'selected_brand_id': brand_id,
        
    }
    return render(request, 'sales_list.html', context)
