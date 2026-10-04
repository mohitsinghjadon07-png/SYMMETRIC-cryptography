# ⛏️ Symmetric Cryptography Lab — Minecraft Edition

A **Minecraft-themed interactive cryptography web application** designed to demonstrate symmetric encryption and classical cipher algorithms in a simple, visual, and beginner-friendly way.

The project combines **AES-256-ECB encryption** with classical cryptography algorithms such as **Caesar Cipher, ROT13, Atbash, and Rail Fence**.

---

## 🎮 Project Overview

This project was developed as an educational implementation of **Symmetric Cryptography**.

The application allows users to:

* Generate a 256-bit secret key
* Encrypt and decrypt text
* Encrypt and decrypt files
* Explore classical substitution and transposition ciphers
* Visualize the Rail Fence cipher using a zig-zag pattern
* Understand how encryption transforms plaintext into ciphertext
* Experiment with different cryptographic techniques through an interactive Minecraft-inspired interface

---

## ✨ Features

### 🔐 AES-256-ECB

The main encryption module uses:

* AES (Advanced Encryption Standard)
* 256-bit secret key
* ECB (Electronic Codebook) mode
* PKCS#7 padding
* Base64 representation for encrypted text

Users can:

**Plaintext → Encrypt → Ciphertext**

and:

**Ciphertext → Decrypt → Original Plaintext**

---

### 🔑 Secret Key Generator

The application can automatically generate a secure **256-bit random key**.

The key can also be copied and shared with the intended recipient.

The same secret key is required for decryption.

---

### 📝 Text Encryption

Users can enter any text and encrypt it using the generated AES-256 key.

Example:

```text
Hello World
```

After encryption:

```text
Base64 Encoded Ciphertext
```

The ciphertext can then be decrypted using the correct key.

---

### 📁 File Encryption

The application also supports file encryption.

Supported workflow:

```text
Select File
      ↓
AES-256 Encryption
      ↓
Encrypted .enc File
```

The encrypted file can later be decrypted using the same secret key.

---

# 🧩 Classical Cipher Algorithms

The project also contains an interactive algorithm laboratory.

## 1. Caesar Cipher — Shift

The Caesar Cipher shifts every letter by a fixed number of positions.

Example with shift `3`:

```text
A → D
B → E
C → F
```

Example:

```text
HELLO
```

becomes:

```text
KHOOR
```

---

## 2. ROT13

ROT13 is a special Caesar Cipher that uses a shift of **13 positions**.

Example:

```text
HELLO
```

becomes:

```text
URYYB
```

The transformation is reversible because applying ROT13 twice returns the original text.

---

## 3. Atbash Cipher

Atbash reverses the alphabet.

```text
ABCDEFGHIJKLMNOPQRSTUVWXYZ
↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓
ZYXWVUTSRQPONMLKJIHGFEDCBA
```

Example:

```text
HELLO
```

becomes:

```text
SVOOL
```

---

## 4. Rail Fence Cipher

Rail Fence is a **transposition cipher** that arranges characters in a zig-zag pattern across multiple rails.

Example:

```text
W . . . E . . . C
. E . R . D . F .
. . A . . . L . .
```

The characters are then read row-by-row to produce the ciphertext.

The application provides a visual **zig-zag Rail Fence representation** so that the transformation can be understood easily.

---

# 🎮 Minecraft-Themed Interface

The application uses a Minecraft-inspired interface featuring:

* Dark pixel-style interface
* Stone-inspired panels
* Grass-themed buttons
* Pixel-style typography
* Minecraft-inspired colors
* Scrollable layout
* Interactive algorithm panels

The theme is designed to make a technical cryptography project more engaging and visually understandable.

---

# 🛠️ Technologies Used

| Technology   | Purpose                             |
| ------------ | ----------------------------------- |
| Python       | Core programming                    |
| PyCryptodome | AES cryptographic implementation    |
| Base64       | Ciphertext/key representation       |
| HTML/CSS     | Web styling                         |
| GitHub       | Version control and project hosting |

---

# 📂 Project Structure

```text
Symmetric_Cryptography_AES_Project/
│
├── app.py
├── requirements.txt
└── README.md
```

---

# ⚙️ Installation

Clone the repository:

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
```

Move into the project directory:

```bash
cd Symmetric_Cryptography_AES_Project
```

Install the required dependencies:

```bash
python -m pip install -r requirements.txt
```

---



# 🔒 Security Note

This project is primarily intended for **educational purposes**.

AES-256-ECB is implemented because the project focuses on demonstrating symmetric cryptography and block cipher operation.

However, **ECB mode is not recommended for real-world secure communication** because identical plaintext blocks can produce identical ciphertext blocks, which can reveal patterns.

For production applications, an authenticated encryption mode such as **AES-GCM** is generally preferable.

Never share a secret encryption key with unauthorized users.

---

# 🎯 Learning Objectives

This project demonstrates:

* What symmetric cryptography is
* How secret-key encryption works
* AES-256 encryption
* Block cipher concepts
* ECB mode
* PKCS#7 padding
* Base64 encoding
* Classical substitution ciphers
* Classical transposition ciphers
* Caesar Cipher
* ROT13
* Atbash
* Rail Fence Cipher
* Text encryption and decryption
* File encryption and decryption
* Basic cryptographic key management
* Web-based cryptography application development

---


# 👨‍💻 Project

**Project:** Symmetric Cryptography Implementation

**Theme:** Minecraft Edition

**Main Technology:** Python 

**Cryptographic Library:** PyCryptodome

---

## ⚠️ Disclaimer

This project is created for **academic and educational demonstration purposes**. It should not be considered a complete production-grade secure communication system.

Use appropriate modern authenticated encryption and secure key-management practices for real-world applications.
