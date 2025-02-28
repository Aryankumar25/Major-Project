from crypto_utils import ecc_manager
from logger import log_event

class Key:
    def __init__(self):
        log_event("🔑 Key system initialized.")

    def sign_challenge(self, challenge):
        """Sign the challenge using ECC."""
        signed_response = ecc_manager.sign_message(challenge)
        log_event(f"✍️ Key signed challenge: {signed_response}")
        return signed_response
