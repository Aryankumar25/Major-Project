from vehicle import Vehicle
from key import Key
from logger import log_event

def main():
    vehicle = Vehicle()
    key = Key()

    print("\n🔹 Generating Challenge...")
    challenge = vehicle.generate_challenge()

    print("\n🔹 Key Signing Challenge...")
    signed_response = key.sign_challenge(challenge)

    print("\n🔹 Authenticating Key...")
    if vehicle.authenticate_key(challenge, signed_response):
        print("✅ Vehicle Unlocked!")
    else:
        print("❌ Access Denied!")

if __name__ == "__main__":
    log_event("Starting Secure Vehicle Authentication System...")
    main()
