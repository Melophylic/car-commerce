# car-commerce

Nama: Muhammad Nadzim Tahara

NPM: 2306275430

Kelas: PBP C

# Tugas 6

## Manfaat JavaScript dalam pengembangan web

### Interaktif
JavaScript bikin halaman web jadi lebih hidup, bisa bikin animasi, validasi form langsung tanpa harus reload page, dan responsif sama user input.

### Nge-handle logic di browser
Banyak proses bisa dijalankan langsung di browser, jadi server nggak dibebani banget. Hasilnya, web jadi lebih cepat dan smooth buat pengguna.

### Asynchronous 
Dengan async/await, kita bisa ambil data dari server (misalnya API) tanpa nge-freeze aplikasi. Jadi user nggak nunggu loading lama.

### Integrasi API mudah
Bisa ambil data dari server atau API eksternal pakai fetch() atau XMLHttpRequest, terus langsung tampilin di halaman.
Bisa lintas platform: Selain web, JavaScript juga bisa dipake buat bikin aplikasi mobile (kayak pake React Native) atau desktop (Electron).

## Fungsi await dengan fetch()
await fungsinya buat nungguin hasil dari promise yang dihasilkan oleh fetch(). Jadi, kode di bawahnya nggak bakal dieksekusi sebelum data dari fetch() selesai didapatkan. Misalnya pas kamu ambil data dari API, kalau nggak pakai await, kode bakal lanjut jalan meskipun data belum diambil, yang bisa bikin error atau data nggak ada. Intinya biar lebih terstruktur aja alurnya.

## Mengapa kita perlu menggunakan decorator `csrf_exempt` pada view yang akan digunakan untuk AJAX `POST`?
Kenapa perlu csrf_exempt buat AJAX POST? csrf_exempt dipake biar request AJAX yang masuk ke server nggak dicek CSRF token-nya. Biasanya server punya mekanisme keamanan buat ngecek apakah request beneran datang dari form di halaman web kita sendiri (pakai CSRF token). Tapi, kalau kita kirim data lewat AJAX dan nggak sertakan token itu, request bisa ditolak. Makanya pakai csrf_exempt buat nge-bypass cek itu, biar request AJAX bisa diproses.

##  Pada tutorial PBP minggu ini, pembersihan data input pengguna dilakukan di belakang (backend) juga. Mengapa hal tersebut tidak dilakukan di frontend saja?
Kenapa nggak pembersihan data input di frontend aja? Bersihin data di backend itu lebih aman. Kalau cuma di frontend, user bisa manipulasi data pake developer tools atau nge-bypass validasi yang ada di browser. Di backend, kita punya kontrol penuh buat ngecek dan validasi semua input sebelum disimpan atau diproses lebih lanjut. Intinya buat jaga-jaga dari hacker atau serangan yang eksploitasi input (kayak SQL injection, XSS, dsb.).

## Step-by-Step Implementation

Pertama saya mulai dari views.py dengan membuat `add_product_ajax`:
> Method ini menggunakan `@csrf_exempt` dan `@require_POST` sebagai decoratornya untuk keamanan dan memastikan user menggunakan POST
```
@csrf_exempt
@require_POST
def add_product_ajax(request):
    name = strip_tags(request.POST.get("name"))
    price = strip_tags(request.POST.get("price"))
    description = request.POST.get("description")
    user = request.user

    new_product = Product(
        name = name,
        price = price,
        description = description,
        user = user
    )
    new_product.save()

    return HttpResponse(b"CREATED", status=201)
```

Selanjutnya, pada `urls.py` saya membuat pathing untuk method tersebut dan setelah itu saya mengacak-acak `main.html`.

Pertama saya membuat `getProduct()` dan `renderProduct()` pada tag `<script>` agar render dilakukan oleh javascript.
> pertama buat div kosong dengan `id` terlebih dahulu yang menggantikan semua div yang berhubungan dengan render sebelumnya.
```
...
<div id="product-cards"></div>
...
```

