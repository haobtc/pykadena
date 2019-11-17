from kadena import utils

payload_base64 = "eyJhY2NvdW50IjoiZTdmNzYzNGU5MjU1NDFmMzY4YjgyN2FkNWM3MjQyMTkwNTEwMGY2MjA1Mjg1YTc4YzE5ZDdiNGEzODcxMTgwNSIsInByZWRpY2F0ZSI6ImtleXMtYWxsIiwicHVibGljLWtleXMiOlsiZTdmNzYzNGU5MjU1NDFmMzY4YjgyN2FkNWM3MjQyMTkwNTEwMGY2MjA1Mjg1YTc4YzE5ZDdiNGEzODcxMTgwNSJdfQ"
payload_bytes = b'{"account":"e7f7634e925541f368b827ad5c72421905100f6205285a78c19d7b4a38711805","predicate":"keys-all","public-keys":["e7f7634e925541f368b827ad5c72421905100f6205285a78c19d7b4a38711805"]}'
payload_dict = {
    "account": "e7f7634e925541f368b827ad5c72421905100f6205285a78c19d7b4a38711805",
    "predicate": "keys-all",
    "public-keys": ["e7f7634e925541f368b827ad5c72421905100f6205285a78c19d7b4a38711805"],
}


def test_encode_base64():
    assert utils.bytes_to_base64(payload_bytes) == payload_base64


def test_decode_base64():
    assert utils.base64_to_bytes(payload_base64) == payload_bytes


def test_decode_dict():
    assert utils.base64_to_dict(payload_base64) == payload_dict


def test_decode_int():
    assert utils.base64_to_int("N_grpZ05rQQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA") == 336988896366426167
