# tests/test_arts_studio.py
import pytest

from arts.karya_seni import KaryaSeni, Lukisan, Patung
from arts.studio import StudioSeni


def test_karya_seni_is_abstract():
    with pytest.raises(TypeError):
        KaryaSeni("Abstrak")  # type: ignore[abstract]


@pytest.mark.parametrize(
    "bad_value,exc",
    [
        ("", ValueError),
        ("   ", ValueError),
        (123, TypeError),
        (None, TypeError),
    ],
)
def test_judul_validation(bad_value, exc):
    with pytest.raises(exc):
        Lukisan(bad_value)  # type: ignore[arg-type]


def test_judul_trimming():
    l = Lukisan("  Pemandangan  ")
    p = Patung("\tPenari\n")
    assert l.judul == "Pemandangan"
    assert p.judul == "Penari"


def test_deskripsi_and_tampilkan_exact_strings():
    l = Lukisan("L1")
    p = Patung("P1")
    assert l.deskripsi() == "Sebuah gambar yang dilukis di atas kanvas"
    assert l.tampilkan() == "Digantung di dinding"
    assert p.deskripsi() == "Sebuah objek tiga dimensi yang dibentuk"
    assert p.tampilkan() == "Diletakkan di atas meja atau lantai"


def test_tambah_karya_seni_hanya_turunan_karya_seni():
    studio = StudioSeni()
    studio.tambah_karya_seni(Lukisan("L1"))  # valid
    with pytest.raises(TypeError):
        studio.tambah_karya_seni(object())  # bukan turunan KaryaSeni


def test_tampilkan_semua_karya_order_and_content():
    studio = StudioSeni()
    l = Lukisan("Senja")
    p = Patung("Ornamen")
    studio.tambah_karya_seni(l)
    studio.tambah_karya_seni(p)

    hasil = studio.tampilkan_semua_karya()
    assert hasil == [
        "Digantung di dinding",
        "Diletakkan di atas meja atau lantai",
    ]


def test_tampilkan_semua_karya_empty():
    studio = StudioSeni()
    assert studio.tampilkan_semua_karya() == []


def test_update_judul_via_setter_reflected():
    l = Lukisan("Awal")
    assert l.judul == "Awal"
    l.judul = "  Baru  "
    assert l.judul == "Baru"
