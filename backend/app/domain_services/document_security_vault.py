import hashlib
from typing import Any, Dict, List, Optional

class DocumentSecurityVault:
    @staticmethod
    def compute_sha256_checksum(content_bytes: bytes) -> str:
        return hashlib.sha256(content_bytes).hexdigest()

    @staticmethod
    def verify_document_integrity(content_bytes: bytes, expected_checksum: str) -> bool:
        computed = DocumentSecurityVault.compute_sha256_checksum(content_bytes)
        return computed.lower() == expected_checksum.lower()
