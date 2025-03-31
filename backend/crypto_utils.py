import ecdsa
import os
import base64
import time  # ✅ Added for performance measurement
from config import KEYS_DIR

class ECCManager:
    def __init__(self):
        os.makedirs(KEYS_DIR, exist_ok=True)

    def get_key_files(self, vehicle_id):
        """Returns file paths for a specific vehicle's ECC keys."""
        return (
            os.path.join(KEYS_DIR, f"{vehicle_id}_private.pem"),
            os.path.join(KEYS_DIR, f"{vehicle_id}_public.pem")
        )

    def generate_keys(self, vehicle_id):
        """Generate and save a new ECC key pair for a vehicle."""
        private_key_file, public_key_file = self.get_key_files(vehicle_id)

        if os.path.exists(private_key_file) and os.path.exists(public_key_file):
            return  # Keys already exist

        start_time = time.time()  # ✅ Start timing

        private_key = ecdsa.SigningKey.generate(curve=ecdsa.NIST256p)
        public_key = private_key.get_verifying_key()

        with open(private_key_file, "wb") as f:
            f.write(private_key.to_pem())

        with open(public_key_file, "wb") as f:
            f.write(public_key.to_pem())

        key_gen_time = time.time() - start_time  # ✅ Calculate execution time
        print(f"✅ New ECC key pair generated for {vehicle_id} in {key_gen_time:.6f} seconds.")

    def load_private_key(self, vehicle_id):
        """Load ECC private key for a specific vehicle."""
        private_key_file, _ = self.get_key_files(vehicle_id)
        with open(private_key_file, "rb") as f:
            return ecdsa.SigningKey.from_pem(f.read())

    def load_public_key(self, vehicle_id):
        """Load ECC public key for a specific vehicle."""
        _, public_key_file = self.get_key_files(vehicle_id)
        with open(public_key_file, "rb") as f:
            return ecdsa.VerifyingKey.from_pem(f.read())

    def sign_message(self, message, vehicle_id):
        """Sign a message using ECC private key and measure signing time."""
        private_key = self.load_private_key(vehicle_id)

        start_time = time.time()  # ✅ Start timing
        signature = private_key.sign(message.encode())
        signing_time = time.time() - start_time  # ✅ Calculate execution time

        print(f"⏳ Signing Time: {signing_time:.6f} seconds")
        return base64.b64encode(signature).decode()

    def verify_signature(self, message, signature, vehicle_id):
        """Verify message signature using ECC public key and measure verification time."""
        try:
            public_key = self.load_public_key(vehicle_id)
            decoded_signature = base64.b64decode(signature)

            start_time = time.time()  # ✅ Start timing
            is_valid = public_key.verify(decoded_signature, message.encode())
            verification_time = time.time() - start_time  # ✅ Calculate execution time

            print(f"⏳ Verification Time: {verification_time:.6f} seconds")
            return is_valid

        except ecdsa.BadSignatureError:
            return False

# Initialize ECC Manager
ecc_manager = ECCManager()