> selanjutnya saya buat `async function`:
```
<script>
 async function getProducts() {
            return fetch("{% url 'main:show_json' %}")
            .then((response) => response.json())
        }

        async function renderProducts() {
            document.getElementById("product-cards").innerHTML = "";
            document.getElementById("product-cards").className = "stagger-box";
            const products = await getProducts();

            let htmlString = "";
            let classNameString = "";

            if (products.length === 0) {
                classNameString = "flex flex-col items-center justify-center min-h-[24rem] p-6";
                htmlString = `
                    <div class="flex flex-col items-center justify-center min-h-[24rem] p-6" id="belum-ada">
                        <img src="{% static 'image/caryellow.png' %}" alt="Sad face" class="w-72 mb-[-2rem]"/>
                        <p class="text-center text-white mt-4 font-bold ">Belum ada data pada Car Commerce!</p>
                    </div>
                `
            } else {
                classNameString = "flex flex-wrap columns-1 sm:columns-2 lg:columns-3 gap-6 w-full h-max justify-evenly";
                products.forEach((product) => {
                    const name = DOMPurify.sanitize(product.fields.name);
                    const price = product.fields.price;
                    const description = DOMPurify.sanitize(product.fields.description);
                    htmlString += `
                        <div class="w-full max-w-sm bg-slate-50 border border-gray-200 rounded-lg shadow dark:bg-gray-800 dark:border-gray-700 stagger-box">
                            <a href="#">
                                <img class="p-8 rounded-t-lg" src="{% static 'image/caryellow.png' %}" alt="product image" />
                            </a>
                            <div class="px-5 pb-5">
                                <a href="#">
                                    <h5 class="text-xl font-semibold tracking-tight text-gray
... <---> masih panjang
```
> bisa dilihat disini saya menggunakan `DOMpurify` untuk mengamankan sistem dari *XSS* _(Cross Site Scripting)_.

Setelah itu saya membuat form modal menggunakan AJAX yang letaknya dibawah div kosong baru tadi:
```
<div id="crudModal" tabindex="-1" aria-hidden="true" class="hidden fixed inset-0 z-50 w-full flex items-center justify-center bg-gray-800 bg-opacity-50 overflow-x-hidden overflow-y-auto transition-opacity duration-300 ease-out">
                <div id="crudModalContent" class="relative bg-white rounded-lg shadow-lg w-5/6 sm:w-3/4 md:w-1/2 lg:w-1/3 mx-4 sm:mx-0 transform scale-95 opacity-0 transition-transform transition-opacity duration-300 ease-out">
                    <!-- Modal header -->
                    <div class="flex items-center justify-between p-4 border-b rounded-t">
                    <h3 class="text-xl font-semibold text-gray-900">
                        Add New Product Entry
                    </h3>
                    <button type="button" class="text-gray-400 bg-transparent hover:bg-gray-200 hover:text-gray-900 rounded-lg text-sm p-1.5 ml-auto inline-flex items-center" id="closeModalBtn">
                        <svg aria-hidden="true" class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg">
                        <path fill-rule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clip-rule="evenodd"></path>
                        </svg>
                        <span class="sr-only">Close modal</span>
                    </button>
                    </div>
                    <!-- Modal body -->
                    <div class="px-6 py-4 space-y-6 form-style">
                    <form id="productForm">
                        <div class="mb-4">
                            <label for="name" class="block text-sm font-medium text-gray-700">Name</label>
                            <input type="text" id="name" name="name" class="mt-1 block w-full border border-gray-300 rounded-md p-2 hover:border-yellow-700" placeholder="Enter your product name" required>
                        </div>
                        <div class="mb-4">
                            <label for="price" class="block text-sm font-medium text-gray-700">Price</label>
                            <input type="number" id="price" name="price" class="mt-1 block w-full border border-gray-300 rounded-md p-2 hover:border-yellow-700" required>
                        </div>
                        <div class="mb-4">
                            <label for="description" class="block text-sm font-medium text-gray-700">Description</label>
                            <textarea id="description" name="description" rows="3" class="mt-1 block w-full h-52 resize-none border border-gray-300 rounded-md p-2 hover:border-yellow-700" placeholder="Description" required></textarea>
                        </div>
                    </form>
                    </div>
                    <!-- Modal footer -->
                    <div class="flex flex-col space-y-2 md:flex-row md:space-y-0 md:space-x-2 p-6 border-t border-gray-200 rounded-b justify-center md:justify-end">
                        <button type="button" class="bg-gray-500 hover:bg-gray-600 text-white font-bold py-2 px-4 rounded-lg" id="cancelButton">Cancel</button>
                        <button type="submit" id="submitProductEntry" form="productForm" class="bg-yellow-700 hover:bg-yellow-600 text-white font-bold py-2 px-4 rounded-lg">Save</button>
                    </div>
                </div>
            </div>   
