from typing import List

def getHash(message: str)->str:
    #calculates a simple ASCII value sum of all characters in the message so that we can check if the password entered is correct or not
    total=0
    for char in message:
        total+=ord(char)
    return str(total)

def _password_bytes(password: str) -> bytes:
    return password.encode('utf-8')

def vigenere_encrypt(message: str, password: str) -> bytes:
    hash=getHash(message)
    payload=f"{hash}||{message}"

    msg_bytes = payload.encode('utf-8')
    key = _password_bytes(password)
    if not key:
        raise ValueError("Password cannot be empty.")
    out = bytearray(len(msg_bytes))
    for i, b in enumerate(msg_bytes):
        k = key[i % len(key)]
        out[i] = (b + k) % 256
    return bytes(out)

def vigenere_decrypt(cipher_text: str, password: str) -> str:
    cipher_bytes=cipher_text.encode('latin-1')
    key = _password_bytes(password)
    if not key:
        raise ValueError("Password cannot be empty.")
    out = bytearray(len(cipher_bytes))
    for i, b in enumerate(cipher_bytes):
        k = key[i % len(key)]
        out[i] = (b - k) % 256
    
    decrypted_payload=out.decode('latin-1')

    try:
        extracted_hash, original_message = decrypted_payload.split("||", 1)
    except ValueError:
        raise ValueError("Integrity Check Failed: Format Error")

    current_hash = getHash(original_message)
    
    if current_hash != extracted_hash:
        raise ValueError("Entered password is wrong.")
        
    return original_message

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

def bits_to_text(bits_str: str) -> str:
    chars = []
    for i in range(0, len(bits_str), 8):
        byte_str = bits_str[i:i+8]
        chars.append(chr(int(byte_str, 2)))
    return "".join(chars)