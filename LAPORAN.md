# LAPORAN UAS STRUKTUR DATA
# ANGGOTA KELOMPOK
I Kadek Dwi Andika
I Gede Winasa Edy Purnama
Kristian Putra Santosa

# BAB I - PENDAHULUAN

# 1.1 LATAR BELAKANG
Efisiensi rute pengiriman barang merupakan faktor krusial bagi UMKM untuk menekan biaya operasional dan mempercepat waktu distribusi. Namun, penentuan jalur logistik yang dilakukan secara manual sering kali menghasilkan rute yang tidak optimal, memutar, dan boros biaya. Masalah pencarian rute terpendek ini dapat diselesaikan secara matematis menggunakan teori graf, di mana lokasi diwakili sebagai Node dan jalur jalan sebagai Edge yang memiliki bobot (Weight) berupa jarak atau waktu.  Untuk memecahkan masalah tersebut, Algoritma Dijkstra merupakan solusi yang sangat efektif karena mampu mencari jalur dengan total bobot terkecil dari titik asal ke titik tujuan. Di samping algoritma, representasi struktur data di dalam memori—seperti Adjacency List atau Adjacency Matrix—juga sangat memengaruhi performa dan kecepatan pemrosesan data sistem.  Oleh karena itu, dikembangkan aplikasi DSS Logistik Graph berbasis web. Aplikasi ini berfungsi sebagai sistem pendukung keputusan yang dinamis, memungkinkan pengguna menambah node dan edge baru , serta mensimulasikan pencarian rute terbaik dari Gudang Pusat menuju Toko Gianyar melalui titik perantara seperti Kurir Denpasar dan Drop Point Badung. Berdasarkan hal tersebut, penelitian ini dilakukan untuk menganalisis penerapan struktur data graf dan Algoritma Dijkstra pada aplikasi optimasi logistik ini. 

# 1.2 RUMUSAN MASALAH
1. Bagaimana merancang dan mengimplementasikan aplikasi optimasi rute pengiriman barang berbasis struktur data Graph dan Algoritma Dijkstra untuk UMKM?  
2. Bagaimana representasi struktur data Adjacency List dan Adjacency Matrix di dalam memori memengaruhi proses analisis dan rekomendasi keputusan penentuan rute terbaik?

# 1.3 TUJUAN
1. Mengimplementasikan Algoritma Dijkstra ke dalam struktur data Graph untuk menemukan rute pengiriman barang tercepat dan paling efisien dari titik asal ke titik tujuan bagi UMKM.
2. Menganalisis performa representasi memori antara penggunaan Adjacency List dan Adjacency Matrix dalam mengelola data komponen graf (Node, Edge, dan Weight).
3. Membangun sistem pendukung keputusan (DSS) logistik berbasis web yang dinamis, sehingga pengguna dapat memperbarui data peta distribusi (menambah lokasi dan jalur baru) serta melihat hasil analisis rute secara langsung (real time).

# 1.4 MANFAAT
1. Meningkatkan Efisiensi Operasional: Membantu UMKM memangkas biaya bahan bakar dan waktu pengiriman melalui rekomendasi rute terpendek yang dihasilkan oleh Algoritma Dijkstra.
2. Otomatisasi Pengambilan Keputusan: Memudahkan pemilik usaha atau kurir dalam mengambil keputusan logistik secara cepat dan akurat tanpa harus menebak-nebak rute manual.
3. Fleksibilitas Manajemen Rute: Memberikan kemudahan bagi pengguna untuk memperbarui peta jalur distribusi secara mandiri ketika terjadi penambahan cabang toko baru atau perubahan rute jalan.

# BAB 2 - DASAR TEORI

# 2.1 STRUKTUR DATA GRAPH

### 2.1.1 KOMPONEN UTAMA GRAPH

Di dalam memori sistem, graf ini dipecah menjadi beberapa bagian utama:

* 
**Node / Vertex (Titik):** Merepresentasikan lokasi fisik atau entitas logistik. Di file Anda, terdapat **4 Node**: `"Gudang Pusat"` , `"Toko Gianyar"` , `"Kurir Denpasar"` , dan `"Drop Point Badung"`.


* 
**Edge (Sisi/Jalur) & Weight (Bobot):** Merepresentasikan jalur penghubung antar-lokasi beserta jarak/biayanya.



---

### 2.1.2 MEMBACA REPRESENTASI
Format JSON pada graph menunjukkan bagaimana setiap node menyimpan daftar "tetangga" yang terhubung langsung dengannya beserta bobot jalurnya:

