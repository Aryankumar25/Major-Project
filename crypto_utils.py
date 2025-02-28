import ecdsa
import os
import base64
from config import ECC_PRIVATE_KEY_FILE, ECC_PUBLIC_KEY_FILE, GENERATE_NEW_KEYS

class ECCManager:
    def __init__(self):
        if GENERATE_NEW_KEYS:
            self.generate_keys()

        self.private_key = self.load_private_key()
        self.public_key = self.load_public_key()

    def generate_keys(self):
        """Generate and save a new ECC key pair."""
        private_key = ecdsa.SigningKey.generate(curve=ecdsa.NIST256p)
        public_key = private_key.get_verifying_key()

        with open(ECC_PRIVATE_KEY_FILE, "wb") as f:
            f.write(private_key.to_pem())

        with open(ECC_PUBLIC_KEY_FILE, "wb") as f:
            f.write(public_key.to_pem())

        print("✅ New ECC key pair generated!")

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
            return False

# Initialize ECC Manager
ecc_manager = ECCManager()
