import struct
from dataclasses import dataclass
from typing import Dict, Union

from kadena import utils

MAX_BOUND = 2 ** 256 - 1


def decode_header(data):
    """
    Decode block or work header from binary, base64 or object encoding.
    """
    if isinstance(data, dict):
        return BlockHeader.from_object(data)
    if isinstance(data, str):
        data = utils.base64_to_bytes(data)
    if len(data) == 318:
        return BlockHeader.from_bytes(data)
    if len(data) == 322:
        return WorkHeader.from_bytes(data)
    raise ValueError("encoded header should be 318 or 322 bytes, got %d bytes", len(data))


def get_adjacents(data: bytes) -> Dict[int, str]:
    """
    Decode adjacent parent block hashes.
    """
    num, data = struct.unpack("<h108s", data)
    adj = struct.unpack("<" + "i32s" * num, data)
    return {chain: utils.bytes_to_base64(block) for chain, block in zip(adj[::2], adj[1::2])}


@dataclass
class BlockHeader:
    nonce: int
    time: int
    parent: str
    adjacents: Dict[int, str]
    target: str
    payload: str
    chain: int
    weight: int
    height: int
    version: Union[int, str]  # examples: "mainnet01" or 5
    epoch_start: int
    flags: int
    hash: str
    difficulty: int = None

    @classmethod
    def from_bytes(cls, data: bytes):
        """
        Size   Bytes    Value
        8      0        nonce
        8      8-15     time
        32     16-47    parent
        110    48-157   adjacents
        32     158-189  target
        32     190-221  payload
        4      222-225  chain
        32     226-257  weight
        8      258-265  height
        4      266-269  version
        8      270-277  epoch start
        8      278-285  flags
        32     286-317  hash
        """
        assert len(data) == 318
        fields = list(struct.unpack("<qq32s110s32s32si32sqiqq32s", data))
        return cls(
            nonce=fields[0],
            time=fields[1],
            parent=utils.bytes_to_base64(fields[2]),
            adjacents=get_adjacents(fields[3]),
            target=utils.bytes_to_base64(fields[4]),
            payload=utils.bytes_to_base64(fields[5]),
            chain=fields[6],
            weight=int.from_bytes(fields[7], "little"),
            height=fields[8],
            version=fields[9],
            epoch_start=fields[10],
            flags=fields[11],
            hash=utils.bytes_to_base64(fields[12]),
            difficulty=MAX_BOUND // int.from_bytes(fields[4], "little"),
        )

    @classmethod
    def from_object(cls, data):
        return cls(
            nonce=int(data["nonce"]),
            time=data["creationTime"],
            parent=data["parent"],
            adjacents={int(chain): block for chain, block in data["adjacents"].items()},
            target=data["target"],
            payload=data["payloadHash"],
            chain=data["chainId"],
            weight=utils.base64_to_int(data["weight"]),
            height=data["height"],
            version=data["chainwebVersion"],  # str
            epoch_start=data["epochStart"],
            flags=data["featureFlags"],
            hash=data["hash"],
            difficulty=MAX_BOUND // utils.base64_to_int(data["target"]),
        )


@dataclass
class WorkHeader:
    chain: int
    target: str
    nonce: int
    time: int
    parent: str
    adjacents: Dict[int, str]  # chain -> hash
    payload: str
    weight: int
    height: int
    version: int
    epoch_start: int
    flags: int
    difficulty: int

    @classmethod
    def from_bytes(cls, data: bytes):
        """
        Size   Bytes    Value
        4      0-3      chain
        32     4-35     hash-target
        8      36-43    nonce
        8      44-51    time
        32     52-83    parent
        110    84-193   adjacents
        32     194-225  target
        32     226-257  payload
        4      258-261  chain
        32     262-293  weight
        8      294-301  height
        4      302-305  version
        8      306-313  epoch start
        8      314-321  flags
        32     286-317  target
        """
        assert len(data) == 322
        fields = list(struct.unpack("<i32sqq32s110s32s32si32sqiqq", data))
        return cls(
            chain=fields[0],
            target=utils.bytes_to_base64(fields[1]),
            nonce=fields[2],
            time=fields[3],
            parent=utils.bytes_to_base64(fields[4]),
            adjacents=get_adjacents(fields[5]),
            payload=utils.bytes_to_base64(fields[7]),
            weight=int.from_bytes(fields[9], "little"),
            height=fields[10],
            version=fields[11],
            epoch_start=fields[12],
            flags=fields[13],
            difficulty=MAX_BOUND // int.from_bytes(fields[1], "little"),
        )