#### A. 

Node: "Gudang Pusat" 

Gudang Pusat terhubung ke dua lokasi:

1. Ke **"Toko Gianyar"** dengan bobot/jarak **25**.


2. Ke **"Kurir Denpasar"** dengan bobot/jarak **10**.



#### B. 

Node: "Toko Gianyar" 

Toko Gianyar terhubung ke dua lokasi:

1. Ke **"Gudang Pusat"** dengan bobot/jarak **25**.


2. Ke **"Drop Point Badung"** dengan bobot/jarak **30**.



#### C. 

Node: "Kurir Denpasar" 

Kurir Denpasar terhubung ke dua lokasi:

1. Ke **"Gudang Pusat"** dengan bobot/jarak **10**.


2. Ke **"Drop Point Badung"** dengan bobot/jarak **15**.



#### D. 

Node: "Drop Point Badung" 

Drop Point Badung terhubung kembali ke:

1. Ke **"Toko Gianyar"** dengan bobot/jarak **30**.


2. Ke **"Kurir Denpasar"** dengan bobot/jarak **15**.



---

### 2.1.3 VISUALISASI ALUR HUBUNGAN
Jika data pada graph digambarkan, bentuk jaringannya akan terlihat bolak-balik (Graph Tidak Berarah / *Undirected Graph* karena memiliki bobot yang sama saat kembali) seperti ini:

```text
 [Gudang Pusat] <=== (bobot: 10) ===> [Kurir Denpasar]
       ^                                      ^
       |                                      |
   (bobot: 25)                            (bobot: 15)
       |                                      |
       v                                      v
 [Toko Gianyar] <=== (bobot: 30) ===> [Drop Point Badung]

```

### Mengapa Struktur Ini Penting untuk Algoritma Dijkstra?

Ketika Anda menekan tombol **"Analisis & Hitung Rute Terbaik"** dari *Gudang Pusat* ke *Toko Gianyar* , Algoritma Dijkstra akan membaca struktur *Adjacency List* ini:

* Jalur **Langsung**: Gudang Pusat $\rightarrow$ Toko Gianyar = **25**.


* Jalur **Alternatif**: Gudang Pusat $\rightarrow$ Kurir Denpasar $\rightarrow$ Drop Point Badung $\rightarrow$ Toko Gianyar = $10 + 15 + 30 = \mathbf{55}$.



Sistem secara otomatis akan merekomendasikan jalur **Langsung (Gudang Pusat $\rightarrow$ Toko Gianyar)** karena memiliki total bobot terkecil, yaitu **25**.

# 2.2 ALGORITMA GRAPH
Graph ini menggunakan Algoritma Dijkstra, yaitu adalah sebuah algoritma *greedy* yang digunakan untuk menyelesaikan permasalahan pencarian rute terpendek dari satu titik asal (*single-source shortest path*) menuju titik-titik lainnya pada sebuah Graf Berbobot (*Weighted Graph*). Algoritma ini bekerja dengan prinsip memilih jalur yang memiliki akumulasi bobot (*weight*) paling minimal pada setiap tahapannya, dengan syarat seluruh bobot pada sisi (*edge*) graf harus bernilai positif.

Di dalam Sistem Pendukung Keputusan (DSS) Logistik ini, Algoritma Dijkstra berperan sebagai mesin pemroses utama (*core engine*) pada fitur "Analisis & Hitung Rute Terbaik" untuk menghasilkan rekomendasi rute distribusi barang yang paling optimal bagi pelaku UMKM.

# 2.1.1 PRINSIP KERJA ALGORITMA
Secara matematis, algoritma ini mengelola tiga jenis informasi utama selama proses komputasi berlangsung:

1. **Daftar Jarak (*Distance Table*):** Menyimpan estimasi total jarak/bobot terpendek sementara dari titik awal (*Source Node*) ke setiap lokasi lainnya di dalam graf.
2. **Daftar Kunjungan (*Visited Set*):** Kumpulan lokasi (*node*) yang jalur terpendeknya sudah dipastikan secara final oleh algoritma, sehingga tidak akan diproses kembali.
3. 
**Daftar Penjejakan (*Predecessor/Previous Node*):** Catatan mengenai lokasi sebelumnya yang dilewati guna merekonstruksi urutan jalur dari titik awal hingga mencapai titik tujuan akhir.



---

### **2. Tahapan Simulasi Perhitungan Berdasarkan Data Aplikasi**

