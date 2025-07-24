# config/urls.py

from django.contrib import admin
from django.urls import path, include

# === IMPORT BARU DITAMBAHKAN DI SINI ===
from django.conf import settings
from django.conf.urls.static import static
# ======================================

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
]

# === KODE BARU DITAMBAHKAN DI SINI ===
# Menambahkan pola URL untuk menyajikan file media HANYA saat dalam mode DEBUG
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
# ====================================