# Tugas 6
## Implementasi
### 1. Membuat Fungsi Create Products, Get Products, Item Menggunakan AJAX
```javascript
async function getProducts() {
    return fetch("{% url 'main:get_product_json' %}", {
        method: 'GET',
        headers: {
            'X-Requested-With': 'XMLHttpRequest'
        }
    }).then((res) => res.json());
    }

function addProduct() {
    fetch("{% url 'main:add_product_ajax' %}", {
        method: "POST",
        body: new FormData(document.querySelector('#form'))
    }).then(refreshProducts);

    document.getElementById("form").reset();
    return false;
}
document.getElementById("button_add").onclick = addProduct;

```

Lalu di views.py definisikan fungsinya
```python
@csrf_exempt
def add_product_ajax(request):
    if request.method == 'POST':
        name = request.POST.get("name")
        amount = request.POST.get("amount")
        description = request.POST.get("description")
        user = request.user

        new_product = Item(name=name, amount=amount, description=description, user=user)
        new_product.save()

        return HttpResponse(b"CREATED", status=201)

    return HttpResponseNotFound()

def get_product_json(request):
    product_item = Item.objects.filter(user=request.user)
    return HttpResponse(serializers.serialize('json', product_item))
```

Tambahkan juga masing-masing path pada `urls.py`

### 2. Membuat Script untuk Menampilkan Item
```javascript
async function refreshProducts() {
    const productContainer = document.getElementById("product_container");
    productContainer.innerHTML = "";

    const products = await getProducts();

    products.forEach((item) => {
        // Create a Bootstrap card for each product
        const card = document.createElement("div");
        card.classList.add("col-4"); // Adjust the column size as needed

        card.innerHTML = `
            <div class="card">
                <div class="card-body">
                    <h5 class="card-title">${item.fields.name}</h5>
                    <p class="card-text">Amount: ${item.fields.amount}</p>
                    <p class="card-text">Description: ${item.fields.description}</p>
                </div>
            </div>
        `;

        productContainer.appendChild(card);
    });
}
```

merubah `main.html`, bagian menampilkan card menjadi `<div class="row" id="product_container"></div> `.

### 3. Membuat Modal Form dalam Menambahkan Item
```javascript
<div class="modal fade" id="exampleModal" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true">
    <div class="modal-dialog">
        <div class="modal-content">
            <div class="modal-header">
                <h1 class="modal-title fs-5" id="exampleModalLabel">Add New Item</h1>
                <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
            </div>
            <div class="modal-body">
                <form id="form" onsubmit="return false;">
                    {% csrf_token %}
                    <div class="mb-3">
                        <label for="name" class="col-form-label">Name:</label>
                        <input type="text" class="form-control" id="name" name="name"></input>
                    </div>
                    <div class="mb-3">
                        <label for="amount" class="col-form-label">Amount:</label>
                        <input type="number" class="form-control" id="amount" name="amount"></input>
                    </div>
                    <div class="mb-3">
                        <label for="description" class="col-form-label">Description:</label>
                        <textarea class="form-control" id="description" name="description"></textarea>
                    </div>
                </form>
            </div>
            <div class="modal-footer">
                <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                <button type="button" class="btn btn-primary" id="button_add" data-bs-dismiss="modal">Add Item</button>
            </div>
        </div>
    </div>
</div>
```

menambahkan button add item by AJAX yang baru
```javascript
<button type="button" class="btn btn-primary" data-bs-toggle="modal" data-bs-target="#exampleModal">Add Item by AJAX</button>
```



## Perbedaan _Asynchronous Programming_ dengan _Synchronous Programming_
Pemrograman asinkron dan pemrograman sinkron adalah dua metode utama dalam pengembangan perangkat lunak yang memiliki perbedaan signifikan dalam pengelolaan dan eksekusi tugas. Dalam pemrograman asinkron, tugas-tugas dieksekusi secara berurutan, yang berarti setiap tugas harus menunggu tugas sebelumnya untuk selesai sebelum dapat dimulai. Situasi ini dapat mengakibatkan kinerja aplikasi yang kurang responsif, terutama saat menangani tugas yang memakan waktu lama seperti operasi jaringan atau berkas.

