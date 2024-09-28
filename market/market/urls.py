from django.contrib import admin
from django.urls import path,include
from django.conf.urls.static import static
from django.conf import settings
from rest_framework.routers import DefaultRouter
from apps.accounts.views import CustomUserViewSet

# -------------------------------------------------------------------------------
router = DefaultRouter()
router.register(r'users', CustomUserViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/',include(('apps.accounts.urls'),namespace ='accounts')),
    path('products/',include(('apps.products.urls'),namespace ='products')),
    path('', include(router.urls)),

]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
