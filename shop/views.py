from django.shortcuts import render

# Create your views here.
def home(request):
    return render(request, 'shop/home.html')

def product_list(request):
    return render(request, 'shop/product_list.html')

def product_detail(request, id):
    return render(request, 'shop/product_detail.html', {'product_id': id})

def cart(request):
    return render(request, 'shop/cart.html')

def checkout(request):
    return render(request, 'shop/checkout.html')