```

> dan untuk bagian `<script>`:
```
const modal = document.getElementById('crudModal');
        const modalContent = document.getElementById('crudModalContent');

        function showModal() {
            const modal = document.getElementById('crudModal');
            const modalContent = document.getElementById('crudModalContent');

            modal.classList.remove('hidden'); 
            setTimeout(() => {
                modalContent.classList.remove('opacity-0', 'scale-95');
                modalContent.classList.add('opacity-100', 'scale-100');
            }, 50); 
        }
        
        function hideModal() {
            const modal = document.getElementById('crudModal');
            const modalContent = document.getElementById('crudModalContent');

            modalContent.classList.remove('opacity-100', 'scale-100');
            modalContent.classList.add('opacity-0', 'scale-95');

            setTimeout(() => {
                modal.classList.add('hidden');
            }, 150); 
        }

        document.getElementById("cancelButton").addEventListener("click", hideModal);
        document.getElementById("closeModalBtn").addEventListener("click", hideModal);

        function addProductEntry() {
            fetch("{% url 'main:add_product_ajax' %}", {
            method: "POST",
            body: new FormData(document.querySelector('#productForm')),
            })
            .then(response => renderProducts())

            document.getElementById("productForm").reset(); 
            document.querySelector("[data-modal-toggle='crudModal']").click();

            return false;
        }

        document.getElementById("productForm").addEventListener("submit", (e) => {
            e.preventDefault();
            addProductEntry();
        })
```
terakhir pada `forms.py`, saya menambahkan metode:
```
class ProductForm(ModelForm):
    ...
    def clean_name(self):
        name = self.cleaned_data["name"]
        return strip_tags(name)

    def clean_price(self):
        price = self.cleaned_data["price"]
        return strip_tags(price)
```


# Tugas 5

## Jika terdapat beberapa CSS selector untuk suatu elemen HTML, jelaskan urutan prioritas pengambilan CSS selector tersebut!

CSS mempunyai beberapa selector dan setiap selector tersebut mempunyai prioritas pengaplikasian yang berbeda-beda. Urutan dari prioritas tersebut adalah
### 1. !important
!important akan memaksa CSS tersebut untuk dipakai walaupun prioritas dasarnya lebih rendah dibandingkan CSS lainnya.

### 2. Inline Style
Inline style terletak pada tag html itu sendiri akan diutamakan pertama seperti `<div style="opacity: 100">`

### 3. ID Selector
ID selector seperti `#header` akan lebih diutamakan dibandingkan class, dsb. Ditandai dengan # didepannya, dan cara memakaikannya dengan menaruh `id=` pada dalam tag html.

### 4. Class, Pseudo-class, dan Attribute Selector
Class, pseudo-class, dan Attribute selector seperti `.nav atau :hover` mempunyai prioritas yang sama. Jika kita menaruh CSS secara bersamaan, yang akan diutamakan adalah yang terakhir disematkan.

### 5. Tag Selector
Tag selector seperti `div > p {}`, dsb. akan diutamakan selanjutnya. Tag selector ini akan memakaikan CSS pada tag yang merupakan child dari tag di kiri.

## Mengapa responsive design menjadi konsep yang penting dalam pengembangan aplikasi web? Berikan contoh aplikasi yang sudah dan belum menerapkan _responsive design_!

Responsivitas pada web penting karena SEO Google dan lainnya lebih mementingkan website yang mempunyai responsivitas yang tinggi. Responsivitas itu sendiri dihitung dari bagaimana layout website ketika user menggunakan ukuran layar yang berbeda dan UX pada aplikasi itu sendiri seperti _loading time_ dan lainnya.

Contoh aplikasi yang menerapkan responsive design biasanya berasal dari perusahaan besar seperti YouTube, Facebook, Instagram, dst. Sedangkan yang belum memakai biasanya merupakan situs lokal seperti situs toko rumahan.

## Jelaskan perbedaan antara _margin, border,_ dan _padding_, serta cara untuk mengimplementasikan ketiga hal tersebut!

### Margin
Margin adalah ruang di luar elemen yang memisahkan elemen tersebut dari elemen lain. Margin ini, biasanya digunakan untuk memberi jarak antara elemen pada suatu div.

