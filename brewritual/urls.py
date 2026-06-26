from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from menu import views as menu_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', menu_views.home, name='home'),
    path('menu/', include('menu.urls')),
    path('accounts/', include('accounts.urls')),
    path('orders/', include('orders.urls')),
    path('loyalty/', include('loyalty.urls')),
    path('ritual/', include('ritual_guide.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
