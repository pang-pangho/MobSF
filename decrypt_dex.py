import base64
import time
from Crypto import Random
from Crypto.Cipher import AES

# 패딩 관련 설정

BS = 16
pad = lambda s: s + (BS - len(s.encode('utf-8')) % BS) * chr(BS - len(s.encode('utf-8')) % BS)
unpad = lambda s: s[:-ord(s[len(s)-1:])]

# AES 암호화 클래스

class AESCipher:
    def __init__(self, key):
        self.key = key

    def encrypt(self, raw):
        raw = pad(raw)
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return base64.b64encode(iv + cipher.encrypt(raw.encode('utf-8')))

    def decrypt(self, enc):
        enc = base64.b64decode(enc)
        iv = enc[:16]
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return unpad(cipher.decrypt(enc[16:]).decode('utf-8'))

# 32바이트 키

key = bytes([
    0x10, 0x01, 0x15, 0x1B, 0xA1, 0x11, 0x57, 0x72,
    0x6C, 0x21, 0x56, 0x57, 0x62, 0x16, 0x05, 0x3D,
    0xFF, 0xFE, 0x11, 0x1B, 0x21, 0x31, 0x57, 0x72,
    0x6B, 0x21, 0xA6, 0xA7, 0x6E, 0xE6, 0xE5, 0x3F
])

cipher = AESCipher(key)

# 1. 파일에서 읽기

original_file = "original.dex"
with open(original_file, "rb") as f:
    original_data = f.read().decode('utf-8', errors='ignore')

# 2. 암호화

encrypted_data = cipher.encrypt(original_data)
print(" Encrypted:\n", encrypted_data)

# 3. 복호화

decrypted_data = cipher.decrypt(encrypted_data)
print("\n Decrypted:\n", decrypted_data)

# 4. 복호화 결과 저장 (선택)

with open("decrypted_output.txt", "w", encoding="utf-8") as f:
    f.write(decrypted_data)
