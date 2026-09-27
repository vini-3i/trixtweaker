"""Roundtrip DPAPI e secure_read/write."""
import sys
import tempfile
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))
from trixtweaker.security.dpapi import dpapi_decrypt, dpapi_encrypt, secure_read, secure_write


def test_roundtrip():
    """Encrypt/decrypt preserva bytes."""
    data = b"trix-test-123"
    enc = dpapi_encrypt(data)
    dec = dpapi_decrypt(enc)
    assert dec == data


def test_secure_write_read(tmp_path=None):
    """secure_write/secure_read preservam dict."""
    if tmp_path is None:
        d = Path(tempfile.mkdtemp()) / "c.enc"
    else:
        d = Path(str(tmp_path)) / "c.enc"
    secure_write(d, {"lang": "pt", "sound": True})
    assert secure_read(d) == {"lang": "pt", "sound": True}