Vanilla CSS
```
div {
  margin: 20px; 
}
```

TailwindCSS
```
<div class="border-2"> </div>
```

### Border 
Border merupakan garis yang berada di sekitar elemen yang membungkus konten dan padding elemen. Border ini dapat memiliki ketebalan, warna, dan gaya yang berbeda.

Vanilla CSS
```
div {
  border: 2px solid black; 
}
```

TailwindCSS
```
<div class="border-2"> </div>
```

### Padding
Ruang di dalam elemen, antara konten elemen dan border. Padding memperbesar ruang di dalam elemen tanpa mengubah ukuran border atau margin.

Vanilla CSS
```
div {
  padding: 10px;  
}
```

TailwindCSS
```
<div class="p-2"> </div>
```

## Jelaskan konsep _flex box_ dan _grid layout_ beserta kegunaannya!

### Flexbox (Flexible Box Layout)
Flexbox biasanya digunakan untuk mengatur tata letak elemen dalam satu dimensi (baris atau kolom). Flexbox memudahkan pengaturan perataan, ukuran, dan distribusi ruang di antara item, terutama ketika ukuran layar berubah.

Penerapan:
- Mengatur tata letak menu horizontal atau vertikal.
- Mengatur grid kartu produk yang responsif.
  
Contoh:
```
.container {
  display: flex;
  justify-content: space-between;
}
```

### Grid Layout
Digunakan untuk membuat tata letak dua dimensi, baik baris maupun kolom. Grid layout memungkinkan kita untuk mengatur elemen-elemen di dalam grid dengan lebih fleksibel dibandingkan Flexbox.

Penerapan:
- Mengatur tata letak halaman dengan area seperti header, sidebar, konten utama, dan footer.
- Mengatur galeri foto dengan baris dan kolom yang dinamis.
- 
Contoh:
```
.container {
  display: grid;
  grid-template-columns: 1fr 2fr;
  grid-gap: 10px;
}
```

## Cara implementasi

Pertama kita buat dulu fungsi `edit_product` dan `delete_product` pada `views.py` di `main`:
```
def edit_product(request, id):
    product = Product.objects.get(id=id)

    form = ProductForm(request.POST or None, instance=product)

    if form.is_valid() and request.method == "POST":
        form.save()
        return HttpResponseRedirect(reverse('main:show_main'))
    
    context = {'form': form}
    return render(request, "edit_product.html", context)

def delete_product(request, id):
    product = Product.objects.get(id=id)
    product.delete()
    return HttpResponseRedirect(reverse('main:show_main'))
```

selanjutnya buat path di `urls.py` seperti biasanya.

setelah itu, kita buat CSS menggunakan TailwindCSS pada setiap html-nya.

Caranya menambahkan script pada `base.html` di tag `<head>`:
```
<script src="https://cdn.tailwindcss.com"></script>
```

Selanjutnya, untuk setiap HTML yang kita buat, kita akan bisa memakai TailwindCSS.

Maka dari itu, kita buat html untuk `edit_product.html`:

```
{% extends 'base.html' %}

{% load static %}

{% block meta %}
<title>Edit Product</title>
{% endblock meta %}

{% block content %}
{% include 'navbar.html' %}
<div class="absolute z-0">
    {% include 'background.html' %}
  </div>
<div class="relative z-10">
    <div class="flex flex-col min-h-screen">
        <div class="container mx-auto px-4 py-8 mt-16 max-w-xl">
          <h1 class="text-3xl font-bold text-center mb-8 text-white">Edit Product</h1>
        
          <div class=" rounded-lg p-6 form-style">
            <form method="POST" class="space-y-6">
                {% csrf_token %}
                {% for field in form %}
                    <div class="flex flex-col">
                        <label for="{{ field.id_for_label }}" class="mb-2 font-semibold text-white">
                            {{ field.label }}
                        </label>
                        <div class="w-full">
                            {{ field }}
                        </div>
                        {% if field.help_text %}
                            <p class="mt-1 text-sm text-white">{{ field.help_text }}</p>
                        {% endif %}
                        {% for error in field.errors %}
                            <p class="mt-1 text-sm text-red-600">{{ error }}</p>
                        {% endfor %}
                    </div>
                {% endfor %}
                <div class="flex justify-center mt-6">
                    <button type="submit" class="bg-yellow-600 text-white font-semibold px-6 py-3 rounded-lg hover:bg-yellow-700 transition duration-300 ease-in-out w-full">
                        Edit Product
                    </button>
                </div>
            </form>
        </div>
        </div>
      </div>
</div>

{% endblock %}
```

