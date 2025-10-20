# oop-polymorphism-python

## Capaian Pembelajaran

1. Mahasiswa mampu mengimplementasikan prinsip **polymorphism** menggunakan inheritance di Python.
2. Mahasiswa mampu mengimplementasikan prinsip **polymorphism** menggunakan duck typing di Python.
3. Mahasiswa mampu menggunakan **abstract class** sesuai kebutuhan.

---

## Lingkungan Pengembangan

1. Platform: Python 3.10+
2. Bahasa: Python
3. Editor/IDE yang disarankan:
   - VS Code + Python Extension
   - Terminal

---

## Cara Menjalankan Project

1. Clone repositori project `oop-polymorphism-python` ke direktori lokal Anda:
   ```bash
   git clone https://github.com/USERNAME/oop-polymorphism-python.git
   cd oop-polymorphism-python
   ```

2. Buat dan aktifkan virtual environment:

   ```bash
   python -m venv .venv
   source .venv/bin/activate        # Linux/macOS
   .venv\Scripts\activate           # Windows
   ```

3. Install dependensi:

   ```bash
   pip install -r requirements.txt
   ```

4. Jalankan unit test:

   ```bash
   pytest
   ```

> PERINGATAN: Lakukan push ke remote repository hanya jika seluruh unit test telah berhasil dijalankan (semua hijau).

---

## Soal-soal

### 1) Parade Hewan dan Suara

**Lokasi:** `src/pet_parade/`

* Buat kelas abstrak `Hewan` di `src/pet_parade/hewan.py`:

  * Atribut privat `_nama: str`
  * Properti `nama` (getter & setter)
  * Metode abstrak `bersuara(self) -> str`
* Turunan:

  * `Kucing`: implementasi `bersuara()` → `"Meong"`
  * `Anjing`: implementasi `bersuara()` → `"Guk"`
* Buat kelas `ParadeHewan` di `src/pet_parade/parade.py`:

  * Atribut privat `_list_hewan: list[Hewan]`
  * Metode:

    * `tambah_hewan(self, hewan: Hewan) -> None`
    * `hapus_hewan(self, hewan: Hewan) -> None`
    * `mulai_parade(self, putaran: int) -> list[str]`

      * Mengembalikan daftar string dengan format:

        ```
        "{namaHewan} bersuara: {suaraHewan}"
        ```
      * Ulangi sesuai jumlah `putaran`.
* Tambahkan blok demo `if __name__ == "__main__":` untuk menampilkan hasil.

---

### 2) Studio Musik

**Lokasi:** `src/music_studio/`

* Kelas abstrak `Instrumen` di `src/music_studio/instrumen.py`:

  * Atribut privat `_nama: str`
  * Properti `nama` (getter & setter)
  * Metode abstrak `mainkan(self) -> str`
* Turunan:

  * `Gitar`: `mainkan()` → `"tring tring"`
  * `Piano`: `mainkan()` → `"tink tink"`
* Kelas `StudioMusik` di `src/music_studio/studio.py`:

  * Atribut privat `_list_instrumen: list[Instrumen]`
  * Metode:

    * `tambah_instrumen(self, instrumen: Instrumen) -> None`
    * `mainkan_instrumen(self) -> list[str]` → hasil berupa daftar string:

      ```
      "{namaInstrumen} berbunyi: {suaraInstrumen}"
      ```
* Tambahkan blok demo `if __name__ == "__main__":`.

---

### 3) Studio Seni

**Lokasi:** `src/arts/`

* Kelas abstrak `KaryaSeni` di `src/arts/karya_seni.py`:

  * Atribut privat `_judul: str`
  * Properti `judul`
  * Metode abstrak:

    * `deskripsi(self) -> str`
    * `tampilkan(self) -> str`
* Turunan:

  * `Lukisan`:

    * `deskripsi()` → `"Sebuah gambar yang dilukis di atas kanvas"`
    * `tampilkan()` → `"Digantung di dinding"`
  * `Patung`:

    * `deskripsi()` → `"Sebuah objek tiga dimensi yang dibentuk"`
    * `tampilkan()` → `"Diletakkan di atas meja atau lantai"`
