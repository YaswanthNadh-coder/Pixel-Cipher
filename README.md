
# Pixel-Cipher

**Team Name:** PyBash

**Author:** Pragyan Ojha 

###  Short Description
Pixel-Cipher is a secure image steganography tool built from scratch in Python. It allows users to hide secret text messages inside images. It uses a **password-seeded random distribution** method. This means the message bits are scattered randomly across the image, making them nearly impossible to find without the correct password.

---

###  Concepts & Libraries Used

#### **Core Concepts**
1.  **LSB Steganography (Least Significant Bit):** We modify the last bit of the Red color channel of specific pixels to store our data. This change is so small that the human eye cannot see the difference.
2.  **Symmetric Encryption (Vigenère Cipher):** Before hiding the message, we encrypt it using a custom Vigenère cipher implementation. This adds a second layer of security.
3.  **Pseudo-Random Number Generation (PRNG):** We use the user's password to "seed" the random number generator. This allows us to generate a unique, reproducible pattern of pixel coordinates to hide the data in.
4.  **Data Integrity :** We calculate a simple ASCII sum of the message before encrypting. We use this to verify if the password entered is correct during decryption.

#### **Libraries**
* **`Pillow` (PIL):** Used for opening images, reading pixel data (`load()`), and saving the final output.
* **`random`:** Used to generate the seeded list of random coordinates.
* **`os`:** Used to check if image files exist before processing.

---

###  Module & Function Explanation

#### 1. `main.py` 
This is the entry point of the application. It provides an interactive menu for the user.
* **Functionality:** Handles user inputs (file paths, passwords, messages) and calls the appropriate functions from the engine.
* **Features:** Auto-detects file extensions and prevents overwriting errors.

#### 2. `crypto.py` 
Handles all encryption and binary conversions.
* **`vigenere_encrypt(message, password)`**: Calculates a hash, attaches it to the message, and encrypts the text bytes using the Vigenere algorithm.
* **`vigenere_decrypt(cipher_text, password)`**: Decrypts the text and verifies the hash. If the checksum fails (due to a wrong password), it raises an error.
* **`text_to_bits(data)` / `bits_to_text(bits)`**: Helper functions that convert text characters into lists of 1s and 0s (binary) and vice versa.

#### 3. `stego.py` 
Handles the image manipulation.
* **`encode(image, message, password)`**:
    1.  Encrypts the message and converts it to bits.
    2.  Hides the **length** of the message in the first 32 pixels.
    3.  Seeds the random generator with the password to pick random pixel coordinates.
    4.  Embeds the message bits into the red channel of the pixel.
* **`decode(image, password)`**:
    1.  Reads the first 32 pixels to find out how long the hidden message is.
    2.  Re-seeds the random generator to find the exact same "random" pixels used during encoding.
    3.  Extracts the bits, converts them to text, and decrypts the message.

---

###  Example Input / Output

1.  **Input:**
    * **Image:** `test.png` (A normal picture of a landscape)
    * **Message:** "Meet me at midnight"
    * **Password:** "secret123"
    * **Output Name:** `hidden.png`

2.  **Process:**
    * The tool encrypts "Meet me at midnight" using **`vigenere_encrypt`**.
    * The encrypted message is then converted to bits using **`text_to_bits`**.
    * It selects required number of random pixels scattered across the image and hides each bit into the LSB of red value of the selected pixels by making them 0 or 1 accordingly.
    * The decoding process is exactly the opposite of this.


3.  **Output:**
    * `hidden.png` is created in the same directory. It looks identical to `test.png` to the naked eye.

---

###  Setup Instructions

Follow these steps to run the project on your local machine.

1. Make sure python is installed by running:
```bash
python3 --version
```
2. Install the pillow library:
```bash
pip install Pillow
```
3. In the same directory as the project folder, run:
```bash
python3 src/main.py
```