dan edit html lainnya.


# Tugas 4

## Apa perbedaan antara `HttpResponseRedirect()` dan `redirect`?

Perbedaan antara kedua methods tersebut secara singkat adalah `HttpResponseRedirect()` merupakan method yang akan mengembalikan status HTTP 302 yang akan mengalihkan client ke sebuah URL yang baru dengan argument sebuah url. Sedangkan `redirect()` melakukan hal yang sama, namun lebih fleksibel dengan cara memakai argument path seperti contohnya pada kasus ini (main:login) atau nama pada path di urls.py.

### HttpResponseRedirect()
```
from django.http import HttpResponseRedirect

...
return HttpResponseRedirect('/sebuah-url/')
...
```

### redirect()

```
from django.shortcuts import redirect

...
return redirect('nama-path')
...
```

## Bagaimana cara kerja penghubungan model `Product` dengan `User`?

Cara kerja model `Product` dengan `User` adalah dengan menggunakan `ForeignKey`.

```
class Product(models.Model):
...
    user=models.ForeignKey(User, on_delete=models.CASCADE)
...
```

ForeignKey tersebut akan menghubungkan `User` dengan setiap object `Product` yang dibuat oleh `User` tersebut.

Jika `User` menambahkan `Product`, maka data akan disimpan dan dapat dishow dengan menggunakan `filter()`, contoh:

```
def show_main(request):
    products = Product.objects.filter(user=request.user)
```

Jika `User` dihapus, maka berdasarkan `on_delete=models.CASCADE`, product yang berkaitan dengan `User` akan ikut terhapus juga.

## Apa perbedaan antara _authentication_ dan _authorization_, apakah yang dilakukan saat pengguna login? Jelaskan bagaimana Django mengimplementasikan kedua konsep tersebut.

### _Authentication_
Authentication pada Django merupakan konsep/proses untuk memverifikasi apakah user sesuai dengan database kredensial pengguna seperti username dan password atau tidak. Hal ini dilakukan untuk memastikan apakah pengguna tersebut valid atau tidak.

### _Authorization_
Authorization pada Django biasanya dilakukan setelah _Authentication_. _Authorization_ merupakan sebuah konsep/proses dimana user tersebut diberikan hak akses terhadap fitur-fitur yang telah diatur oleh website/program yang ingin dipakai.

> Jadi perbedaan mereka adalah _Authentication_ merupakan proses pencocokan data, sedangkan _Authorization_ merupakan proses pemberian hak akses terhadap data dan/atau fitur.

### Implementasi pada Django

pada Django, kita dapat melakukan _Authentication_ dengan menggunakan method `authenticate` untuk melakukan proses login seperti contoh berikut ini:

```
from django.contrib.auth import authenticate, login

def login_user(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)

        if form.is_valid():
            user = form.get_user()
            login(request, user)
            response = HttpResponseRedirect(reverse("main:show_main"))
            response.set_cookie('last_login', str(datetime.datetime.now()))
            return response

    else:
        form = AuthenticationForm(request)
    context = {'form': form}
    return render(request, 'login.html', context)

```

Pada contoh ini, kita menggunakan `form = AuthenticationForm(request)` yang merupakan sebuah class yang menggunakan method authenticate untuk melakukan _Authentication_ pada data.

Sedangkan, untuk melakukan _Authorization_, sebagai contoh kita dapat menggunakan Django decorators sebagai _gatekeeper_ dari laman utama kita, seperti contoh berikut ini:

```
from django.contrib.auth.decorators import login_required

@login_required(login_url='/login')
def show_main(request):
    ...
    return render(request, "main.html", object)
```

## Bagaimana Django mengingat pengguna yang telah login? Jelaskan kegunaan lain dari cookies dan apakah semua cookies aman digunakan?

### Bagaimana Django mengingat user?
Django mengingat pengguna yang telah login dengan menggunakan `Session` dan `Cookies`. Pada saat pengguna berhasil login pada website, Django akan membuat sebuah session untuk pengguna tersebut dan menyimpan ID session di cookies pada browser pengguna. Setiap kali pengguna mengunjungi halaman, Django akan memeriksa cookies untuk dapat mengidentifikasi pengguna berdasarkan session ID yang aktif.