* Kelas `StudioSeni` di `src/arts/studio.py`:

  * Atribut privat `_list_karya: list[KaryaSeni]`
  * Metode:

    * `tambah_karya_seni(self, karya: KaryaSeni) -> None`
    * `tampilkan_semua_karya(self) -> list[str]`

      * Mengembalikan list string hasil pemanggilan `tampilkan()` semua karya.
* Tambahkan blok demo `if __name__ == "__main__":`.

---

### 4) Notifier (Duck Typing)

**Lokasi:** `src/notify/`

* Buat kelas `Notifier` di `src/notify/notifier.py`:

  * Menyimpan daftar “pengirim” bebas tipe (`list[Any]`).
  * Metode:

    * `tambah_pengirim(self, pengirim) -> None` → simpan objek apa pun (tanpa pewarisan/ABC).
    * `kirim(self, pesan: str) -> list[str]` → untuk setiap pengirim, jika objek **memiliki** metode `kirim(pesan: str) -> str`, panggil dan kumpulkan hasilnya; jika tidak punya, **abaikan** objek tersebut.
* Buat beberapa pengirim di modul terpisah:

  * `src/notify/email_sender.py` → `EmailSender.kirim(self, pesan) -> str` mengembalikan `"Email terkirim: {pesan}"`.
  * `src/notify/sms_sender.py` → `SmsSender.kirim(self, pesan) -> str` mengembalikan `"SMS terkirim: {pesan}"`.
  * `src/notify/push_sender.py` → `PushSender.kirim(self, pesan) -> str` mengembalikan `"Push terkirim: {pesan}"`.
  * Tambahkan contoh kelas tanpa `kirim()` (mis. `BrokenSender`) untuk menunjukkan objek tersebut diabaikan.
* Demo `if __name__ == "__main__":` di `notifier.py`: daftarkan berbagai pengirim, panggil `kirim("Halo")`, dan cetak seluruh hasil.

---

### 5) ShapeRenderer (Duck Typing)

**Lokasi:** `src/render/`

* Buat kelas `ShapeRenderer` di `src/render/renderer.py`:

  * Menyimpan daftar “bentuk” bebas tipe (`list[Any]`).
  * Metode:

    * `tambah_bentuk(self, bentuk) -> None` → simpan objek apa pun.
    * `render_semua(self) -> list[str]` → iterasi semua objek; jika objek **memiliki** metode `render() -> str`, panggil dan kumpulkan hasilnya; selain itu **abaikan**.
* Buat beberapa bentuk (tanpa harus saling mewarisi):

  * `src/render/lingkaran.py` → `Lingkaran(radius)` dengan `render()` mengembalikan `"Render Lingkaran (r={radius})"`.
  * `src/render/persegi.py` → `Persegi(sisi)` dengan `render()` mengembalikan `"Render Persegi (s={sisi})"`.
  * `src/render/segitiga.py` → `Segitiga(alas, tinggi)` dengan `render()` mengembalikan `"Render Segitiga (a={alas}, t={tinggi})"`.
  * Tambahkan contoh kelas `BukanBentuk` tanpa `render()` untuk menunjukkan objek tersebut diabaikan.
* Demo `if __name__ == "__main__":` di `renderer.py`: tambahkan beberapa bentuk dan cetak hasil `render_semua()`.

---

### 6) Extra

**Lokasi:** `src/extra/extra.py`

Buat soal dan implementasi Anda sendiri menggunakan polymorphism:

* Tentukan kelas abstrak + kelas turunan.
* Lengkapi dengan atribut, properti, metode, validasi.
* Gunakan prinsip polymorphism (panggil metode abstrak via referensi ke kelas induk) **dan/atau** duck typing sesuai kebutuhan.
* Tambahkan demo `if __name__ == "__main__":`.

---

=== Selesai ===