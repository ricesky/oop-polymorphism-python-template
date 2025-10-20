# tests/test_render.py
import pytest

from render.renderer import ShapeRenderer
from render.lingkaran import Lingkaran
from render.persegi import Persegi
from render.segitiga import Segitiga
from render.bukan_bentuk import BukanBentuk


# ---------- Konstruktor & validasi parameter ----------

@pytest.mark.parametrize(
    "val,exc",
    [
        (0, ValueError),
        (-1, ValueError),
        ("a", TypeError),
        (None, TypeError),
        ([], TypeError),
    ],
)
def test_lingkaran_validasi_radius(val, exc):
    with pytest.raises(exc):
        Lingkaran(val)  # type: ignore[arg-type]


@pytest.mark.parametrize(
    "val,exc",
    [
        (0, ValueError),
        (-2.5, ValueError),
        ("x", TypeError),
        (None, TypeError),
        ({}, TypeError),
    ],
)
def test_persegi_validasi_sisi(val, exc):
    with pytest.raises(exc):
        Persegi(val)  # type: ignore[arg-type]


@pytest.mark.parametrize(
    "alas,tinggi,exc",
    [
        (0, 1, ValueError),
        (1, 0, ValueError),
        (-1, 2, ValueError),
        (3, -2, ValueError),
        ("a", 1, TypeError),
        (1, "b", TypeError),
        (None, 1, TypeError),
        (1, None, TypeError),
    ],
)
def test_segitiga_validasi(alas, tinggi, exc):
    with pytest.raises(exc):
        Segitiga(alas, tinggi)  # type: ignore[arg-type]


def test_properties_getter_values():
    l = Lingkaran(5)
    p = Persegi(4)
    s = Segitiga(3, 6)
    assert l.radius == 5.0
    assert p.sisi == 4.0
    assert s.alas == 3.0 and s.tinggi == 6.0


# ---------- Perilaku render & urutan ----------

def test_render_exact_strings_for_nominal_values():
    l = Lingkaran(5)
    p = Persegi(4)
    s = Segitiga(3, 6)
    assert l.render() == "Render Lingkaran (r=5)"
    assert p.render() == "Render Persegi (s=4)"
    assert s.render() == "Render Segitiga (a=3, t=6)"


def test_shape_renderer_mengabaikan_objek_tanpa_render():
    r = ShapeRenderer()
    r.tambah_bentuk(BukanBentuk())  # tidak punya .render()
    r.tambah_bentuk(object())        # tidak punya .render()
    assert r.render_semua() == []


def test_shape_renderer_mengumpulkan_dari_semua_shape_dengan_urutan():
    r = ShapeRenderer()
    r.tambah_bentuk(Lingkaran(5))
    r.tambah_bentuk(Persegi(4))
    r.tambah_bentuk(Segitiga(3, 6))
    r.tambah_bentuk(BukanBentuk())  # diabaikan

    out = r.render_semua()
    assert out == [
        "Render Lingkaran (r=5)",
        "Render Persegi (s=4)",
        "Render Segitiga (a=3, t=6)",
    ]


def test_shape_renderer_kosong():
    r = ShapeRenderer()
    assert r.render_semua() == []


# ---------- Edge cases duck typing ----------

def test_shape_renderer_mengonversi_non_string_return_ke_string():
    class WeirdShape:
        def render(self):
            return 123  # bukan string

    r = ShapeRenderer()
    r.tambah_bentuk(WeirdShape())
    assert r.render_semua() == ["123"]


def test_shape_renderer_meneruskan_exception_dari_render():
    class BadShape:
        def render(self):
            raise RuntimeError("boom")

    r = ShapeRenderer()
    r.tambah_bentuk(BadShape())
    with pytest.raises(RuntimeError, match="boom"):
        r.render_semua()
