import struct
from dataclasses import dataclass
from typing import Dict


@dataclass
class BlockHeader:
    chain: int
    hash_target: str
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
    def from_binary(cls, data: bytes):
        """
        Decode work header from binary format.

        See also:
            https://github.com/kadena-io/chainweb-node/wiki/Block-Header-Binary-Encoding
        """
        fields = list(struct.unpack("<i32sqq32s110s32s32si32sqiqq", data))
        fields.pop(6)  # duplicate hash_target
        fields.pop(7)  # duplicate chain
        num, adjacent = struct.unpack("<h108s", fields[5])
        adjacent = struct.unpack("<" + "i32s" * num, adjacent)
        fields[5] = {chain: adj_hash.hex() for chain, adj_hash in zip(adjacent[::2], adjacent[1::2])}
        fields[7] = int.from_bytes(fields[7], "little")  # weight
        fields.append(2 ** 256 // int.from_bytes(fields[1], "little"))  # difficulty
        fields[1] = fields[1].hex()  # hash_target
        fields[4] = fields[4].hex()  # parent
        fields[6] = fields[6].hex()  # payload
        return cls(*fields)