Di sisi yang berlawanan, pemrograman asinkron memungkinkan tugas-tugas untuk berjalan secara mandiri tanpa harus menunggu satu sama lain. Akibatnya, aplikasi dapat menjalankan tugas-tugas lain sambil menunggu penyelesaian tugas yang memerlukan waktu lebih lama. Ini menghasilkan peningkatan responsivitas dan efisiensi aplikasi, terutama dalam situasi di mana ada banyak operasi non-blocking yang perlu dijalankan, seperti yang sering terjadi dalam aplikasi web yang harus menangani sejumlah besar permintaan dari pengguna. Pemrograman asinkron sering melibatkan penggunaan konsep seperti callback, promise, atau async/await untuk mengelola eksekusi tugas-tugas tanpa menghalangi pemrosesan utama.

## Paradigma Event-driven Programming
Event-driven adalah jenis pendekatan dalam pengembangan perangkat lunak yang serupa dengan pemanfaatan event listener dalam bahasa seperti Java. Implementasi paradigma pemrograman event-driven dalam JavaScript memungkinkan pengembang untuk menentukan tindakan atau fungsi yang akan dijalankan saat terjadi sebuah peristiwa, tanpa harus menjalankan kode secara berurutan. Sebagai contoh, ketika seorang pengguna melakukan klik pada sebuah tombol, JavaScript dapat merespons dengan menjalankan kode yang telah ditentukan untuk menangani peristiwa tersebut. Dengan demikian, paradigma ini memungkinkan pembuatan aplikasi web yang interaktif dan dinamis, di mana respons terhadap peristiwa pengguna dapat diprogram dengan fleksibilitas dan efisiensi.

Contohnya :  tombol yang akan menjalankan suatu tindakan saat ditekan, seperti tombol "Tambah Item melalui AJAX," yang akan memicu fungsi addItem saat ditekan.

## Penerapan Asynchronous Programming pada AJAX
Asynchronous programming pada AJAX (Asynchronous JavaScript and XML) adalah teknik yang digunakan untuk mengirim dan menerima data dari server web tanpa menghentikan atau memblokir eksekusi kode JavaScript di browser. Saat sebuah permintaan (request) AJAX dikirim ke server, JavaScript dapat melanjutkan eksekusi kode lainnya tanpa harus menunggu respon dari server. Ketika respon dari server tiba, JavaScript akan menjalankan callback function yang telah ditentukan, memungkinkan tindakan-tindakan selanjutnya seperti pembaruan tampilan atau manipulasi data. Ini adalah prinsip fundamental dalam pemrograman berbasis peristiwa (event-driven programming) yang sangat berguna dalam pengembangan aplikasi web yang responsif. Dengan menggunakan AJAX, pengguna dapat berinteraksi dengan situs web tanpa harus menunggu lama untuk setiap permintaan server selesai diproses, yang akan meningkatkan pengalaman pengguna secara keseluruhan.

## Penerapan AJAX Menggunakan Fetch API vs Library JQuery
Penerapan AJAX dengan menggunakan Fetch API dan jQuery adalah dua pendekatan yang berbeda dalam mengirim permintaan HTTP asynchronous ke server dan memanipulasi data yang diterima. Pilihan antara keduanya tergantung pada kebutuhan proyek dan preferensi pengembang.

Fetch API adalah bagian dari JavaScript modern yang menawarkan antarmuka yang kuat untuk mengelola permintaan HTTP. Ia lebih ringan daripada jQuery, memungkinkan pengembang untuk mengirim permintaan dan mengelola respons dengan lebih langsung. Fetch API mendukung Promise, yang membuatnya mudah untuk menangani respons async dan chaining berbagai operasi, serta mengintegrasikan lebih baik dengan ES6 dan ekosistem JavaScript modern. Namun, implementasi dan penggunaannya mungkin sedikit lebih rumit daripada jQuery untuk pengembang yang belum terbiasa dengan aspek-aspek ini.

