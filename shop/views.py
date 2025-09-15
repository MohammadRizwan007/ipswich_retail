from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from django.db.models import Q
from django.contrib import messages
from django.core.paginator import Paginator
from django.views.generic import TemplateView
from .models import Product, Category

# Create your views here.
# def home(request):
#     return render(request, 'shop/home.html')

# def product_list(request):
#     return render(request, 'shop/product_list.html')

# def product_detail(request, id):
#     return render(request, 'shop/product_detail.html', {'product_id': id})

# def cart(request):
#     return render(request, 'shop/cart.html')

# def checkout(request):
#     return render(request, 'shop/checkout.html')

class HomeView(TemplateView):
    template_name = 'shop/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['featured_products'] = Product.objects.filter(
            status='active', featured=True
        )[:8]
        context['latest_products'] = Product.objects.filter(
            status='active'
        ).order_by('-created_at')[:8]
        context['categories'] = Category.objects.all()[:6]
        return context

def about(request):
    return render(request, 'shop/about.html')

def contact(request):
    return render(request, 'shop/contact.html')

class ProductListView(ListView):
    model = Product
    template_name = 'shop/product_list.html'
    context_object_name = 'products'
    paginate_by = 12

    def get_queryset(self):
        queryset = Product.objects.filter(status='active')
        
        # Search functionality
        search_query = self.request.GET.get('search')
        if search_query:
            queryset = queryset.filter(
                Q(name__icontains=search_query) |
                Q(description__icontains=search_query) |
                Q(category__name__icontains=search_query)
            )
        
        # Category filtering
        category_slug = self.request.GET.get('category')
        if category_slug:
            queryset = queryset.filter(category__slug=category_slug)
        
        # Price filtering
        min_price = self.request.GET.get('min_price')
        max_price = self.request.GET.get('max_price')
        if min_price:
            queryset = queryset.filter(price__gte=min_price)
        if max_price:
            queryset = queryset.filter(price__lte=max_price)
        
        # Sorting
        sort_by = self.request.GET.get('sort', '-created_at')
        if sort_by in ['price', '-price', 'name', '-name', 'created_at', '-created_at']:
            queryset = queryset.order_by(sort_by)
        
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['featured_products'] = Product.objects.filter(status='active', featured=True)[:4]
        
        # Preserve GET parameters for pagination
        get_params = self.request.GET.copy()
        if 'page' in get_params:
            del get_params['page']
        context['get_params'] = get_params.urlencode()
        
        return context

class ProductDetailView(DetailView):
    model = Product
    template_name = 'shop/product_detail.html'
    context_object_name = 'product'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

    def get_queryset(self):
        return Product.objects.filter(status='active')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Related products from same category
        context['related_products'] = Product.objects.filter(
            category=self.object.category,
            status='active'
        ).exclude(id=self.object.id)[:4]
        return context

def category_detail(request, slug):
    category = get_object_or_404(Category, slug=slug)
    products = Product.objects.filter(category=category, status='active')
    
    # Pagination
    paginator = Paginator(products, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'category': category,
        'products': page_obj,
        'categories': Category.objects.all(),
    }
    return render(request, 'shop/category_detail.html', context)