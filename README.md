# car-commerce

Nama: Muhammad Nadzim Tahara

NPM: 2306275430

Kelas: PBP C

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



6. Lampiran Postman
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
