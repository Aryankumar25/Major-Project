from vehicle import Vehicle
from key import Key
from logger import log_event

def main():
    vehicle = Vehicle()
    key = Key()

    for i in range(6):  # Run multiple authentications to trigger key rotation
        print(f"\n🔐 Authentication Attempt {i+1}...")
        challenge = vehicle.generate_challenge()
        signed_response = key.sign_challenge(challenge)

        if vehicle.authenticate_key(challenge, signed_response):
            print("✅ Vehicle Unlocked!")
        else:
            print("❌ Access Denied!")

    print("\n🔄 Key Rotation should have happened after 5 successful authentications.")

if __name__ == "__main__":
    log_event("Starting Secure Vehicle Authentication System...")
    main()