### Kegunaan lain dari cookies
Cookies mempunyai kegunaan lain seperti:

- Menyimpan preferensi pengguna, seperti tema, bahasa yang dipilih, dll.
- Melacak aktifitas pengguna, seperti item apa saja sudah yang dimasukkan
- Autentikasi otomatis, contohnya ada pada fitur `"Remember Me"` yang ada pada kebanyakan website yang menerapkan fitur login-logout.

### Apakah semua cookies aman untuk digunakan?
Tidak semua cookies aman untuk digunakan. Salah satu contohnya adalah cookies yang dapat diserangn dengan menggunakan serangna Cross-Site Scripting (XSS). Maka dari itu, untuk kemanan, Django menyediakan beberapa langkah untuk memsatikan bahwa cookies yang kita pakai sudah aman. Salah satunya dengna built-in seperti:

```
SESSION_COOKIE_SECURE = True
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = 'Lax'
```

- `SESSION_COOKIE_SECURE = True` hanya menerima pengiriman cookies melalui koneksi HTTPS
- `SESSION_COOKIE_HTTPONLY = True` mengatur agar cookies tidak dapat diakses dengan JavaScript
- `SESSION_COOKIE_SAMESITE = 'Lax'` Mengatur sehingga cookies hanya dapat dikirim dengan konteks yang sama untuk mencegah CSRF.

## Step-by-step Implementation dari Tugas 4

Pertama saya memulai dengan membuat fungsi register, login, dan logout pada views.py.

```
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

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

def login_user(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)

        if form.is_valid():
            user = form.get_user()
            login(request, user)
            response = HttpResponseRedirect(reverse("main:show_main"))
            response.set_cookie('last_login', str(datetime.datetime.now()))
            return response

    else:
        form = AuthenticationForm(request)
    context = {'form': form}
    return render(request, 'login.html', context)

def logout_user(request):
    logout(request)
    response = HttpResponseRedirect(reverse('main:login'))
    response.delete_cookie('last_login')
    return response
```

setelah itu, pada templates, saya menambahkan register.html dan login.html sebagai page untuk menerima user yang di redirect.

kemudian saya menambahkan path pada urls.py

```

urlpatterns = [
    ...,
    path('register/', register, name='register'),
    path('login/', login_user, name='login'),
    path('logout/', logout_user, name='logout'),
]
```

Selanjutnya saya menambahkan decorator `login_required` agar user perlu melakukan _Authentication_ dan _Authorization_.

```
@login_required(login_url='/login')
def show_main(request):
    products = Product.objects.all()
    product = {
        'name' : 'R34',
        'price': '$100,000',
        'description': 'A cool car',
        'products': products,
        'last_login': request.COOKIES['last_login'],
        'nama': request.user.username
    }
    return render(request, "main.html", product)
```

Sudah dilihat, bahwa pada kode methods `register`, `login`, dan `logout` saya sudah membuat kode untuk proses cookies dengan nama `last_login`. `last_login` ini kemudian akan ditunjukkan pada main.html.

Terakhir, saya mengaitkan products dengan user dengan menggunakan `ForeignKey`. 

```
class Product(models.Model):
    ...
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    ...
```

dan kemudian agar Django hanya menunjukkan items yang terkait pada user, saya mengganti products pada show_main dari `products = Product.objects.all()` menjadi `products = Product.objects.filter(user=request.user)`.



# Tugas 3

1. Mengapa kita memerlukan data delivery dalam pengimplementasian sebuah platform? 

> Data delivery penting karena berguna pada hampir semua platfrom modern yang berinteraksi dengan banyak komponen yang memerlukan data. Data delivery berfungsi sebagai pembawa data kepada client yang melakukan sebuah request ke sebuah server. Data Delivery mencakup HTTP, JSON, XML, AJAX< jQuery, WebSocket, dan HTTP/HTTPS.

2. Mana yang lebih baik anatara XML dan JSON? Mengapa JSON lebih populer dibandingkan dengan XML?

> XML dan JSON memiliki kelebihan dan kekurangan masing-masing. Salah satu kelebihan dari XML adalah kita dapat melihat struktur hierarkis dan metadata yang lebih luas dan lengkap dengan XML karena mempunyai struktur layaknya tree. XML cocok untuk data yang mempunyai hierarki yang banyak dan lebih kompleks.

