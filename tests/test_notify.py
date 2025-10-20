# tests/test_notify.py
import pytest

from notify.notifier import Notifier
from notify.email_sender import EmailSender
from notify.sms_sender import SmsSender
from notify.push_sender import PushSender
from notify.broken_sender import BrokenSender


def test_notifier_collects_from_all_senders_and_ignores_broken():
    n = Notifier()
    n.tambah_pengirim(EmailSender("postmaster@example.com"))
    n.tambah_pengirim(SmsSender("+62812"))
    n.tambah_pengirim(PushSender("dev-1"))
    n.tambah_pengirim(BrokenSender())  # tidak punya .kirim → diabaikan

    out = n.kirim("Halo")
    assert out == [
        "Email terkirim: Halo",
        "SMS terkirim: Halo",
        "Push terkirim: Halo",
    ]


def test_notifier_ignores_objects_without_kirim_entirely():
    n = Notifier()
    n.tambah_pengirim(object())
    n.tambah_pengirim({"no": "method"})
    n.tambah_pengirim(BrokenSender())

    out = n.kirim("apa saja")
    assert out == []


def test_notifier_preserves_sender_order():
    n = Notifier()
    n.tambah_pengirim(SmsSender("1"))
    n.tambah_pengirim(EmailSender("a@b.c"))
    n.tambah_pengirim(PushSender("X"))

    out = n.kirim("Ping")
    assert out == [
        "SMS terkirim: Ping",
        "Email terkirim: Ping",
        "Push terkirim: Ping",
    ]


def test_notifier_validates_pesan_type():
    n = Notifier()
    n.tambah_pengirim(EmailSender("a@b.c"))
    with pytest.raises(TypeError):
        n.kirim(123)  # type: ignore[arg-type]


def test_notifier_coerces_non_string_return_to_string():
    class OddSender:
        def kirim(self, pesan: str):
            return 42  # bukan string

    n = Notifier()
    n.tambah_pengirim(OddSender())
    out = n.kirim("X")
    assert out == ["42"]


def test_notifier_bubbles_up_exception_from_sender():
    class BadSender:
        def kirim(self, pesan: str) -> str:
            raise RuntimeError("boom")

    n = Notifier()
    n.tambah_pengirim(BadSender())
    with pytest.raises(RuntimeError, match="boom"):
        n.kirim("test")