Sebaliknya, jQuery adalah perpustakaan JavaScript yang telah lama ada dan cukup populer. Ia menyediakan antarmuka yang lebih sederhana dan mudah digunakan untuk AJAX, dengan banyak fitur dan fungsi yang telah siap digunakan. Ini memungkinkan pengembang untuk mengirim permintaan AJAX dengan lebih sedikit kode. Namun, karena itu menyediakan banyak fitur yang mungkin tidak digunakan dalam proyek tertentu, ini bisa mempengaruhi kinerja dan memuat waktu aplikasi web.

# Tugas 5
## Implementasi
Pada implementasi, saya memilih untuk menggunakan framework bootstrap.

Beberapa komponen bootstrap pada page `main` yang saya gunakan adalah.

### Login:

Halaman login telah diperbarui untuk memmbuat tampilan yang lebih terpusat baik secara vertikal maupun horizontal. Ini membuat tampilannya lebih menarik dan lebih baik untuk pengguna.
Sekarang, label dan bidang masukan pada formulir login disusun dalam dua kolom yang terlihat rapi. Kolom pertama untuk label, sementara kolom kedua untuk bidang masukan. Ini mempermudah pengguna untuk melihat dan mengisi formulir.
Selain itu, ada jarak vertikal yang ditambahkan setelah setiap bidang masukan dengan menggunakan jeda baris (<br>) agar tampilannya tidak terlalu padat.
Halaman Pendaftaran (Register Page):

### Register:

Halaman pendaftaran juga telah diperbarui dengan peningkatan tampilan yang mencakup penataan yang lebih baik baik secara vertikal maupun horizontal. Ini membuat halaman terlihat lebih menarik dan lebih mudah dinavigasi.

### create_product:

Formulir "Tambah Item Baru" sekarang tampil lebih teratur dengan penempatan yang tepat baik secara vertikal maupun horizontal. Ini dilakukan untuk memastikan pengalaman yang lebih baik.
Tampilan formulir ini responsif, artinya akan menyesuaikan ukuran layar. Setiap kolom untuk memasukkan data ditempatkan sejajar dengan labelnya, sehingga tampilannya lebih seimbang.
Untuk membuat tampilan lebih rapi dan sejajar secara horizontal, jeda baris tidak lagi digunakan 
Pada formulir pendaftaran, label dan bidang masukan disusun dalam dua kolom yang terlihat rapi. Hal ini memudahkan pengguna dalam mengisi formulir dengan jelas.
menambahkan jarak vertikal dengan menggunakan jeda baris (<br>) setelah setiap bidang masukan agar tampilannya lebih teratur.
Formulir "Tambah Item Baru" (Add New Item Form):

### Main:

Pada halaman "main," yang menggambarkan halaman inventori, menambahkan Card Bootstrap untuk menampilkan setiap item secara lebih menarik secara visual.
Setiap produk sekarang ditampilkan dalam komponen Card Bootstrap tersendiri, memberikan tampilan yang terstruktur dan terorganisir untuk menampilkan informasi produk.
Di dalam setiap kartu, nama produk, jumlah, dan deskripsi produk ditampilkan secara terpisah, memberikan bagian yang jelas dan terpisah untuk setiap informasi.
Tiga tombol, yaitu "Tambah," "Kurang," dan "Hapus," telah disertakan di dalam setiap kartu untuk memungkinkan pengguna melakukan tindakan pada setiap produk.
Tombol-tombol ini di-styling dengan kelas tombol Bootstrap (btn btn-primary, btn btn-warning, dan btn btn-danger) untuk antarmuka yang konsisten dan ramah pengguna.
Tata letak kartu tersebut responsif dan menyesuaikan dengan berbagai ukuran layar, sehingga cocok untuk berbagai perangkat dan resolusi layar.
Baris terakhir dari setiap kartu, yang mencakup tombol-tombol ("Tambah," "Kurang," dan "Hapus"), memiliki warna latar belakang yang berbeda (orange) untuk membedakannya dari bagian Card lainnya dan menarik perhatian ke tombol aksi.


