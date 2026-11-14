"""
Tests for Security & Authentication (Phase 1)
"""

import pytest
from app.utils.security import hash_password, verify_password, create_access_token, decode_token


def test_password_hashing():
    raw = "SecurePassword123!"
    hashed = hash_password(raw)

    assert hashed != raw
    assert verify_password(raw, hashed) is True
    assert verify_password("WrongPassword!", hashed) is False


def test_password_longer_than_72_bytes_handled():
    """Verify that bcrypt 72-byte truncation boundary is safely handled without raising exception."""
    long_pwd = "A" * 150
    hashed = hash_password(long_pwd)

    assert verify_password(long_pwd, hashed) is True
    assert verify_password("B" * 150, hashed) is False


def test_jwt_token_encode_decode():
    payload = {"sub": "user-12345", "role": "developer"}
    token = create_access_token(payload)

    decoded = decode_token(token)
    assert decoded["sub"] == "user-12345"
    assert decoded["role"] == "developer"
    assert "exp" in decoded
