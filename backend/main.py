import argparse
import time  # ✅ Added for performance tracking
from vehicle import Vehicle
from keyfob import KeyFob
from logger import log_event
from crypto_utils import ecc_manager

def authenticate_vehicle(vehicle_id):
    vehicle = Vehicle(vehicle_id)
    key_fob = KeyFob(vehicle_id)

    print(f"\nTesting Vehicle {vehicle_id}...")

    start_time = time.time()  # ✅ Start measuring authentication process

    challenge = vehicle.generate_challenge()
    signed_response = key_fob.sign_challenge(challenge)

    if vehicle.authenticate_key(challenge, signed_response):
        auth_time = time.time() - start_time  # ✅ Calculate total authentication time
        print(f"Vehicle {vehicle_id} authenticated successfully!")
        print(f"Authentication Time: {auth_time:.6f} seconds")
    else:
        print(f"Vehicle {vehicle_id} authentication failed.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Vehicle Authentication System")
    parser.add_argument("--vehicle", type=str, help="Specify vehicle ID for authentication (e.g., V001)")
    parser.add_argument("--generate-keys", type=str, help="Generate ECC keys for vehicle ID")

    args = parser.parse_args()

    # Handle generate keys
    if args.generate_keys:
        ecc_manager.generate_keys(args.generate_keys)
        print(f"ECC keys generated for vehicle {args.generate_keys}")
        exit(0)

    # Handle vehicle authentication
    if args.vehicle:
        authenticate_vehicle(args.vehicle)
    else:
        vehicle_id = input("\nEnter vehicle ID for authentication: ").strip()
        authenticate_vehicle(vehicle_id)