## Manfaat Element Sector dan Waktu Penggunaannya
### 1. Element Sector
Selector elemen digunakan untuk memilih semua elemen dengan jenis tertentu dalam dokumen HTML. Ini berguna ketika Anda ingin menerapkan gaya yang sama ke semua elemen dari jenis yang sama dalam dokumen.
### 2. ID Selector
Selector ID digunakan untuk memilih elemen berdasarkan atribut id yang bersifat unik. Ini berguna ketika Anda perlu mengacu pada elemen tertentu dalam dokumen dan memastikan bahwa elemen tersebut memiliki id yang hanya ada satu di dalam dokumen tersebut.
### 3. Class Selector
Selector kelas digunakan untuk memilih elemen berdasarkan atribut kelas yang telah ditentukan. Penggunaan ini berguna ketika Anda ingin menerapkan gaya atau fungsi yang serupa pada beberapa elemen dalam dokumen.

## HTML5 Tag
HTML5 adalah versi terbaru dari bahasa markup HTML (Hypertext Markup Language) yang digunakan untuk membuat halaman web. HTML5 menyediakan sejumlah tag (elemen) baru yang memungkinkan saya untuk membuat konten website yang lebih interaktif.

`<header>`: Untuk bagian atas halaman web, seperti judul dan logo.

`<nav>`: Untuk menu navigasi dalam halaman web.

`<section>`: Menandai bagian konten yang berdiri sendiri.

`<article>`:  Untuk mengelompokkan konten yang berdiri sendiri.

`<video>`: Untuk menyisipkan pemutaran video ke dalam halaman web.

## Perbedaan antara _margin_ dan _padding_
Margin dan padding memiliki fungsi yang sama dalam mengatur tata letak, namun perbedaan utamanya adalah bagaimana mereka mengatur ruang. Margin adalah ruang di luar batas elemen tersebut yang memisahkannya dari elemen-elemen sekitarnya, sedangkan padding adalah ruang di dalam batas elemen tersebut, yang berada antara kontennya dan batasnya sendiri. Selain itu, perlu dicatat bahwa margin dapat berdampak pada tata letak elemen-elemen di seluruh halaman web, sementara padding hanya memengaruhi tata letak elemen itu sendiri tanpa memengaruhi elemen-elemen di luarnya.

## Perbedaan _framework_ CSS Tailwind dan Bootstrap
Bootstrap adalah suatu framework CSS yang lebih tradisional yang menawarkan berbagai komponen siap pakai seperti tombol, jumbotron, dan menu navigasi, sehingga mempermudah dalam pengembangan web yang cepat. Bootstrap memiliki gaya bawaan yang khas yang dapat menghasilkan desain yang serupa di banyak situs web.

Sementara itu, Tailwind CSS adalah suatu kerangka kerja CSS yang lebih modern dan berbasis pada kelas utilitas. Ketika Anda menggunakan Tailwind, Anda menggabungkan kelas-kelas yang telah ditentukan sebelumnya untuk mengatur tata letak, warna, dan gaya elemen-elemen. Pendekatan ini memberikan fleksibilitas yang besar dan memungkinkan Anda mengontrol setiap aspek desain dengan sangat rinci.

Jadi, secara singkat, Anda bisa menggunakan Bootstrap jika ingin pengembangan web yang cepat dengan desain yang seragam, dan Anda dapat memilih Tailwind jika Anda ingin fleksibilitas maksimum dalam menentukan desain situs web Anda.

# tugas 4
### 1. Membuat Fungsi Registrasi
Dengan memanfaatkan UserCreationForm bawaan django, pengguna baru dapat mendaftar dengan mudah di situs web Anda tanpa harus menulis kode dari awal. dengan membuat fungsi untuk register seperti dibawah
```python
def register(request):
    form = UserCreationForm()

    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your account has been successfully created!')
            return redirect('main:login')
    context = {'form':form}
    return render(request, 'register.html', context)
```

