# tugas 3
### 1. Membuat Input Form
Membuat `forms.py` pada direktori main dengan isi:
```python
from django.forms import ModelForm
from main.models import Item

class ProductForm(ModelForm):
    class Meta:
        model = Item
        fields = ['name', 'amount', 'description']
```
membuat fungsi `create_product` untuk membuat formulir yang secara otomatis menyimpan data produk yang disubmit
```python
def create_product(request):
    form = ProductForm(request.POST or None)

    if form.is_valid() and request.method == "POST":
        form.save()
        return HttpResponseRedirect(reverse('main:show_main'))

    context = {'form': form}
    return render(request, "create_item.html", context)
```
membuat file `create_item.html` yang diletakkan di direktori `templates`, file ini adalah tampilan form kepada user.
```html
{% extends 'base.html' %} 

{% block content %}
<h1>Add New Item</h1>

<form method="POST">
    {% csrf_token %}
    <table>
        {{ form.as_table }}
        <tr>
            <td></td>
            <td>
                <input type="submit" value="Add Item"/>
            </td>
        </tr>
    </table>
</form>

{% endblock %}
```

menambahkan path nya pada `urls.py` di direktori `main`
```python
path('create-product', create_item, name='create_item'),
```
### 2. Menampilkan Objek yang Ditambahkan (dalam Format HTML, XML, JSON, XML by ID, dan JSON by ID)
#### HTML
merubah fungsi `show_main` pada `views.py` agar data produk dapat ditampilkan.
```python
def show_main(request):
    items = Item.objects.all()
    context = {
        'name': 'Rhaken Shaquille Akbar Yanuanda',
        'class': 'PBP B',
        'products': products, # Modifikasi di sini
    }

    return render(request, "main.html", context)
```
Merubah `main.html` untuk menampilkan objeknya.
```html
...
<!-- Untuk menampilkan tabel -->
<table>
    <tr>
        <th>Name</th>
        <th>Amount</th>
        <th>Description</th>
    
    </tr>

    {% comment %} Berikut cara memperlihatkan data produk di bawah baris ini {% endcomment %}

    {% for product in products %}
        <tr>
            <td>{{product.name}}</td>
            <td>{{product.amount}}</td>
            <td>{{product.description}}</td>
            
        </tr>
    {% endfor %}
</table>

<br />

<!-- Untuk button Add New Item -->
<a href="{% url 'main:create_item' %}">
    <button>
        Add New Item
    </button>
</a>
```


#### XML dan JSON
menambahkan fungsi `show_xml` dan `show_json` yang akan return HttpResponse berisi data yang sudah diserialize menjadi XML dan JSON.
```python
def show_xml(request):
    data = Item.objects.all()
    return HttpResponse(serializers.serialize("xml", data), content_type="application/xml")

def show_json(request):
    data = Item.objects.all()
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")
```

#### XML dan JSON (by ID)
Kurang lebih sama seperti yang tanpa id.
```python
def show_xml_by_id(request, id):
    data = Item.objects.filter(pk=id)
    return HttpResponse(serializers.serialize("xml", data), content_type="application/xml")

def show_json_by_id(request, id):
    data = Item.objects.filter(pk=id)
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")
```

### 3. Membuat _Routing_ URL
menambahkan path nya pada `urls.py`.:
```python
from django.urls import path
from main.views import show_main, create_item, show_xml, show_json, show_xml_by_id, show_json_by_id 

app_name = 'main'

urlpatterns = [
    path('', show_main, name='show_main'),
    path('create-product', create_product, name='create_product'),
    path('xml/', show_xml, name='show_xml'),
    path('json/', show_json, name='show_json'), 
    path('xml/<int:id>/', show_xml_by_id, name='show_xml_by_id'),
    path('json/<int:id>/', show_json_by_id, name='show_json_by_id'), 
]
```
## Perbedaan Form POST dan GET
# Metode GET

Metode GET adalah salah satu dari dua metode utama yang digunakan dalam protokol HTTP untuk mengirim permintaan dan menerima respons dari server. Berikut adalah beberapa karakteristik utama dari metode GET:

- **Keamanan**: Kurang aman karena data terlihat di URL dan dapat dilihat oleh siapa saja yang melihat riwayat penelusuran atau tautan yang digunakan. Tidak aman untuk data sensitif.

