import secrets
from crypto_utils import ecc_manager
from logger import log_event
from config import NONCE_LENGTH

class Vehicle:
    def __init__(self):
        log_event("Vehicle system initialized.")

    def generate_challenge(self):
        """Generate a random nonce (challenge)."""
        nonce = secrets.token_hex(NONCE_LENGTH)
        log_event(f"Vehicle generated challenge: {nonce}")
        return nonce

    def authenticate_key(self, challenge, signed_response):
        """Verify the key's response using ECDSA."""
        if ecc_manager.verify_signature(challenge, signed_response):
            log_event("Authentication successful: Vehicle unlocked.")
            return True
        else:
            log_event("Authentication failed: Invalid key response.")
            return False
