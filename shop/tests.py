from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from products.models import Product, Category
from decimal import Decimal

class CoreViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        
        # Create test data
        self.category = Category.objects.create(
            name='Test Category',
            description='Test category for home page'
        )
        
        self.featured_product = Product.objects.create(
            name='Featured Product',
            description='A featured product for testing',
            price=Decimal('49.99'),
            category=self.category,
            stock_quantity=20,
            sku='FEAT001',
            status='active',
            featured=True
        )
        
        self.regular_product = Product.objects.create(
            name='Regular Product',
            description='A regular product for testing',
            price=Decimal('29.99'),
            category=self.category,
            stock_quantity=15,
            sku='REG001',
            status='active',
            featured=False
        )
        
    def test_home_view(self):
        """Test home page view"""
        response = self.client.get(reverse('core:home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Welcome to Ipswich Retail')
        self.assertContains(response, 'Featured Product')
        self.assertContains(response, 'Regular Product')
        
    def test_home_view_context(self):
        """Test home page context data"""
        response = self.client.get(reverse('core:home'))
        
        # Check featured products in context
        featured_products = response.context['featured_products']
        self.assertEqual(len(featured_products), 1)
        self.assertEqual(featured_products[0].name, 'Featured Product')
        
        # Check latest products in context
        latest_products = response.context['latest_products']
        self.assertEqual(len(latest_products), 2)
        
        # Check categories in context
        categories = response.context['categories']
        self.assertEqual(len(categories), 1)
        self.assertEqual(categories[0].name, 'Test Category')
        
    def test_about_view(self):
        """Test about page view"""
        response = self.client.get(reverse('core:about'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'About Ipswich Retail')
        self.assertContains(response, 'Django MVT Architecture')
        self.assertContains(response, 'Model Layer')
        self.assertContains(response, 'View Layer')
        self.assertContains(response, 'Template Layer')
        
    def test_contact_view(self):
        """Test contact page view"""
        response = self.client.get(reverse('core:contact'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Contact Us')
        self.assertContains(response, 'Send us a message')
        self.assertContains(response, 'Contact Information')
        
    def test_navigation_links(self):
        """Test navigation links work correctly"""
        # Test home page navigation
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        
        # Test that navigation contains correct links
        self.assertContains(response, 'href="/"')  # Home link
        self.assertContains(response, reverse('products:product_list'))
        self.assertContains(response, reverse('core:about'))
        self.assertContains(response, reverse('core:contact'))
        
    def test_footer_links(self):
        """Test footer contains proper links"""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        
        # Check footer content
        self.assertContains(response, 'Ipswich Retail')
        self.assertContains(response, '2025')  # Copyright year
        self.assertContains(response, 'Django MVT Architecture')

class TemplateTest(TestCase):
    def setUp(self):
        self.client = Client()
        
    def test_base_template_elements(self):
        """Test base template contains required elements"""
        response = self.client.get('/')
        
        # Check for Bootstrap CSS
        self.assertContains(response, 'bootstrap')
        
        # Check for Font Awesome
        self.assertContains(response, 'font-awesome')
        
        # Check for navbar
        self.assertContains(response, 'navbar')
        self.assertContains(response, 'Ipswich Retail')
        
        # Check for footer
        self.assertContains(response, 'footer')
        
    def test_responsive_design_elements(self):
        """Test responsive design elements are present"""
        response = self.client.get('/')
        
        # Check for viewport meta tag
        self.assertContains(response, 'viewport')
        
        # Check for responsive classes
        self.assertContains(response, 'container')
        self.assertContains(response, 'col-')
        
    def test_css_variables(self):
        """Test CSS custom properties are defined"""
        response = self.client.get('/')
        
        # Check for CSS custom properties
        self.assertContains(response, '--primary-color')
        self.assertContains(response, '--secondary-color')
        
    def test_javascript_includes(self):
        """Test JavaScript libraries are included"""
        response = self.client.get('/')
        
        # Check for Bootstrap JS
        self.assertContains(response, 'bootstrap.bundle.min.js')

class URLTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(
            name='Test Category',
            slug='test-category'
        )
        
        self.product = Product.objects.create(
            name='Test Product',
            slug='test-product',
            description='Test description',
            price=Decimal('29.99'),
            category=self.category,
            stock_quantity=10,
            sku='TEST001',
            status='active'
        )
    
    def test_core_urls(self):
        """Test core app URLs resolve correctly"""
        self.assertEqual(reverse('core:home'), '/')
        self.assertEqual(reverse('core:about'), '/about/')
        self.assertEqual(reverse('core:contact'), '/contact/')
        
    def test_product_urls(self):
        """Test product app URLs resolve correctly"""
        self.assertEqual(reverse('products:product_list'), '/products/')
        self.assertEqual(
            reverse('products:product_detail', kwargs={'slug': 'test-product'}),
            '/products/product/test-product/'
        )
        self.assertEqual(
            reverse('products:category_detail', kwargs={'slug': 'test-category'}),
            '/products/category/test-category/'
        )

class SecurityTest(TestCase):
    def setUp(self):
        self.client = Client()
        
    def test_admin_requires_authentication(self):
        """Test admin panel requires authentication"""
        response = self.client.get('/admin/')
        # Should redirect to login
        self.assertEqual(response.status_code, 302)
        
    def test_csrf_protection(self):
        """Test CSRF protection is enabled"""
        response = self.client.get('/')
        # Should contain CSRF token
        self.assertContains(response, 'csrfmiddlewaretoken')

