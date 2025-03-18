import secrets
from crypto_utils import ecc_manager
from logger import log_event
from config import NONCE_LENGTH, KEY_ROTATION_INTERVAL
import time

class Vehicle:
    def __init__(self):
        self.last_key_rotation = time.time()
        log_event("Vehicle system initialized.")

    def generate_challenge(self):
        """Generate a random nonce (challenge)."""
        self.check_key_rotation()
        nonce = secrets.token_hex(NONCE_LENGTH)
        log_event(f"Vehicle generated challenge: {nonce}")
        return nonce

    def authenticate_key(self, challenge, signed_response):
        """Verify the key's response using ECDSA."""
        self.check_key_rotation()
        if ecc_manager.verify_signature(challenge, signed_response):
            log_event("Authentication successful: Vehicle unlocked.")
            return True
        else:
            log_event("Authentication failed: Invalid key response.")
            return False

    def check_key_rotation(self):
        """Rotate keys if the defined interval has passed."""
        if time.time() - self.last_key_rotation > KEY_ROTATION_INTERVAL:
            ecc_manager.generate_keys()
            self.last_key_rotation = time.time()
            log_event("🔄 Keys rotated due to timeout.")