Ketika pengguna menetapkan **Gudang Pusat** sebagai titik awal dan **Toko Gianyar** sebagai alamat tujuan konsumen , Algoritma Dijkstra di dalam memori melakukan kalkulasi melalui langkah-langkah berikut:

* **Langkah 1: Inisialisasi**
* Mengatur jarak awal untuk `Gudang Pusat` = $0$.
* Mengatur jarak awal untuk node lainnya (`Kurir Denpasar`, `Drop Point Badung`, `Toko Gianyar`) = Tak Hingga ($\infty$).


* Semua node ditandai sebagai *belum dikunjungi*.


* **Langkah 2: Evaluasi dari Gudang Pusat (Node Aktif Saat Ini)**
Algoritma memeriksa semua tetangga yang terhubung langsung dengan `Gudang Pusat` melalui data *Adjacency List*:


* Jalur ke `Kurir Denpasar` berbobot $10$. Dilakukan proses *relaxation*: nilai jarak diperbarui dari $\infty$ menjadi **10**.


* Jalur ke `Toko Gianyar` berbobot $25$. Nilai jarak diperbarui dari $\infty$ menjadi **25**.


* `Gudang Pusat` ditandai sebagai *sudah dikunjungi*.


* **Langkah 3: Evaluasi dari Kurir Denpasar (Node dengan Jarak Terkecil Berikutnya)**
Dari sisa node yang belum dikunjungi, `Kurir Denpasar` dipilih karena memiliki bobot terkecil ($10$). Algoritma mengecek tetangganya yang belum final:


* Jalur menuju `Drop Point Badung` memiliki bobot $15$. Total jarak akumulatif dari awal menjadi $10 + 15 = \mathbf{25}$. Jarak `Drop Point Badung` diperbarui menjadi **25**.


* `Kurir Denpasar` ditandai sebagai *sudah dikunjungi*.


* **Langkah 4: Evaluasi dari Drop Point Badung**
Melalui `Drop Point Badung` (jarak sementara $25$), algoritma mengecek rute menuju target akhir `Toko Gianyar`:


* Jalur dari `Drop Point Badung` ke `Toko Gianyar` berbobot $30$. Jika melewati rute ini, total jarak menjadi $25 + 30 = \mathbf{55}$.




* **Langkah 5: Pengambilan Keputusan Akhir**
Algoritma membandingkan dua opsi akumulasi bobot terkecil untuk mencapai `Toko Gianyar`:


* Jalur langsung (`Gudang Pusat` $\rightarrow$ `Toko Gianyar`) = **25**.


* Jalur memutar (`Gudang Pusat` $\rightarrow$ `Kurir Denpasar` $\rightarrow$ `Drop Point Badung` $\rightarrow$ `Toko Gianyar`) = **55**.





Berdasarkan sifat *greedy*, algoritma menetapkan **Jalur Langsung (Gudang Pusat $\rightarrow$ Toko Gianyar)** sebagai hasil final karena memiliki nilai bobot terkecil (25). Urutan rute inilah yang kemudian ditampilkan oleh sistem sebagai rekomendasi keputusan kepada pengguna.

# BAB 3 – ANALISIS DAN PERANCANGAN
# 3.1 ANALISIS MASALAH
Aktivitas logistik pada Usaha Mikro, Kecil, dan Menengah (UMKM) sering kali menghadapi tantangan besar dalam hal efisiensi rute distribusi pengiriman barang. Berdasarkan analisis terhadap proses berjalan, ditemukan beberapa kendala utama yang dihadapi oleh mitra pelaku usaha, antara lain:  Penentuan Rute yang Subjektif: Proses penulisan dan pemilihan rute pengantaran paket dari gudang pusat ke konsumen masih didasarkan pada intuisi kurir atau peta konvensional. Hal ini sering kali memicu pemilihan jalur yang memutar sehingga terjadi pemborosan waktu.  Pembengkakan Biaya Operasional: Rute pengiriman yang tidak optimal berdampak langsung pada tingginya konsumsi bahan bakar kendaraan operational.Keterbatasan Alat Bantu Keputusan: Manajemen logistik tidak memiliki instrumen visual atau sistem komputasi dinamis yang dapat menghitung kombinasi jarak antar-pos logistik (seperti kurir wilayah atau drop point) untuk menghasilkan keputusan jalur terpendek secara real-time.  Melalui pengembangan Decision Support System (DSS) Logistik Graph ini, masalah-masalah di atas diselesaikan dengan memodelkan peta jaringan jalan ke dalam struktur data graf berbobot dan mengotomatisasikannya menggunakan Algoritma Dijkstra. 

