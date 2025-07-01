## Website Pencarian Peraturan Bidang Sektoral Pajak Daerah dan Retribusi Daerah

Project Akhir Magang Tim Sinkronisasi Kebijakan Pajak Daerah dan Retribusi Daerah, Direktorat Jenderal Perimbangan Keuangan, Kementerian Keuangan Republik Indonesia

---

### Daftar Isi

- [Deskripsi Proyek](#deskripsi-proyek)
- [Getting Started Proyek](#getting-started-proyek)
- [Run Aplikasi](#run-aplikasi)
- [Struktur Proyek](#struktur-proyek)
- [Desain dan Model Database](#desain-dan-model-database)
    - [Mockup UI/UX](#mockup-uiux)
    - [Model Skema Database](#desain-dan-model-database)
- [Referensi](#referensi)

### Deskripsi Proyek

Aplikasi database peraturan sektoral bidang pajak daerah dan retribusi daerah merupakan aplikasi berbasis website yang dirancang secara mandiri sebagai alat untuk memudahkan dalam mencari peraturan perundang - undangan. Website ini berisi proses bisnis, penampilan peraturan dengan mode pencarian, pen-update-an peraturan, monitoring perubahan yang dilakukan, dan informasi mengenai data potensi pajak dan retribusi daerah di seluruh wilayah kabupaten/kota di Indonesia.

### Getting Started Proyek

Berikut langkah - langkah untuk memulai dan menjalankan proyek lingkungan lokal Anda.

#### Requirement
- [Git](https://git-scm.com/)

1. *Clone Repository*. Kemudian, buka terminal dan clone proyek ini ke mesin lokal Anda.
    
   ```
   git clone https://github.com/iksnn/tr-sinkron.git
   ```
    
3. *Buka Folder Proyek. Masuk ke dalam *virtual environment.

    ```
    .\env\Scripts\activate
    ```
    
4. *Install Kebutuhan Backend dengan Menggunakan Django* dengan mengakses command berikut.

    ```
    pip install -r requirements.txt 
    ```
    
5. *Install Kebutuhan Frontend dengan Menggunakan Vue Js* dengan masuk ke dalam virtual environment terlebih dahulu.

    ```
    npm install
    ```

### Run Aplikasi

Untuk mengakses aplikasi dengan menjalankan perintah berikut.
1. Masuk terlebih dahulu ke dalam virtual environment 

    ```
    .\env\Scripts\activate
    ```
    
1. Akses sisi backend, di dalam virtual environment dengan menjalankan perintah.

    ```
    py manage.py runserver
    ```
    
2. Akses sisi frontend di dalam terminal virtual environment yang berbeda dengan perintah.

    ```
    npm run serve
    ```
    
3. Kemudian, mengakses link url.

    ```
    http://localhost:8080/
    ```

### Struktur Proyek
Arsitektur proyek ini diorganisir sebagai berikut.

```
tr-sinkron/
├── backend/                      # Direktori akses yang menangani semua request dari client
│   ├── api/
│       ├── migrations/           # Direktori migrasi model ke database
│   ├── backend/
│   ├── data/
│   ├── import_data_potensi.py    
│   └── manage.py                 # File akses backend
├── env/                          
├── frontend/                     # Aplikasi tampilan antarmuka yang dirancang dengan Vue.js
│   ├── node_modules/
│   ├── public/
│   └── src/                       
├── .gitignore                    
└── requirements.txt              # Kebutuhan pengembangan                           
```

### Desain dan Model Database

#### Mockup UI/UX

Desain antarmuka tampilan awal aplikasi website pencarian peraturan sektoral PDRD.

![Desain Mockup Tampilan](./frontend/src/assets/images/Desain%20Mockup.png)

#### Model Schema Database
Model schema database

![Schema Database](./frontend/src/assets/images/Schema%20Database.png)

### Referensi
- [JDIH BPK](https://peraturan.bpk.go.id/)
- [JDIH Setneg](https://jdih.setneg.go.id/)
- [SIKD Kemenkeu](https://sikd.kemenkeu.go.id/)