Selanjutnya, membuat HTML untuk menampilkan form registrasinya yang akan saya taruh di `main/templates`
```html
{% extends 'base.html' %}

{% block meta %}
    <title>Register</title>
{% endblock meta %}

{% block content %}  

<div class = "login">
    
    <h1>Register</h1>  

        <form method="POST" >  
            {% csrf_token %}  
            <table>  
                {{ form.as_table }}  
                <tr>  
                    <td></td>
                    <td><input type="submit" name="submit" value="Daftar"/></td>  
                </tr>  
            </table>  
        </form>

    {% if messages %}  
        <ul>   
            {% for message in messages %}  
                <li>{{ message }}</li>  
                {% endfor %}  
        </ul>   
    {% endif %}

</div>  

{% endblock content %}
```
### 2. Membuat Fungsi Login
mengimport _authenticate_ dari Django, user yang melakukan login akan diautentikasi secara otomatis. dan memanfaatkan fungsi itu pada fungsi login
```python
def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('main:show_main')
        else:
            messages.info(request, 'Sorry, incorrect username or password. Please try again.')
    context = {}
    return render(request, 'login.html', context)
```
dan menambahkan HTML nya pada main seperti kode dibawah
```html
{% extends 'base.html' %}

{% block meta %}
    <title>Login</title>
{% endblock meta %}

{% block content %}

<div class = "login">

    <h1>Login</h1>

    <form method="POST" action="">
        {% csrf_token %}
        <table>
            <tr>
                <td>Username: </td>
                <td><input type="text" name="username" placeholder="Username" class="form-control"></td>
            </tr>
                    
            <tr>
                <td>Password: </td>
                <td><input type="password" name="password" placeholder="Password" class="form-control"></td>
            </tr>

            <tr>
                <td></td>
                <td><input class="btn login_btn" type="submit" value="Login"></td>
            </tr>
        </table>
    </form>

    {% if messages %}
        <ul>
            {% for message in messages %}
                <li>{{ message }}</li>
            {% endfor %}
        </ul>
    {% endif %}     
        
    Don't have an account yet? <a href="{% url 'main:register' %}">Register Now</a>

</div>

{% endblock content %}
```

### 3. Membuat Fungsi Logout
Membuat fungsi logout, yang juga akan mendelete cookies jika user telah logout.
```python
def logout_user(request):
    logout(request)
    return redirect('main:login')
```
Menambahkan tombol logout pada HTML di main.html.
```html
<a href="{% url 'main:logout' %}">
    <button>
        Logout
    </button>
</a>
```

### 4. Menghubungkan Model Item dan User
Untuk menghubungkan User dengan Item pada Django, dapat menggunakan interface User pada django.contrib.auth.models. _Code_ ini menghubungkan satu produk dengan satu User melalui sebuah relationship, dimana sebuah produk pasti terasosiasikan dengan seorang User.
```python
class Item(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    name = models.CharField(max_length=255)
    amount = models.IntegerField()
    description = models.TextField()
```
juga perlu merubah `create_item` yang ada pada `views.py`.
```python
def create_item(request):
    form = ItemForm(request.POST or None)

    if form.is_valid() and request.method == "POST":
        item = form.save(commit=False)
        item.user = request.user
        item.save()
        return HttpResponseRedirect(reverse('main:show_main'))

    context = {'form': form}
    return render(request, "create_item.html", context)
```
Parameter `commit = False` adalah agar objek tidak langsung tersimpan ke database. Hal tersebut membuat kita bisa untuk memodifikasi terlebih dahulu objek tersebut sebelum disimpan ke database. Pada kasus ini, kita akan mengisi field user dengan objek User dari return value request.user yang sedang terotorisasi untuk menandakan bahwa objek tersebut dimiliki oleh pengguna yang sedang login. 

### 5. Menampilkan Informasi Pengguna dan Menerapkan _Cookies_
Untuk menampilkan informasi pengguna yang sudah login, saya akan menambahkan _cookies_ untuk melihat kapan terakhir kali user melakukan login. Caranya adalah dengan sedikit memodif pada fungsi `login_user`.
```python
...

if user is not None:
    login(request, user)
    response = HttpResponseRedirect(reverse("main:show_main")) 
    response.set_cookie('last_login', str(datetime.datetime.now()))
    return response

...  
```
Saya juga perlu menambah variabel pada context, yaitu `'last_login': request.COOKIES['last_login']`, dan perlu memodif pada fungsi `logout_user`.
```python
def logout_user(request):
    logout(request)
    response = HttpResponseRedirect(reverse('main:login'))
    response.delete_cookie('last_login')
    return response
```
Terakhir, pada `main.html`, waktu terakhir login akan disimpan pada variabel `last_login` dan saya tinggal menampilkannya.

