# car-commerce

Nama: Muhammad Nadzim Tahara

NPM: 2306275430

Kelas: PBP C

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

dan kemudian agar Django hanya menunjukkan items yang terkait pada user, saya mengganti products pada show_main dari `products = Product.objects.all()` dan `products = Product.objects.filter(user=request.user)`



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
