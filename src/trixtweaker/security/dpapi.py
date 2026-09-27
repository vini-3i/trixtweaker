"""Criptografia DPAPI via ctypes (stdlib puro)."""
from __future__ import annotations
import ctypes
import json
import os
from pathlib import Path


class DATA_BLOB(ctypes.Structure):
    """Estrutura BLOB da API CryptProtectData."""

    _fields_ = [("cbData", ctypes.c_uint32),
                ("pbData", ctypes.POINTER(ctypes.c_byte))]


def _blob_to_bytes(blob: DATA_BLOB) -> bytes:
    """Converte DATA_BLOB em bytes."""
    return ctypes.string_at(blob.pbData, blob.cbData)


def _bytes_to_blob(data: bytes) -> DATA_BLOB:
    """Converte bytes em DATA_BLOB."""
    buf = ctypes.create_string_buffer(data, len(data))
    return DATA_BLOB(len(data), ctypes.cast(buf, ctypes.POINTER(ctypes.c_byte)))


def dpapi_encrypt(plaintext: bytes) -> bytes:
    """Cifra bytes com DPAPI (no-op fora do Windows)."""
    if os.name != "nt":
        return plaintext
    try:
        in_blob = _bytes_to_blob(plaintext)
        out_blob = DATA_BLOB()
        ok = ctypes.windll.crypt32.CryptProtectData(
            ctypes.byref(in_blob), None, None, None, None, 0,
            ctypes.byref(out_blob)
        )
        if not ok:
            return plaintext
        try:
            return _blob_to_bytes(out_blob)
        finally:
            ctypes.windll.kernel32.LocalFree(out_blob.pbData)
    except Exception:
        return plaintext


def dpapi_decrypt(ciphertext: bytes) -> bytes:
    """Decifra bytes com DPAPI (no-op fora do Windows)."""
    if os.name != "nt":
        return ciphertext
    try:
        in_blob = _bytes_to_blob(ciphertext)
        out_blob = DATA_BLOB()
        ok = ctypes.windll.crypt32.CryptUnprotectData(
            ctypes.byref(in_blob), None, None, None, None, 0,
            ctypes.byref(out_blob)
        )
        if not ok:
            return ciphertext
        try:
            return _blob_to_bytes(out_blob)
        finally:
            ctypes.windll.kernel32.LocalFree(out_blob.pbData)
    except Exception:
        return ciphertext


def secure_write(path: Path, data: dict) -> None:
    """Escreve dict em disco cifrado com DPAPI."""
    try:
        raw = json.dumps(data, ensure_ascii=False).encode("utf-8")
        enc = dpapi_encrypt(raw)
        path.write_bytes(enc)
    except Exception:
        pass


def secure_read(path: Path) -> dict:
    """Le dict cifrado do disco (fallback para JSON puro)."""
    if not path.exists():
        return {}
    try:
        raw = path.read_bytes()
        dec = dpapi_decrypt(raw)
        try:
            return json.loads(dec.decode("utf-8"))
        except Exception:
            try:
                return json.loads(raw.decode("utf-8"))
            except Exception:
                return {}
    except Exception:
        return {}