## Dummy Account
![image](https://github.com/rhaken/rhaken_storage/assets/39646450/32abebc3-e8d6-48d9-bc3b-aef6bf94e5cc)
![image](https://github.com/rhaken/rhaken_storage/assets/39646450/cd7295a4-cc3d-44f8-9d1d-22c41445f848)

## Penjelasan Django UserCreationForm
UserCreationForm dalam Django adalah sebuah formulir standar yang telah disediakan oleh framework web Python Django. Fungsinya adalah untuk mempermudah pembuatan akun pengguna dalam aplikasi web yang menggunakan Django. UserCreationForm secara spesifik dibuat untuk mengumpulkan informasi yang diperlukan, seperti nama pengguna (username) dan kata sandi (password), untuk membuat dan mendaftarkan pengguna baru dalam database Django.

Salah satu keunggulan dari formulir ini adalah kemudahannya dalam penggunaan dan kemampuan untuk melakukan validasi otomatis guna memastikan bahwa data yang dimasukkan oleh pengguna sesuai dengan persyaratan yang telah ditetapkan, seperti panjang kata sandi atau kompleksitas kata sandi.

Namun, ada beberapa kelemahan yang perlu diingat. Tampilan bawaan formulir mungkin tidak selalu cocok dengan desain visual aplikasi Anda, sehingga perlu penyesuaian tambahan. Selain itu, untuk aplikasi yang sangat peduli terhadap keamanan, perlu adanya lapisan keamanan tambahan yang harus diterapkan.

## Perbedaan antara Autentikasi dan Otorisasi dalam Konteks Django
Autentikasi dan otorisasi adalah dua konsep yang terkait dan berperan penting dalam mengatur cara pengguna memanfaatkan akses ke aplikasi. Kedua konsep ini memiliki peran kunci dalam menjaga tingkat keamanan, privasi, dan pengelolaan hak akses pengguna.

Autentikasi adalah tahap awal yang melibatkan proses verifikasi identitas pengguna yang ingin masuk ke aplikasi, biasanya dengan menggunakan kombinasi username dan password. Ketika proses autentikasi berhasil, Django akan memberikan izin akses ke bagian yang sesuai dalam aplikasi berdasarkan peran atau permissi pengguna, yang disebut juga dengan istilah otorisasi.

Otorisasi, di sisi lain, adalah tahap berikutnya yang menentukan apa yang diizinkan atau tidak oleh pengguna yang telah berhasil diautentikasi. Ini mengendalikan hak akses ke konten khusus atau tindakan tertentu dalam aplikasi. Django akan memeriksa izin yang dimiliki pengguna untuk memastikan bahwa mereka memiliki izin yang diperlukan untuk melaksanakan tindakan tersebut. Jika pengguna memiliki izin yang sesuai, maka mereka diberikan akses; sebaliknya, jika tidak, mereka akan diberikan penolakan akses.

## Penjelasan tentang _Cookies_
Dalam kerangka aplikasi web, cookies adalah berkas kecil yang berfungsi untuk menyimpan informasi pada perangkat pengguna. Cookies digunakan untuk mempertahankan informasi tertentu di perangkat pengguna, seperti data sesi, preferensi, atau informasi lain yang relevan dalam konteks pengalaman pengguna. Django, sebagai contoh, memanfaatkan cookies untuk mengelola data sesi pengguna, seperti ID sesi, yang memungkinkan aplikasi web untuk menjaga status sesi pengguna yang sedang aktif.

## Keamanan _Cookies_
Penggunaan cookies dalam pengembangan web pada umumnya dianggap aman secara bawaan karena mereka berfungsi untuk menyimpan data sesi atau preferensi pengguna, meningkatkan pengalaman pengguna secara keseluruhan. Meskipun demikian, ada potensi risiko yang harus diwaspadai, terutama terkait dengan cookies pihak ketiga yang dapat digunakan untuk melacak aktivitas pengguna secara online tanpa izin mereka. Ini dapat mengancam privasi pengguna dan memicu masalah keamanan jika data yang tersimpan dalam cookies tersebut disalahgunakan.


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
