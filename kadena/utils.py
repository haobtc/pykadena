import base64
import json


def base64_to_bytes(data: str) -> bytes:
    """
    Convert unpadded base64-url to ``bytes``.
    """
    return base64.urlsafe_b64decode(data + "=" * (-len(data) % 4))


def base64_to_dict(data: str) -> dict:
    """
    Convert unpadded base64-url with json data to ``dict``.
    """
    return json.loads(base64_to_bytes(data))


def base64_to_int(data: str) -> int:
    """
    Convert unpadded base64-url with little-endian integer to ``int``.
    """
    return int.from_bytes(base64_to_bytes(data), "little")


def bytes_to_base64(data: bytes) -> str:
    """
    Convert ``bytes`` to unpadded base64-url string.
    """
    return base64.urlsafe_b64encode(data).decode().rstrip("=")
