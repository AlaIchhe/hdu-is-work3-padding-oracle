"""Local teaching service for a CBC padding-oracle demonstration.

The service is intentionally vulnerable and must only be run on localhost.
"""

from __future__ import annotations

import base64
import os

from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from flask import Flask, jsonify, request


BLOCK_SIZE = 16
DEMO_KEY = bytes.fromhex(
    "603deb1015ca71be2b73aef0857d7781"
    "1f352c073b6108d72d9810a30914dff4"
)
PLAINTEXT = b"role=user;uid=1001;ok=1"


def _encrypt(plaintext: bytes) -> bytes:
    padder = padding.PKCS7(BLOCK_SIZE * 8).padder()
    padded = padder.update(plaintext) + padder.finalize()
    iv = os.urandom(BLOCK_SIZE)
    encryptor = Cipher(algorithms.AES(DEMO_KEY), modes.CBC(iv)).encryptor()
    ciphertext = encryptor.update(padded) + encryptor.finalize()
    return iv + ciphertext


def _decrypt(token: bytes) -> bytes:
    if len(token) < BLOCK_SIZE * 2 or (len(token) - BLOCK_SIZE) % BLOCK_SIZE:
        raise ValueError("ciphertext length is invalid")
    iv, ciphertext = token[:BLOCK_SIZE], token[BLOCK_SIZE:]
    decryptor = Cipher(algorithms.AES(DEMO_KEY), modes.CBC(iv)).decryptor()
    padded = decryptor.update(ciphertext) + decryptor.finalize()
    unpadder = padding.PKCS7(BLOCK_SIZE * 8).unpadder()
    return unpadder.update(padded) + unpadder.finalize()


def _parse_session(plaintext: bytes) -> dict[str, str]:
    try:
        text = plaintext.decode("ascii")
    except UnicodeDecodeError as exc:
        raise ValueError("session is not ASCII") from exc

    fields: dict[str, str] = {}
    for item in text.split(";"):
        key, separator, value = item.partition("=")
        if not separator or not key or not value:
            raise ValueError("session field is malformed")
        fields[key] = value

    required = {"role", "uid", "ok"}
    if not required.issubset(fields):
        raise ValueError("session fields are missing")
    return fields


def create_app() -> Flask:
    app = Flask(__name__)

    @app.get("/session")
    def issue_session():
        cookie = base64.b64encode(_encrypt(PLAINTEXT)).decode("ascii")
        return jsonify(cookie=cookie, note="educational localhost target")

    @app.post("/account")
    def account():
        body = request.get_json(silent=True) or {}
        cookie = body.get("cookie")
        if not isinstance(cookie, str):
            return jsonify(error="missing cookie"), 400
        try:
            token = base64.b64decode(cookie, validate=True)
        except (ValueError, TypeError):
            return jsonify(error="invalid encoding"), 400

        try:
            plaintext = _decrypt(token)
        except ValueError:
            # Deliberately distinguishable: this is the padding oracle.
            return jsonify(error="invalid padding"), 400

        try:
            fields = _parse_session(plaintext)
        except ValueError:
            return jsonify(error="invalid payload"), 422

        if fields["role"] == "root":
            return jsonify(
                role="root",
                access="admin console",
                flag="FLAG{padding_oracle_demo}",
            )
        if fields["role"] == "user":
            return jsonify(role="user", access="user dashboard")
        return jsonify(error="unknown role"), 403

    @app.get("/health")
    def health():
        return jsonify(status="ok")

    return app


app = create_app()


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5053, debug=False)
