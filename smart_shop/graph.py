import math

coordinates = {
    "Pintu Masuk": (0, 0),
    "Keranjang Belanja": (4, 2),
    "Koridor Depan": (12, 0),
    "Buah & Sayur": (5, 5),
    "Daging & Ikan": (4, 8),
    "Produk Susu": (9, 6),
    "Makanan Ringan": (9, 8),
    "Minuman": (9, 11),
    "Perlengkapan Rumah": (12, 5),
    "Koridor Belakang": (12, 15),
    "Gudang": (2, 15),
    "Kasir": (9, 0)
}

def dist(a, b):
    x1, y1 = coordinates[a]
    x2, y2 = coordinates[b]
    return round(math.sqrt((x1-x2)**2 + (y1-y2)**2), 1)

supermarket_graph = {
    "Pintu Masuk": [
        ("Keranjang Belanja", dist("Pintu Masuk", "Keranjang Belanja"))
    ],

    "Keranjang Belanja":[
        ("Kasir", dist("Keranjang Belanja", "Kasir")), 
        ("Pintu Masuk", dist("Keranjang Belanja", "Pintu Masuk")),
        ("Buah & Sayur", dist("Keranjang Belanja", "Buah & Sayur"))
    ],

    "Koridor Depan": [
        ("Kasir", dist("Koridor Depan", "Kasir")),
        ("Perlengkapan Rumah", dist("Koridor Depan", "Perlengkapan Rumah")),
    ],

    "Buah & Sayur": [
        ("Daging & Ikan", dist("Buah & Sayur", "Daging & Ikan")),
        ("Keranjang Belanja", dist("Buah & Sayur", "Keranjang Belanja"))
    ],

    "Daging & Ikan": [
        ("Buah & Sayur", dist("Daging & Ikan", "Buah & Sayur")), 
        ("Minuman", dist("Daging & Ikan", "Minuman")),
        ("Gudang", dist("Daging & Ikan", "Gudang"))
    ],

    "Produk Susu": [
        ("Makanan Ringan", dist("Produk Susu", "Makanan Ringan")),
        ("Kasir", dist("Produk Susu", "Kasir"))
    ],

    "Makanan Ringan": [
        ("Produk Susu", dist("Makanan Ringan", "Produk Susu")), 
        ("Minuman", dist("Makanan Ringan", "Minuman")), 
    ],

    "Minuman": [
        ("Makanan Ringan", dist("Minuman", "Makanan Ringan")), 
        ("Koridor Belakang", dist("Minuman", "Koridor Belakang")),
        ("Daging & Ikan", dist("Minuman", "Daging & Ikan"))
    ],

    "Perlengkapan Rumah": [
        ("Koridor Depan", dist("Perlengkapan Rumah", "Koridor Depan")), 
        ("Koridor Belakang", dist("Perlengkapan Rumah", "Koridor Belakang"))
    ],

    "Koridor Belakang": [
        ("Minuman", dist("Koridor Belakang", "Minuman")),
        ("Perlengkapan Rumah", dist("Koridor Belakang", "Perlengkapan Rumah")),
        ("Gudang", dist("Koridor Belakang", "Gudang")),
    ],

    "Gudang": [
        ("Koridor Belakang", dist("Gudang", "Koridor Belakang")),
        ("Daging & Ikan", dist("Gudang", "Daging & Ikan")),
    ],

    "Kasir": [
        ("Koridor Depan", dist("Kasir", "Koridor Depan")), 
        ("Produk Susu", dist("Kasir", "Produk Susu")),
        ("Keranjang Belanja", dist("Kasir", "Keranjang Belanja")),
    ]
}

categories = ["Buah & Sayur","Daging & Ikan","Produk Susu","Makanan Ringan","Minuman","Perlengkapan Rumah","Koridor Belakang",]

def get_coordinates(node):
    return coordinates.get(node, (0, 0))

def print_coordinates():
    for node, (x, y) in coordinates.items():
        print(f"{node}: ({x}, {y})")