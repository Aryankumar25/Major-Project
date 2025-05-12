from crypto_utils import ecc_manager
from logger import log_event

class KeyFob:
    def __init__(self, vehicle_id):
        self.vehicle_id = vehicle_id
        log_event(f"KeyFob initialized for Vehicle {vehicle_id}.")

    def sign_challenge(self, challenge):
        """Sign the challenge using the key fob's private key for the selected vehicle."""
        signed_response = ecc_manager.sign_message(challenge, self.vehicle_id)
        log_event(f"KeyFob signed challenge for Vehicle {self.vehicle_id}: {signed_response}")
        return signed_response