> Sedangkan kelebihan JSON dan mengapa JSON lebih dipopuleri adalah dia lebih ringan dan lebih mudah dibaca oleh manusia. JSON juga mudah untuk diintegrasikan dengan JavaScript.

> Method is_valid() pada form Django digunakan untuk memeriksa apakah data yang dikirimkan oleh client melalui form sesuai dengan aturan atau validasi yang telah didefinisikan di form pada models.py. Jika apa yang diisi oleh client sesuai dengan apa yang telah ditetapkan pada models.py, method ini akan mengembalikan nilai True, dan kita bisa melanjutkan proses seperti menyimpan data ke database. Jika validasi gagal, method ini akan mengembalikan False dan form akan menyertakan pesan kesalahan. Ini diperlukan untuk menghindari error karena tipe data yang diisi oleh client tidak sesuai dengan tipe data yang ada di models.py.

4. Mengapa kita membutuhkan csrf_token saat membuat form di Django? 

> csrf_token diperlukan untuk melindungi aplikasi dari serangan CSRF (Cross-Site Request Forgery). CSRF adalah jenis serangan di mana penyerang memalsukan permintaan dari user yang bener untuk melakukan tindakan yang berbahaya, contohnya mengubah pengaturan akun atau melakukan transaksi atas nama user. Jika kita tidak menambahkan csrf_token, penyerang bisa memanfaatkan kelemahan keamanan tersebut untuk melakukan serangan CSRF. Sebagai contoh, penyerang bisa membuat tautan atau form berbahaya yang, jika diklik oleh user yang sedang login, akan mengirimkan permintaan ke server tanpa diketahui oleh user. csrf_token memastikan bahwa setiap form yang dikirim berasal dari sumber yang bener dengan memverifikasi token unik yang ada pada dalam form.

5. Cara mengimplementasikan checklist secara step-by-step (bukan hanya sekadar mengikuti tutorial)

Pertama, saya menambahkan base.html sebagai html utama saya pada direktori templates yang ada di direktori proyek utama. Setelah itu saya tambahkan direktori templates pada settings.py. Setelah itu, pada base.html dan main.html saya menambahkan link Django templates tag agar base.html dapat terektensikan oleh templates lainnya sebagai template utama. Setelah itu saya fokus pada models.py. Disana saya menambahkan variabel uuid pada class Product agar dapat diakses oleh XML dan JSON nantinya. Setelah itu, saya membuat forms.py sebagai ektension dari main.html. Disana saya mengisi dengan csrf dan forms.py yang berisi meta dari forms yang saya ingin buat. Setelah itu saya membuat keempat kode XML dan JSON yang ada dengan views.py methods nya. Terakhir saya menambahkan semua path() pada urls.py agar dapat diaksaes pada main.html.



