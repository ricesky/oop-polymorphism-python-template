# tests/test_music_studio.py
import pytest

from music_studio.instrumen import Instrumen, Gitar, Piano
from music_studio.studio import StudioMusik


def test_instrumen_is_abstract():
    with pytest.raises(TypeError):
        Instrumen("Abstrak")  # type: ignore[abstract]


@pytest.mark.parametrize(
    "bad_value,exc",
    [
        ("", ValueError),
        ("   ", ValueError),
        (123, TypeError),
        (None, TypeError),
    ],
)
def test_nama_validation(bad_value, exc):
    with pytest.raises(exc):
        Gitar(bad_value)  # type: ignore[arg-type]


def test_nama_trimming():
    g = Gitar("  Fender  ")
    p = Piano("\tYamaha U1\n")
    assert g.nama == "Fender"
    assert p.nama == "Yamaha U1"


def test_bunyi_gitar_piano():
    assert Gitar("G1").mainkan() == "tring tring"
    assert Piano("P1").mainkan() == "tink tink"


def test_tambah_instrumen_hanya_turunan_instrumen():
    studio = StudioMusik()
    studio.tambah_instrumen(Gitar("G1"))
    with pytest.raises(TypeError):
        studio.tambah_instrumen(object())  # bukan turunan Instrumen


def test_mainkan_instrumen_format_and_order():
    studio = StudioMusik()
    g = Gitar("Fender Stratocaster")
    p = Piano("Yamaha U1")
    studio.tambah_instrumen(g)
    studio.tambah_instrumen(p)

    hasil = studio.mainkan_instrumen()
    assert hasil == [
        "Fender Stratocaster berbunyi: tring tring",
        "Yamaha U1 berbunyi: tink tink",
    ]


def test_mainkan_instrumen_kosong():
    studio = StudioMusik()
    assert studio.mainkan_instrumen() == []


def test_multiple_adds_and_call_multiple_times_idempotent():
    studio = StudioMusik()
    studio.tambah_instrumen(Gitar("G1"))
    studio.tambah_instrumen(Piano("P1"))

    first = studio.mainkan_instrumen()
    second = studio.mainkan_instrumen()

    assert first == [
        "G1 berbunyi: tring tring",
        "P1 berbunyi: tink tink",
    ]
    assert second == first
