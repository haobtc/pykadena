from json.decoder import JSONDecodeError
from ssl import SSLError

from httpx import ProtocolError, ConnectTimeout, ReadTimeout, HTTPError

CONNECTION_ERRORS = (
    ProtocolError,
    ConnectTimeout,
    ReadTimeout,
    SSLError,
    OSError,
    ConnectionResetError,
    ConnectionRefusedError,
    JSONDecodeError,
    HTTPError,
)

MINING_REQUEST = {
    "account": "ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff",
    "predicate": "keys-all",
    "public-keys": ["ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff"],
}

ENCODINGS = {
    "binary": "application/octet-stream",
    "base64": "application/json",
    "object": "application/json;blockheader-encoding=object",
}

MAX_BOUND = 2 ** 256 - 1
