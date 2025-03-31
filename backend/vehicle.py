import secrets
from crypto_utils import ecc_manager
from logger import log_event
from config import NONCE_LENGTH

class Vehicle:
    def __init__(self, vehicle_id):
        self.vehicle_id = vehicle_id
        log_event(f"Vehicle {vehicle_id} initialized.")

    def generate_challenge(self):
        """Generate a random nonce (challenge)."""
        nonce = secrets.token_hex(NONCE_LENGTH)
        log_event(f"Vehicle {self.vehicle_id} generated challenge: {nonce}")
        return nonce

    def authenticate_key(self, challenge, signed_response):
        """Verify the key's response using ECDSA."""
        if ecc_manager.verify_signature(challenge, signed_response, self.vehicle_id):
            log_event(f"Authentication successful: Vehicle {self.vehicle_id} unlocked.")
            return True
        else:
            log_event(f"Authentication failed: Vehicle {self.vehicle_id} denied access.")
            return False
