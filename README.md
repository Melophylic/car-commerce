# car-commerce

Nama: Muhammad Nadzim Tahara
NPM: 2306275430
Kelas: PBP C

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