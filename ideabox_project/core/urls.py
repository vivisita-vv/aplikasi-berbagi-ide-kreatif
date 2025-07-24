# Di dalam core/urls.py

from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # Halaman Utama
    path('', views.IdeListView.as_view(), name='home'),

    # URL untuk Ide
    path('ide/<int:pk>/', views.IdeDetailView.as_view(), name='ide-detail'),
    path('ide/baru/', views.IdeCreateView.as_view(), name='ide-create'),
    path('ide/<int:pk>/edit/', views.IdeUpdateView.as_view(), name='ide-update'),
    path('ide/<int:pk>/hapus/', views.IdeDeleteView.as_view(), name='ide-delete'),
    path('ide/<int:pk>/suka/', views.suka_ide, name='ide-suka'),

    # URL untuk Komentar
    path('ide/<int:pk>/komentar/', views.tambah_komentar, name='tambah-komentar'),

    # URL untuk Autentikasi
    path('signup/', views.signup, name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    # URL Profil
    path('profil/<str:username>/', views.profil_view, name='profil'),
]