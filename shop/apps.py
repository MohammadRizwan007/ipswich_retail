from django.apps import AppConfig
import os
from django.conf import settings

class ShopConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'shop'
    def ready(self):
        # Ensure the products folder exists in MEDIA_ROOT
        products_path = os.path.join(settings.MEDIA_ROOT, 'products')
        os.makedirs(products_path, exist_ok=True)  

   
    
