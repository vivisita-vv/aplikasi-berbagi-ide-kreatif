from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

class Kategori(models.Model):
    nama = models.CharField(max_length=50, unique=True)
    
    class Meta:
        verbose_name_plural = "Kategori"

    def __str__(self):
        return self.nama

class Ide(models.Model):
    class StatusPilihan(models.TextChoices):
        KONSEP = 'Konsep', 'Konsep'
        PENGEMBANGAN = 'Pengembangan', 'Pengembangan'
        SELESAI = 'Selesai', 'Selesai'

    penulis = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ide')
    judul = models.CharField(max_length=200)
    deskripsi = models.TextField()

    # === PERUBAHAN DI SINI ===
    # Menambahkan field gambar yang tidak wajib diisi.
    gambar = models.ImageField(upload_to='ide_pics', null=True, blank=True)
    # =========================

    kategori = models.ForeignKey(Kategori, on_delete=models.SET_NULL, null=True, blank=True)
    status = models.CharField(
        max_length=20,
        choices=StatusPilihan.choices,
        default=StatusPilihan.KONSEP
    )
    suka = models.ManyToManyField(User, related_name='ide_disukai', blank=True)
    dibuat_pada = models.DateTimeField(auto_now_add=True)
    diperbarui_pada = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.judul

    def get_absolute_url(self):
        return reverse('ide-detail', kwargs={'pk': self.pk})

    def jumlah_suka(self):
        return self.suka.count()

class Komentar(models.Model):
    ide = models.ForeignKey(Ide, related_name='komentar', on_delete=models.CASCADE)
    penulis = models.ForeignKey(User, on_delete=models.CASCADE)
    isi = models.TextField()
    dibuat_pada = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-dibuat_pada']

    def __str__(self):
        return f'Komentar oleh {self.penulis.username} di {self.ide.judul}'