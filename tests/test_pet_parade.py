# tests/test_pet_parade.py
import pytest

from pet_parade.hewan import Hewan, Kucing, Anjing
from pet_parade.parade import ParadeHewan


def test_hewan_is_abstract():
    # Tidak boleh bisa diinstansiasi langsung
    with pytest.raises(TypeError):
        Hewan("Si Abstrak")  # type: ignore[abstract]


@pytest.mark.parametrize(
    "bad_value,expected_exception",
    [
        ("", ValueError),
        ("   ", ValueError),
        (123, TypeError),
        (None, TypeError),
    ],
)
def test_nama_setter_validation(bad_value, expected_exception):
    with pytest.raises(expected_exception):
        Kucing(bad_value)  # type: ignore[arg-type]


def test_nama_getter_strips_whitespace():
    k = Kucing("  Mimi  ")
    a = Anjing("  Bobo\t")
    assert k.nama == "Mimi"
    assert a.nama == "Bobo"


def test_suara_kucing_anjing():
    assert Kucing("Mimi").bersuara() == "Meong"
    assert Anjing("Bobo").bersuara() == "Guk"


def test_parade_tambah_hanya_hewan():
    parade = ParadeHewan()
    parade.tambah_hewan(Kucing("Mimi"))  # valid
    with pytest.raises(TypeError):
        parade.tambah_hewan(object())  # bukan turunan Hewan


def test_parade_mulai_putaran_validasi():
    parade = ParadeHewan()
    parade.tambah_hewan(Kucing("Mimi"))
    with pytest.raises(ValueError):
        parade.mulai_parade(0)
    with pytest.raises(TypeError):
        parade.mulai_parade("2")  # type: ignore[arg-type]


def test_parade_flow_single_putaran_order_and_format():
    parade = ParadeHewan()
    k = Kucing("Mimi")
    a = Anjing("Bobo")
    parade.tambah_hewan(k)
    parade.tambah_hewan(a)

    hasil = parade.mulai_parade(1)
    assert hasil == [
        "Mimi bersuara: Meong",
        "Bobo bersuara: Guk",
    ]


def test_parade_multiple_putaran_repeats_in_order():
    parade = ParadeHewan()
    parade.tambah_hewan(Kucing("Mimi"))
    parade.tambah_hewan(Anjing("Bobo"))
    parade.tambah_hewan(Kucing("Ciko"))

    putaran = 3
    hasil = parade.mulai_parade(putaran)

    # Total baris = jumlah hewan * putaran
    assert len(hasil) == 3 * putaran

    # Pola urutan per putaran harus konsisten
    expected_once = [
        "Mimi bersuara: Meong",
        "Bobo bersuara: Guk",
        "Ciko bersuara: Meong",
    ]
    # Bagi menjadi chunk per putaran dan bandingkan
    for i in range(putaran):
        start = i * 3
        end = start + 3
        assert hasil[start:end] == expected_once


def test_hapus_hewan_idempotent():
    parade = ParadeHewan()
    k = Kucing("Mimi")
    a = Anjing("Bobo")
    parade.tambah_hewan(k)
    parade.tambah_hewan(a)

    # Hapus satu kali
    parade.hapus_hewan(k)
    # Pastikan tidak muncul di hasil parade
    hasil = parade.mulai_parade(1)
    assert all("Mimi" not in line for line in hasil)
    assert any("Bobo" in line for line in hasil)

    # Hapus lagi (tidak error meskipun sudah tidak ada)
    parade.hapus_hewan(k)
    # Tetap normal
    hasil2 = parade.mulai_parade(1)
    assert all("Mimi" not in line for line in hasil2)
