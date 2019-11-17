import dataclasses

from kadena import types

work_header_bytes = bytes.fromhex(
    "05000000d3a6e63c5b5767267eb9021d98be2333d4af4bd3d1df740f7fffc70a000000000000000000000000fa5b1b55de9605006d4503feb42b2494cacf9bd1b1998300c53cc31c3c0601a427e159a586befc3e030000000000022442d2f610b4db056a254b8c34378fdab681651c379a9d82b07eee5b242775060000007972e7a310a9941a5f77c5b864cc21ae95a9c72712f5e9d876b79dd7db45280f090000008019cf71bcdbe10621b75d9364a3a3ebe8a5bd546bc4924e61a3aa1672994ec2d3a6e63c5b5767267eb9021d98be2333d4af4bd3d1df740f7fffc70a0000000077c681d5bb4290eb0fa481bc8b1d703883c0e3e4fb41ad78012762a15a1ffbe105000000b452fc44ba010100000000000000000000000000000000000000000000000000307100000000000005000000aadbc3f0dd9605000000000000000000"
)

decoded_work_header = types.WorkHeader(
    chain=5,
    target="06bmPFtXZyZ-uQIdmL4jM9SvS9PR33QPf__HCgAAAAA",
    nonce=0,
    time=1573256538315770,
    parent="bUUD_rQrJJTKz5vRsZmDAMU8wxw8BgGkJ-FZpYa-_D4",
    adjacents={
        0: "AiRC0vYQtNsFaiVLjDQ3j9q2gWUcN5qdgrB-7lskJ3U",
        6: "eXLnoxCplBpfd8W4ZMwhrpWpxycS9enYdred19tFKA8",
        9: "gBnPcbzb4QYht12TZKOj6-ilvVRrxJJOYaOqFnKZTsI",
    },
    payload="d8aB1btCkOsPpIG8ix1wOIPA4-T7Qa14ASdioVof--E",
    weight=283374509642420,
    height=28976,
    version=5,
    epoch_start=1573254854859690,
    flags=0,
    difficulty=101983759913,
)

block_header = types.BlockHeader(
    nonce=8305999242,
    time=1573381243298146,
    parent="0ksoqElFS1O92ELs4H9eJVw1GpwhyvMm2ghsvuk8oTg",
    adjacents={
        4: "WROEIBmF5Tj1GpWN3sFjqkNji3o8u5jmKZyhLlHtSBQ",
        5: "Y119tFyVzf0ZkDa1fr_loPkgP_2o--UbrdZRXEC-ht8",
        8: "OBEvbGZFJC1pKJOf9kCklZpLKVK7LMkyK3TDd8Qyjn8",
    },
    target="HNCMLDL-Iq96jjq6Sy4wbTREcvRSgPmXWHCmBgAAAAA",
    payload="ajRtuwfvpXKukOzDNVHoJxqi5eW9vKdogdEtLE437Ro",
    chain=9,
    weight=737270491038141,
    height=33157,
    version="mainnet01",
    epoch_start=1573380104334007,
    flags=0,
    hash="Yui29I2k4S0BQiIRNR1vdsvxoyzBliCQIWomn--bZjU",
    difficulty=165336321130,
)
block_header_int_version = dataclasses.replace(block_header, version=5)

block_header_base64 = "in0T7wEAAABiYRpe-5YFANJLKKhJRUtTvdhC7OB_XiVcNRqcIcrzJtoIbL7pPKE4AwAEAAAAWROEIBmF5Tj1GpWN3sFjqkNji3o8u5jmKZyhLlHtSBQFAAAAY119tFyVzf0ZkDa1fr_loPkgP_2o--UbrdZRXEC-ht8IAAAAOBEvbGZFJC1pKJOf9kCklZpLKVK7LMkyK3TDd8Qyjn8c0IwsMv4ir3qOOrpLLjBtNERy9FKA-ZdYcKYGAAAAAGo0bbsH76VyrpDswzVR6CcaouXlvbynaIHRLSxON-0aCQAAAL3BuCmLngIAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAhYEAAAAAAAAFAAAAtyo3GvuWBQAAAAAAAAAAAGLotvSNpOEtAUIiETUdb3bL8aMswZYgkCFqJp_vm2Y1"
block_header_bytes = bytes.fromhex(
    "8a7d13ef0100000062611a5efb960500d24b28a849454b53bdd842ece07f5e255c351a9c21caf326da086cbee93ca138030004000000591384201985e538f51a958ddec163aa43638b7a3cbb98e6299ca12e51ed481405000000635d7db45c95cdfd199036b57ebfe5a0f9203ffda8fbe51badd6515c40be86df0800000038112f6c6645242d6928939ff640a4959a4b2952bb2cc9322b74c377c4328e7f1cd08c2c32fe22af7a8e3aba4b2e306d344472f45280f9975870a606000000006a346dbb07efa572ae90ecc33551e8271aa2e5e5bdbca76881d12d2c4e37ed1a09000000bdc1b8298b9e0200000000000000000000000000000000000000000000000000858100000000000005000000b72a371afb960500000000000000000062e8b6f48da4e12d01422211351d6f76cbf1a32cc1962090216a269fef9b6635"
)
block_header_object = {
    "creationTime": 1573381243298146,
    "parent": "0ksoqElFS1O92ELs4H9eJVw1GpwhyvMm2ghsvuk8oTg",
    "height": 33157,
    "hash": "Yui29I2k4S0BQiIRNR1vdsvxoyzBliCQIWomn--bZjU",
    "chainId": 9,
    "weight": "vcG4KYueAgAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA",
    "featureFlags": 0,
    "epochStart": 1573380104334007,
    "adjacents": {
        "4": "WROEIBmF5Tj1GpWN3sFjqkNji3o8u5jmKZyhLlHtSBQ",
        "5": "Y119tFyVzf0ZkDa1fr_loPkgP_2o--UbrdZRXEC-ht8",
        "8": "OBEvbGZFJC1pKJOf9kCklZpLKVK7LMkyK3TDd8Qyjn8",
    },
    "payloadHash": "ajRtuwfvpXKukOzDNVHoJxqi5eW9vKdogdEtLE437Ro",
    "chainwebVersion": "mainnet01",
    "target": "HNCMLDL-Iq96jjq6Sy4wbTREcvRSgPmXWHCmBgAAAAA",
    "nonce": "8305999242",
}


def test_decode_work_header():
    assert types.decode_header(work_header_bytes) == decoded_work_header


def test_decode_block_header_base64():
    assert types.decode_header(block_header_base64) == block_header_int_version


def test_decode_block_header_bytes():
    assert types.decode_header(block_header_bytes) == block_header_int_version


def test_decode_block_header_object():
    assert types.decode_header(block_header_object) == block_header
