import ecdsa
import os
import base64
import shutil
import time
from config import (
    ECC_PRIVATE_KEY_FILE, ECC_PUBLIC_KEY_FILE, GENERATE_NEW_KEYS, 
    NONCE_LENGTH, ROTATION_INTERVAL, LAST_ROTATION_FILE
)
from logger import log_event

class ECCManager:
    def __init__(self):
        os.makedirs("old_keys", exist_ok=True)  # Ensure old_keys folder exists

        if GENERATE_NEW_KEYS:
            self.generate_keys()
            self.update_last_rotation_time()

        self.private_key = self.load_private_key()
        self.public_key = self.load_public_key()

    def generate_keys(self):
        """Generate and save a new ECC key pair."""
        private_key = ecdsa.SigningKey.generate(curve=ecdsa.NIST256p)
        public_key = private_key.get_verifying_key()

        self.backup_old_keys()  # Backup current keys before replacing

        with open(ECC_PRIVATE_KEY_FILE, "wb") as f:
            f.write(private_key.to_pem())

        with open(ECC_PUBLIC_KEY_FILE, "wb") as f:
            f.write(public_key.to_pem())

        log_event("🔄 New ECC key pair generated!")

    def load_private_key(self):
        """Load ECC private key from file."""
        with open(ECC_PRIVATE_KEY_FILE, "rb") as f:
            return ecdsa.SigningKey.from_pem(f.read())

    def load_public_key(self):
        """Load ECC public key from file."""
        with open(ECC_PUBLIC_KEY_FILE, "rb") as f:
            return ecdsa.VerifyingKey.from_pem(f.read())

    def sign_message(self, message):
        """Sign a message using ECC private key."""
        signature = self.private_key.sign(message.encode())
        return base64.b64encode(signature).decode()

    def verify_signature(self, message, signature):
        """Verify message signature using ECC public key."""
        try:
            decoded_signature = base64.b64decode(signature)
            return self.public_key.verify(decoded_signature, message.encode())
        except ecdsa.BadSignatureError:
            return self.verify_old_keys(message, signature)

    def verify_old_keys(self, message, signature):
        """Check old public keys for validity."""
        for old_key in os.listdir("old_keys"):
            try:
                with open(os.path.join("old_keys", old_key), "rb") as f:
                    old_public_key = ecdsa.VerifyingKey.from_pem(f.read())
                if old_public_key.verify(base64.b64decode(signature), message.encode()):
                    return True
            except ecdsa.BadSignatureError:
                continue
        return False

    def rotate_keys(self):
        """Rotate ECC keys if necessary."""
        if self.should_rotate():
            log_event("🔄 Rotating ECC keys...")
            self.generate_keys()
            self.private_key = self.load_private_key()
            self.public_key = self.load_public_key()
            self.update_last_rotation_time()
            log_event("✅ Key rotation complete.")
        else:
            log_event("⏳ No rotation needed yet.")

    def should_rotate(self):
        """Check if keys should rotate based on time interval."""
        try:
            with open(LAST_ROTATION_FILE, "r") as f:
                last_rotation_time = float(f.read().strip())
        except (FileNotFoundError, ValueError):
            return True  # Rotate if the file doesn't exist

        elapsed_time = time.time() - last_rotation_time
        return elapsed_time >= ROTATION_INTERVAL

    def update_last_rotation_time(self):
        """Update the last rotation time file."""
        with open(LAST_ROTATION_FILE, "w") as f:
            f.write(str(time.time()))

    def backup_old_keys(self):
        """Move old keys to an archive before rotation."""
        if os.path.exists(ECC_PUBLIC_KEY_FILE):
            shutil.move(ECC_PUBLIC_KEY_FILE, f"old_keys/public_key_{os.path.getmtime(ECC_PUBLIC_KEY_FILE)}.pem")
        if os.path.exists(ECC_PRIVATE_KEY_FILE):
            shutil.move(ECC_PRIVATE_KEY_FILE, f"old_keys/private_key_{os.path.getmtime(ECC_PRIVATE_KEY_FILE)}.pem")

# Initialize ECC Manager
ecc_manager = ECCManager()
