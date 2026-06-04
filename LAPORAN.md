# LAPORAN UAS STRUKTUR DATA
# ANGGOTA KELOMPOK
I Kadek Dwi Andika
I Gede Winasa Edy Purnama
Kristian Putra Santosa

# BAB I

# LATAR BELAKANG
Efisiensi rute pengiriman barang merupakan faktor krusial bagi UMKM untuk menekan biaya operasional dan mempercepat waktu distribusi. Namun, penentuan jalur logistik yang dilakukan secara manual sering kali menghasilkan rute yang tidak optimal, memutar, dan boros biaya. Masalah pencarian rute terpendek ini dapat diselesaikan secara matematis menggunakan teori graf, di mana lokasi diwakili sebagai Node dan jalur jalan sebagai Edge yang memiliki bobot (Weight) berupa jarak atau waktu.  Untuk memecahkan masalah tersebut, Algoritma Dijkstra merupakan solusi yang sangat efektif karena mampu mencari jalur dengan total bobot terkecil dari titik asal ke titik tujuan. Di samping algoritma, representasi struktur data di dalam memori—seperti Adjacency List atau Adjacency Matrix—juga sangat memengaruhi performa dan kecepatan pemrosesan data sistem.  Oleh karena itu, dikembangkan aplikasi DSS Logistik Graph berbasis web. Aplikasi ini berfungsi sebagai sistem pendukung keputusan yang dinamis, memungkinkan pengguna menambah node dan edge baru , serta mensimulasikan pencarian rute terbaik dari Gudang Pusat menuju Toko Gianyar melalui titik perantara seperti Kurir Denpasar dan Drop Point Badung. Berdasarkan hal tersebut, penelitian ini dilakukan untuk menganalisis penerapan struktur data graf dan Algoritma Dijkstra pada aplikasi optimasi logistik ini.  

# RUMUSAN MASALAH
1. Bagaimana merancang dan mengimplementasikan aplikasi optimasi rute pengiriman barang berbasis struktur data Graph dan Algoritma Dijkstra untuk UMKM?  
2. Bagaimana representasi struktur data Adjacency List dan Adjacency Matrix di dalam memori memengaruhi proses analisis dan rekomendasi keputusan penentuan rute terbaik?

# TUJUAN
1. Mengimplementasikan Algoritma Dijkstra ke dalam struktur data Graph untuk menemukan rute pengiriman barang tercepat dan paling efisien dari titik asal ke titik tujuan bagi UMKM.
2. Menganalisis performa representasi memori antara penggunaan Adjacency List dan Adjacency Matrix dalam mengelola data komponen graf (Node, Edge, dan Weight).
3. Membangun sistem pendukung keputusan (DSS) logistik berbasis web yang dinamis, sehingga pengguna dapat memperbarui data peta distribusi (menambah lokasi dan jalur baru) serta melihat hasil analisis rute secara langsung.

# MANFAAT
1. Meningkatkan Efisiensi Operasional: Membantu UMKM memangkas biaya bahan bakar dan waktu pengiriman melalui rekomendasi rute terpendek yang dihasilkan oleh Algoritma Dijkstra.
2. Otomatisasi Pengambilan Keputusan: Memudahkan pemilik usaha atau kurir dalam mengambil keputusan logistik secara cepat dan akurat tanpa harus menebak-nebak rute manual.
3. Fleksibilitas Manajemen Rute: Memberikan kemudahan bagi pengguna untuk memperbarui peta jalur distribusi secara mandiri ketika terjadi penambahan cabang toko baru atau perubahan rute jalan.

# BAB 2 | DASAR TEORI

# STRUKTUR DATA GRAPH
Tentu. Berdasarkan data JSON yang ada pada file, aplikasi Anda menggunakan **Graph Berarah (Directed Graph)** atau **Graph Berbobot (Weighted Graph)** yang direpresentasikan melalui struktur **Adjacency List** (Daftar Keketanggaan).

Mari kita bedah struktur data tersebut agar lebih mudah dipahami:

### 1. Komponen Utama Graph pada File

Di dalam memori sistem, graf ini dipecah menjadi beberapa bagian utama:

* 
**Node / Vertex (Titik):** Merepresentasikan lokasi fisik atau entitas logistik. Di file Anda, terdapat **4 Node**: `"Gudang Pusat"` , `"Toko Gianyar"` , `"Kurir Denpasar"` , dan `"Drop Point Badung"`.


* 
**Edge (Sisi/Jalur) & Weight (Bobot):** Merepresentasikan jalur penghubung antar-lokasi beserta jarak/biayanya.



---

### 2. Membaca Representasi *Adjacency List* di File

Format JSON pada file menunjukkan bagaimana setiap node menyimpan daftar "tetangga" yang terhubung langsung dengannya beserta bobot jalurnya:

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

### 3. Visualisasi Alur Hubungan (Peta Logistik)

Jika data di atas digambarkan, bentuk jaringannya akan terlihat bolak-balik (Graf Tidak Berarah / *Undirected Graph* karena memiliki bobot yang sama saat kembali) seperti ini:

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
