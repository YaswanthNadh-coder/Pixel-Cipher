def get_hash(message):
    #Calculates a simple sum of ASCII values of characters in the message
    total = 0
    for char in message:
        total += ord(char)
    return str(total)

def vigenere_encrypt(message, password):
    hash = get_hash(message)
    combined_text = hash + "||" + message

    msg_bytes = combined_text.encode('utf-8')
    key_bytes = password.encode('utf-8')
    
    if not password:
        raise ValueError("Password cannot be empty.")

    encrypted_out = bytearray(len(msg_bytes))
    key_len = len(key_bytes)
    
    for i in range(len(msg_bytes)):
        msg_val = msg_bytes[i]
        key_val = key_bytes[i % key_len]
    
        encrypted_out[i] = (msg_val + key_val) % 256
        
    return bytes(encrypted_out)

def vigenere_decrypt(cipher_text, password):
    cipher_bytes = cipher_text.encode('latin-1')
    key_bytes = password.encode('utf-8')
    
    if not password:
        raise ValueError("Password cannot be empty.")
        
    decrypted_out = bytearray(len(cipher_bytes))
    key_len = len(key_bytes)

    for i in range(len(cipher_bytes)):
        cipher_val = cipher_bytes[i]
        key_val = key_bytes[i % key_len]
        
        decrypted_out[i] = (cipher_val - key_val) % 256
    
    try:
        decrypted_str = decrypted_out.decode('utf-8')
    except UnicodeDecodeError:
        raise ValueError("Entered password is wrong.")

    try:
        extracted_hash, original_message = decrypted_str.split("||", 1)
    except ValueError:
        raise ValueError("Integrity Check Failed: Format Error")

    current_hash = get_hash(original_message)
    
    if current_hash != extracted_hash:
        raise ValueError("Entered password is wrong.")
        
    return original_message

def text_to_bits(data):
    bits = []
    for byte in data:
        for i in range(8):
            val = (byte >> (7 - i)) & 1
            bits.append(val)
    return bits

def bits_to_text(bits_string):
    chars = []
    for i in range(0, len(bits_string), 8):
        byte_chunk = bits_string[i:i+8]
        
        int_val = int(byte_chunk, 2)
        
        chars.append(chr(int_val))
        
    return "".join(chars)