7. Lampiran Postman
![Screenshot 2024-09-18 111017](https://github.com/user-attachments/assets/ba2503c8-1007-4e70-bad9-ac27559951e4)
![Screenshot 2024-09-18 111035](https://github.com/user-attachments/assets/86362ada-bafa-482e-84ff-417aee9a8462)
![Screenshot 2024-09-18 110935](https://github.com/user-attachments/assets/59553909-61fa-4de0-b949-0d9ba6e40d3e)
![Screenshot 2024-09-18 110957](https://github.com/user-attachments/assets/89d00682-8fe0-421b-a255-4434545ee7ae)




# Tugas 2

Pada tugas kali ini, saya ditugaskan untuk membuat sebuah web sederhana yang meng-implementsaikan *Model-View-Template* (MVT) pada Django. Tugas ini sangatlah mirip dengan tutorial 1 yang diberikan minggu lalu pada pelajaran PBP.

Berikut step-by-step pembuatan website MVT car-commerce:

Pertama, saya membuat sebuah direktori baru di file explorer dengan nama e-commerce. Kemudian saya membuka direktori tersebut pada VSCode. saya menginisiasikan sebuah repo pada github dengan nama car-commerce. Setelah itu saya menyalin link pada commerce dan membuat menghubungkan direktori e-commerce dengan repositori car-commerce dengan cara:

> git init //untuk menginisiasi git pada direktori

> git remote add origin (link_url_github) //untuk menghubungkan direktori dengan repositori github

Kedua, Di dalam VSCode, pada terminal, saya menginisiasikan sebuah aplikasi Django dengan membuat sebuah Virtual Enviroment dengan cara menuliskan

> python -m venv env

ini membuat folder baru bernama **env**.

kemudian kita aktifkan virtual enviroment kita dengan 

> env\Scripts\activate

dengan baris tersebut, saya menjalankan script activate yang terdapat pada direktori env\Scripts\activate. Dengan demikian virtual enviroment berhasil diinisiasikan dan akan terlihat **(env)** pada awal baris terminal.


Ketiga, saya menyiapkan dependencies kita dengan membuat berkas requirements.txt yang berisi:

django
gunicorn
whitenoise
psycopg2-binary
requests
urllib3

ini diperlukan untuk memudahkan instalasi jika diperlukan baik secara lokal, maupun server.

selanjutnya kita install pada virtual enviroment dengan:

> pip install -r requirements.txt

dimana -r merupakan perintah untuk membaca isi dari requirements.txt dan menginstall setiap dependencies yang ada di .txt file tersebut.

akhirnya, saya membuat sebuah proyek django dengan menuliskan:

> django-admin startproject car_commerce

ini akan membuat sebuah folder car_commerce dengan isi-isinya.

agar kita dapat menjalankan localhost, perlu dilakukan perubahan pada settings.py di dalam direktori proyek car_commerce.

pada variabel ALLOWED_HOST, kita tambahkan
> ["localhost", "127.0.0.1", "url_github"
>]
> "localhost", "127.0.0.1", "url_github"


kemudian inisiasi aplikasi main dengan

> python manage.py startapp main

baris tersebut akan membuat sebuah folder baru bernama main

agar django dapat membaca main, kita tambahkan di settings.py direktori proyek pada variabel INSTALLED_APPS 

> [
    ...,
    'main',
]

kemudian buat folder baru bernama templates dan tambahkan main.html

setelah memnginisiasi aplikasi main, kita terapkan MVT.

Pertama pada `main/views.py`kita tambahkan fungsi show_main untuk mengantarkan dictionary kepada main.html kita.

Setelah itu, kita buat pada `main/urls.py` import show_main dari views sebagai routing.

Kemudian, tambahkan path pada car_commerce path yang menuju main.urls agar dapat diakses oleh direktori proyek.

Terakhir pada main.html, tambahkan dengan `{{}}` berisi key dictionary pada views.py untuk menampilkan ke layar.


# Kaitan urls.py, views.py, models.py dan main.html

Client -> urls.py -> views.py -> models.py -> views.py -> Template (HTML) -> Client

1. Pertama, Client akan mengirimkan HTTP request ke web aplikasi melalui URL tertentu.

2. Kedua, Django akan memeriksa urls.py untuk mencocokkan request tersebut dengan URL yang sesuai.
urls.py akan memetakan URL ke views.py, yang berisi fungsi atau kelas view.

3. Ketiga, views.py akan mengambil data dari models.py (jika diperlukan), yang terhubung ke database melalui ORM Django.

4. Terakhir, Setelah data didapatkan atau diproses, views.py akan mengirimkan data tersebut ke berkas template HTML (jika diperlukan) untuk merender tampilan.
Terakhir, response HTML atau data lainnya (JSON, XML, dll.) dikirimkan kembali ke client.

Kaitan pertama dimulai dari urls.py:

> urls.py memetakan URL ke fungsi view pada views.py
> views.py dipanggil oleh urls.py dan akan meng-*handle* logika aplikasi dan mengambil data dari models.py
>berfungsi sebagai template dictionary dan inisiasi variabel untuk views.py
>HTML menampilkan views.py dengan rounting urls.py kepada laman web

# Kegunaaan Git

Git berfungsi sebagai jembatan antara kita dengan server, maupun dengan repositori online agar kode kita dapat disimpan di cloud/server

# Mengapa Django bagus?

1. Karena berbahasa Python sehingga mudah untuk dipelajari dengan syntax yang relatif mudah.
2. Merupakan sebuah framework lama, Django juga mempunyai dokumentasi yang bagus dengan komunitas yang kuat.
3. Django mempunyai fitur django-admin yang mempunyai integrated CRUD tersendiri

# Mengapa Django disebut ORM?

Karena Django menconvert/abstraksi bahasa python menuju bahasa sql untuk menangani CRUD pada database.