- **Ukuran Data**: Terbatas pada panjang URL tertentu, cocok untuk data yang relatif kecil. Terlalu banyak data dalam URL dapat menyebabkan masalah kompatibilitas dan keamanan.

- **Cache**: Dapat di-cache oleh browser dan server karena data ada di URL, yang dapat meningkatkan kinerja. Ini bisa berguna untuk mempercepat pengambilan data yang sama secara berulang-ulang.

# Metode POST

Metode POST adalah metode HTTP lainnya yang digunakan untuk mengirim permintaan ke server, tetapi memiliki karakteristik yang berbeda dari metode GET. Berikut adalah beberapa karakteristik utama dari metode POST:

- **Keamanan**: Lebih aman karena data tidak terlihat di URL. Cocok untuk data sensitif yang tidak boleh terlihat oleh pihak ketiga yang tidak sah.

- **Ukuran Data**: Tidak ada batasan ukuran data, cocok untuk data besar seperti file. Ini membuatnya ideal untuk mengirim data yang besar atau kompleks ke server.

- **Cache**: Tidak di-cache oleh browser atau server secara default karena data dianggap sensitif. Ini memastikan bahwa data yang dikirimkan dengan metode POST tidak akan disimpan di cache dan akan selalu diminta ulang dari server.
  
## Perbedaan XML, JSON, dan HTML dalam Pengiriman Data
XML (eXtensible Markup Language) menggunakan sintaks berbasis tag (mirip seperti HTML). Ini memungkinkan untuk mendefinisikan struktur data yang sangat fleksibel dan kompleks, tetapi jadi lebih sulit dibaca oleh manusia. XML dirancang untuk menjadi format data yang digunakan oleh komputer dan aplikasi, bukan untuk keterbacaan manusia. 

HTML (Hypertext Markup Language) adalah bahasa yang digunakan untuk membangun tampilan web dan memiliki tujuan utama untuk mengorganisasi dan menampilkan konten di browser. Ini memiliki struktur dasar yang berbeda dan **biasanya tidak digunakan untuk pengiriman data** dalam konteks yang sama seperti XML atau JSON. HTML digunakan untuk tujuan yang berbeda dan memiliki fokus utama pada tampilan dan interaksi dengan pengguna.

JSON (JavaScript Object Notation) adalah adalah format data yang digunakan untuk mengirim dan menyimpan informasi dalam bentuk teks yang mudah dibaca oleh manusia dan mudah diproses oleh komputer. JSON umum digunakan dalam pengembangan web dan aplikasi, khususnya dalam pertukaran data antara browser dan server, karena komunikasi web umumnya berbasis JavaScript.


## Pentingnya JSON dalam Pertukaran Data antara Aplikasi Web Modern
* JSON menggunakan sintaks yang lebih sederhana dan mudah dibaca oleh manusia, menggunakan struktur List dan Dictionary pada Python.

* JSON memiliki overhead (jumlah karakter) yang lebih kecil dibandingkan dengan XML dan HTML, sehingga memerlukan lebih sedikit sumber daya untuk mengurai data

* JSON  didukung untuk mengurai dan menghasilkan data oleh banyak bahasa pemrograman. Ini memungkinkan aplikasi yang ditulis dalam bahasa yang berbeda untuk berkomunikasi dengan mudah dan mempertukarkan data dengan format yang sama.

## Screenshot Postman
### 1. HTML
![postmanhtml](https://github.com/rhaken/rhaken_storage/assets/39646450/7757194e-f441-4d1d-8228-13895d3b98d8)
### 2. JSON
![Postman JSON](https://github.com/rhaken/rhaken_storage/assets/39646450/ea494da8-5f33-4806-a06c-85e5fa1de376)
### 3. JSON by ID
![image](https://github.com/rhaken/rhaken_storage/assets/39646450/a1481baf-7a91-4dc6-b413-9a44e8d45ff2)
### 4. XML
![image](https://github.com/rhaken/rhaken_storage/assets/39646450/4fa46922-64aa-476d-a638-8b68a96150b2)
### 5. XML by ID
![image](https://github.com/rhaken/rhaken_storage/assets/39646450/f8d639e6-f71b-4c90-9cc0-744b27f84314)




# Tugas 2
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
