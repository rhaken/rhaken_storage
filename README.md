# Rhaken Storage
Alikasi penyimpanan Barang Rhaken
https://rhakenstorage.adaptable.app/main/

## Implementasi
### 1. Membuat proyek Django baru
1.Membuat _virtual environment_ dengan perintah `python -m venv env` dan mengaktifkannya dengan perintah `env\Scripts\activate.bat`.
2.Memasang _dependencies_ dengan perintah `pip install -r requirements.txt`.
3.Membuat direktori baru bernama `rhaken_storage`, lalu menambahkan berkas `requirements.txt` di dalam direktori tersebut yang berisi:
```
django
gunicorn
whitenoise
psycopg2-binary
requests
urllib3
```
Berkas itu berisi _dependencies_ yang akan digunakan.
Lalu, saya menginstall dengan perintah `pip install -r requirements.txt`.

4.membuat proyek baru, jalankan perintah `django-admin startproject rhaken_storage .`. Perintah itu akan membuat direktori proyek baru (beserta dengan berkas-berkas yang dibutuhkan) di dalam direktori utama saya.

### 2. Membuat aplikasi `main` pada proyek tersebut
1.Jalankan perintah `python manage.py startapp main` untuk membuat aplikasi dengan nama `main`.
2.Mendaftarkan aplikasi **main** ke dalam proyek dengan membuka berkas `settings.py`, lalu masukkan **main** ke dalam variable **INSTALLED_APPS**
```python
INSTALLED_APPS = [
    ...,
    'main',
    ...
]
```

### 3. Melakukan _routing_ agar dapat menjalankan aplikasi
1.membuat `urls.py` di dalam direktori `main` yang berisi:
```python
from django.urls import path
from main.views import show_main

app_name = 'main'

urlpatterns = [
    path('', show_main, name='show_main'),
]
```
Berkas ini berguna untuk mengatur rute URL yang terkait pada aplikasi `main`.
2.membuka `urls.py` di dalam direktori proyek, lalu memodifikasi _code_-nya menjadi seperti ini:
```python
...
from django.urls import path, include
...
urlpatterns = [
    ...
    path('main/', include('main.urls')),
    ...
]
```
Berkas ini berguna untuk mengimport rute URL dari aplikasi `main` ke dalam `urls.py` proyek.
### 4. Membuat model pada aplikasi `main`
1.membuka `models.py` yang ada di direktori aplikasi, lalu mengisinya dengan _code_ berikut:
```python
from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=255)
    amount = models.IntegerField()
    description = models.TextField()
```
2.saya melakukan migrasi model untuk melacak perubahan pada model basis data saya. Hal itu dilakukan dengan cara menjalankan perintah `python manage.py makemigrations`, setelah itu `python manage.py migrate`.

### 5. Membuat fungsi pada `views.py`
1.membuat direktori `templates` pada direktori aplikasi `main`. Di dalam direktori tersebut, saya menambahkan berkas `main.html` berisi _HTML code_ yang ingin saya tampilkan. Pada `views.py`, saya dapat mengembalikan `main.html` tesebut dengan memodifikasi _code_:
```python
from django.shortcuts import render

# Create your views here.
def show_main(request):
    context = {
        'name': 'Rhaken Shaquille Akbar Yanuanda',
        'class': 'PBP B'
    }
    return render(request, "main.html", context)
```

### 6. Melakukan _deployment_
1.Pada adaptable, pilih opsi _deploy a new app_. Karena saya memilih -_deploy_ _repository_ `rhaken_storage`. 
2.Pilih _Python App Template_ sebagai _template deployment_. 
3.pilih PostgreSQL. 
4.Sesuaikan versi python dengan versi lokal. Dan masukan `python manage.py migrate && gunicorn rhaken_storage.wsgi` pada _Start Command_. Tentukan nama applikasi dan checklist _HTTP Listener on PORT_.

## Bagan
![basic-django](https://github.com/rhaken/rhaken_storage/assets/39646450/315ab361-b1bf-47bc-9473-178a512237c5)
1._Client_ meminta untuk membuka suatu situs kepada _browser_
2.yang akan mengirimkan HTTP _request_
3.lalu diteruskan ke sistem _routing_ dan mencari pola URL yang sesuai dengan permintaan _client_
4.Django akan memanggil fungsi yang terkait dalam berkas `views.py` yang telah terhubung dengan URL tersebut. `views.py` akan mengambil data yang dibutuhkan pada `models.py`. Setelah itu
5.`views.py` akan mengirimkan _webpage_ dalam bentuk HTML yang terdapat pada direktori `templates`. Terakhir, HTTP _request_ akan dikembalikan oleh view menjadi HTTP _response_ berupa HTML _page_.

## Virtual Environment
Fungsi _virtual environment_ adalah untuk memisahkan _packages_ dan _dependencies_ untuk setiap proyek kita, sehingga setiap proyek kita dapat menggunakan paket _Python_ yang berbeda-beda. Kita sebenarnya bisa saja membuat proyek tanpa _virtual environment_, tetapi akan sangat berisiko. Tanpa virtual environment, semua paket Python yang saya instal akan berada dalam lingkungan Python global di sistem saya. Ini dapat menyebabkan konflik jika dua proyek berbeda memerlukan versi yang berbeda dari paket yang sama. Dengan virtual environment, saya dapat mengisolasi dependensi untuk setiap proyek, mencegah konflik tersebut.

## MVC, MVT, MVVM
### 1. MVC (Model-View-Controller)
1 Model: Komponen ini mewakili data dan logika aplikasi.
2 View: Komponen ini bertanggung jawab untuk menampilkan informasi kepada pengguna dan menerima input dari mereka.
3 Control: Komponen ini bertindak sebagai penghubung antara Model dan View. Ini mengatur alur kontrol, dan mengolah input dari pengguna.

Pada arsitektur MVC, Model dan View biasanya tidak mengetahui satu sama lain secara langsung, dan komunikasi antara keduanya diatur melalui Controller.
### 2. MVT (Model-View-Template)
1 Model: Komponen ini mewakili data dan logika aplikasi.
2 View: Komponen ini adalah bagian yang menentukan apa yang harus ditampilkan kepada pengguna.
3 Template: Ini adalah bagian yang menangani tampilan HTML. Template mengambil data dari Model dan menggabungkannya dengan HTML untuk membuat tampilan yang akhir kepada pengguna.

Pola MVT digunakan khususnya dalam pengembangan web dengan framework Django, yang secara konseptual mirip dengan pola MVC, tetapi dengan istilah yang sedikit berbeda.
### 3. MVVM (Model-View-ViewModel)
1 Model: Seperti dalam pola-pola lain, Model mewakili data dan logika aplikasi.
2 View: Komponen ini bertanggung jawab untuk menampilkan informasi kepada pengguna.
3 ViewModel: Ini berfungsi sebagai perantara antara Model dan View. ViewModel juga mengelola input dari pengguna dan mengirimkannya ke Model jika diperlukan.

MVVM adalah pola arsitektur yang umum digunakan dalam pengembangan aplikasi berbasis antarmuka pengguna (UI).
