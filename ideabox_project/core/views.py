# Di dalam core/views.py

from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
# --- DITAMBAHKAN ---
from django.db.models import Q
# -------------------
from .models import Ide, Komentar
from .forms import UserSignUpForm, KomentarForm

# View untuk menampilkan daftar semua ide (Halaman Utama)
class IdeListView(ListView):
    model = Ide
    template_name = 'core/home.html'
    context_object_name = 'ide_list'
    ordering = ['-dibuat_pada']
    paginate_by = 5

    # --- DITAMBAHKAN: Method untuk logika pencarian ---
    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(
                Q(judul__icontains=query) |
                Q(deskripsi__icontains=query)
            ).distinct()
        return queryset
    # ------------------------------------------------

# View untuk menampilkan detail satu ide
class IdeDetailView(DetailView):
    model = Ide
    template_name = 'core/ide_detail.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['komentar_form'] = KomentarForm()
        context['komentar_list'] = self.object.komentar.all()
        return context

# View untuk membuat ide baru
class IdeCreateView(LoginRequiredMixin, CreateView):
    model = Ide
    fields = ['judul', 'deskripsi', 'gambar', 'kategori', 'status']
    template_name = 'core/ide_form.html'

    def form_valid(self, form):
        form.instance.penulis = self.request.user
        return super().form_valid(form)

# View untuk mengedit ide
class IdeUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Ide
    fields = ['judul', 'deskripsi', 'gambar', 'kategori', 'status']
    template_name = 'core/ide_form.html'

    def form_valid(self, form):
        form.instance.penulis = self.request.user
        return super().form_valid(form)

    def test_func(self):
        ide = self.get_object()
        return self.request.user == ide.penulis

# View untuk menghapus ide
class IdeDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Ide
    template_name = 'core/ide_confirm_delete.html'
    success_url = reverse_lazy('home')

    def test_func(self):
        ide = self.get_object()
        return self.request.user == ide.penulis

# View untuk registrasi pengguna (signup)
def signup(request):
    if request.method == 'POST':
        # Penyesuaian form signup jika ada file yang diupload (opsional, tapi praktik yang baik)
        form = UserSignUpForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserSignUpForm()
    return render(request, 'registration/signup.html', {'form': form})

# View untuk menambah komentar (function-based)
@login_required
def tambah_komentar(request, pk):
    ide = get_object_or_404(Ide, pk=pk)
    if request.method == 'POST':
        form = KomentarForm(request.POST)
        if form.is_valid():
            komentar = form.save(commit=False)
            komentar.ide = ide
            komentar.penulis = request.user
            komentar.save()
            return redirect('ide-detail', pk=ide.pk)
    return redirect('ide-detail', pk=ide.pk)

# View untuk like/suka (function-based)
@login_required
def suka_ide(request, pk):
    ide = get_object_or_404(Ide, pk=pk)
    if request.user in ide.suka.all():
        ide.suka.remove(request.user)
    else:
        ide.suka.add(request.user)
    return redirect('ide-detail', pk=ide.pk)

# View untuk profil
def profil_view(request, username):
    profil_user = get_object_or_404(User, username=username)
    ide_user = Ide.objects.filter(penulis=profil_user).order_by('-dibuat_pada')
    context = {
        'profil_user': profil_user,
        'ide_user': ide_user,
    }
    return render(request, 'core/profil.html', context)