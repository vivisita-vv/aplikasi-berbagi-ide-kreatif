# Di dalam core/admin.py

from django.contrib import admin
from .models import Kategori, Ide, Komentar

admin.site.register(Kategori)
admin.site.register(Ide)
admin.site.register(Komentar)