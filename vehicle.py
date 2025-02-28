import secrets
from crypto_utils import ecc_manager
from logger import log_event
from config import NONCE_LENGTH

class Vehicle:
    def __init__(self):
        self.auth_count = 0
        log_event("🚗 Vehicle system initialized.")

    def generate_challenge(self):
        """Generate a random nonce (challenge)."""
        nonce = secrets.token_hex(NONCE_LENGTH)
        log_event(f"🔄 Vehicle generated challenge: {nonce}")
        return nonce

    def authenticate_key(self, challenge, signed_response):
        """Verify key response and check for key rotation."""
        if ecc_manager.verify_signature(challenge, signed_response):
            log_event("✅ Authentication successful: Vehicle unlocked.")
            self.auth_count += 1

            # Rotate keys after 5 authentications OR if time interval reached
            if self.auth_count >= 5 or ecc_manager.should_rotate():
                ecc_manager.rotate_keys()
                self.auth_count = 0  # Reset counter after rotation

            return True
        else:
            log_event("❌ Authentication failed: Invalid key response.")
            return False
