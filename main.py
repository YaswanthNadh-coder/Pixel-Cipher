from PIL import Image
import random
import os
from typing import List

def _password_bytes(password: str) -> bytes:
    return password.encode('utf-8')

def vigenere_encrypt(message: str, password: str) -> bytes:
    
    msg_bytes = message.encode('utf-8')
    key = _password_bytes(password)
    if not key:
        raise ValueError("Password cannot be empty.")
    out = bytearray(len(msg_bytes))
    for i, b in enumerate(msg_bytes):
        k = key[i % len(key)]
        out[i] = (b + k) % 256
    return bytes(out)

def vigenere_decrypt(cipher_bytes: bytes, password: str) -> str:
   
    key = _password_bytes(password)
    if not key:
        raise ValueError("Password cannot be empty.")
    out = bytearray(len(cipher_bytes))
    for i, b in enumerate(cipher_bytes):
        k = key[i % len(key)]
        out[i] = (b - k) % 256
    return out.decode('utf-8', errors='strict')


def text_to_bits(data: bytes) -> List[int]:
    bits = []
    for b in data:
        for i in range(8):
            bits.append((b >> (7 - i)) & 1)
    return bits

def bits_to_bytes(bits: List[int]) -> bytes:
    if len(bits) % 8 != 0:
        raise ValueError("Bits length must be multiple of 8.")
    out = bytearray(len(bits) // 8)
    for i in range(0, len(bits), 8):
        byte = 0
        for j in range(8):
            byte = (byte << 1) | (bits[i + j] & 1)
        out[i // 8] = byte
    return bytes(out)

def _set_lsb(value: int, bit: int) -> int:
    return (value & 0xFE) | (bit & 1)

def _get_lsb(value: int) -> int:
    return value & 1