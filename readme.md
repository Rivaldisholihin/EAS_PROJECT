# Smart Shop: Supermarket Route Optimization and Crowd Avoidance

Aplikasi berbasis Flask untuk membantu pengguna menemukan rute belanja paling efisien di supermarket dengan mempertimbangkan jarak dan tingkat keramaian.

---

## Tentang Project

Smart Shop adalah aplikasi yang dirancang untuk:
- Mengoptimalkan rute belanja dalam supermarket
- Menghindari area yang ramai
- Menghemat waktu pengguna saat berbelanja

Aplikasi ini menggunakan algoritma optimasi (seperti graph traversal / shortest path) untuk menentukan jalur terbaik berdasarkan input pengguna.

---

## Fitur

- Optimasi rute belanja
- Deteksi area ramai (crowd avoidance)
- Input daftar barang
- Visualisasi atau output jalur optimal
- Backend berbasis Flask

---

## Teknologi

- Python 3
- Flask
- (Opsional) NetworkX / algoritma graph
- HTML/CSS (jika ada frontend)

---

## Instalasi

### 1. Clone Repository

```bash
git clone https://github.com/username/smart-shop.git
cd smart-shop

## Setup Environment

### 2. Buat Virtual Environment (Direkomendasikan)

```bash
python -m venv venv
```

Aktifkan environment:

**Windows**

```bash
venv\Scripts\activate
```

**Linux / Mac**

```bash
source venv/bin/activate
```

---

### 3. Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

Jika belum ada `requirements.txt`, bisa install manual:

```bash
pip install flask
```

---

## Cara Menjalankan

```bash
python app.py
```

Aplikasi akan berjalan di:

```text
http://127.0.0.1:5000/
```

---

## Struktur Folder

```text
smart-shop/
│── app.py
│── requirements.txt
│── static/
│── templates/
│── README.md
```

---

## Contoh Penggunaan

1. Jalankan aplikasi
2. Masukkan daftar barang
3. Sistem akan:

   * Menghitung rute optimal
   * Menghindari area ramai
4. Output berupa jalur terbaik

---

## Algoritma yang Digunakan

Masalah ini dimodelkan sebagai **graph**, di mana:

* Node = lokasi produk / rak
* Edge = jalur antar lokasi
* Weight = jarak + tingkat keramaian

Pendekatan yang bisa digunakan:

* Dijkstra (shortest path)
* BFS (jika tanpa bobot)
* Greedy / heuristic (untuk optimasi lebih cepat)

---

## Kontribusi

Kontribusi terbuka:

1. Fork repository
2. Buat branch baru
3. Commit perubahan
4. Pull request
