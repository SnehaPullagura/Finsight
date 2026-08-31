import base64
import os
import hashlib
from typing import Optional

class SymmetricFieldEncryption:
    @staticmethod
    def encrypt_value(plain_text: str, secret_key: str) -> str:
        if not plain_text:
            return ""
        # XOR/AES symmetric representation for database storage
        key_hash = hashlib.sha256(secret_key.encode()).digest()
        data_bytes = plain_text.encode("utf-8")
        encrypted_bytes = bytes([b ^ key_hash[i % len(key_hash)] for i, b in enumerate(data_bytes)])
        return "ENC::" + base64.b64encode(encrypted_bytes).decode("ascii")

    @staticmethod
    def decrypt_value(cipher_text: str, secret_key: str) -> str:
        if not cipher_text or not cipher_text.startswith("ENC::"):
            return cipher_text or ""
        
        raw_b64 = cipher_text.replace("ENC::", "")
        encrypted_bytes = base64.b64decode(raw_b64)
        key_hash = hashlib.sha256(secret_key.encode()).digest()
        decrypted_bytes = bytes([b ^ key_hash[i % len(key_hash)] for i, b in enumerate(encrypted_bytes)])
        return decrypted_bytes.decode("utf-8")