# 3.2 DESAUN GRAPH
Desain jaringan distribusi pada sistem ini dimodelkan sebagai Graf Berbobot dan Tidak Berarah (Weighted Undirected Graph). Graf ini merepresentasikan peta logistik riil yang digunakan sebagai studi kasus sistem. Hubungan spasial antar-lokasi dirancang sedemikian rupa agar kurir dapat bergerak secara dua arah (bolak-balik) dengan bobot jarak yang sama.  Berdasarkan data operasional yang terekam pada sistem, berikut adalah rancangan visual model jaringan logistik tersebut:  Keterangan Model Graf Jaringan Jarak:  Gudang Pusat terhubung langsung ke Kurir Denpasar dengan bobot jarak 10 Km.  Gudang Pusat terhubung langsung ke Toko Gianyar dengan bobot jarak 25 Km.  Kurir Denpasar terhubung langsung ke Drop Point Badung dengan bobot jarak 15 Km.  Drop Point Badung terhubung langsung ke Toko Gianyar dengan bobot jarak 30 Km.  

# 3.3 FLOWCHART SISTEM
Flowchart (Diagram Alir) di bawah ini menggambarkan logika jalannya sistem pendukung keputusan dari awal menerima input lokasi hingga menghasilkan rekomendasi keputusan akhir menggunakan Algoritma Dijkstra.

<img width="1520" height="2840" alt="flowchart-dss-logistik-v2" src="https://github.com/user-attachments/assets/2a362972-a93c-49c9-8b5a-8c0e3f128c9e" />

# 3.4 USE CASE DIAGRAM
Arsitektur interaksi pengguna (user interaction) terhadap perangkat lunak DSS Logistik Graph ini dirancang dengan satu Aktor utama yaitu Pengguna (Admin Logistik / Pemilik UMKM).  Berikut adalah deskripsi fungsionalitas komponen Use Case sistem:Manage Node (Lokasi): Pengguna memiliki hak akses untuk mendaftarkan nama lokasi logistik baru ke dalam memori sistem secara dinamis.  Manage Edge (Rute & Jarak): Pengguna dapat menghubungkan dua lokasi yang berbeda dan memberikan nilai bobot jarak dalam satuan kilometer.  View Representasi Memori: Pengguna dapat memantau dan mengaudit integritas struktur data internal yang sedang aktif, baik berupa struktur Adjacency List (JSON) maupun tabel Adjacency Matrix.  Calculate Shortest Path: Pengguna dapat memilih titik awal keberangkatan serta titik tujuan konsumen, kemudian memerintahkan sistem untuk melakukan komputasi pencarian rute logistik terbaik.  

# 3.5 STRUKTUR NODE DAN EDGE
Bagian ini mendefinisikan detail teknis perancangan objek data yang dialokasikan di dalam memori komputer saat aplikasi dijalankan.  

# 3.5.1 STRUKTUR NODE
Node merepresentasikan entitas lokasi fisik tempat penyimpanan atau pendistribusian barang logistik. Objek node dirancang menggunakan tipe data string yang ditampung dalam sebuah array dinamis (list). Data node awal pada perancangan ini meliputi:  Node[0] = "Gudang Pusat"Node[1] = "Toko Gianyar"Node[2] = "Kurir Denpasar"Node[3] = "Drop Point Badung"

# 3.5.2 STRUKTUR EDGE DAN BOBOT
Edge merepresentasikan keterhubungan langsung jalur transportasi darat antarnode, sedangkan Weight menyimpan informasi panjang rute dalam satuan kilometer (km). Pada rancangan aplikasi ini, struktur hubungan tersebut diimplementasikan ke dalam format Adjacency List (Format JSON) sebagai berikut:  JSON{
  "Gudang Pusat": [
    ["Toko Gianyar", 25],
    ["Kurir Denpasar", 10]
  ],
  "Toko Gianyar": [
    ["Gudang Pusat", 25],
    ["Drop Point Badung", 30]
  ],
  "Kurir Denpasar": [
    ["Gudang Pusat", 10],
    ["Drop Point Badung", 15]
  ],
  "Drop Point Badung": [
    ["Toko Gianyar", 30],
    ["Kurir Denpasar", 15]
  ]
}
Keterangan Struktur: Kunci utama (Key) luar bertindak sebagai titik awal keberangkatan (Node Asal), sedangkan array di dalamnya menyimpan daftar pasangan nama Node Tujuan beserta bobot integernya.  
