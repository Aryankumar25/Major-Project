from vehicle import Vehicle
from key import Key
from logger import log_event
from performance import track_performance

def main():
    vehicle = Vehicle()
    key = Key()

    print("\nGenerating Challenge...")
    challenge, challenge_time = track_performance(vehicle.generate_challenge)

    print("\nKey Signing Challenge...")
    signed_response, sign_time = track_performance(lambda: key.sign_challenge(challenge))

    print("\nAuthenticating Key...")
    auth_result, auth_time = track_performance(lambda: vehicle.authenticate_key(challenge, signed_response))

    if auth_result:
        print("✅ Vehicle Unlocked!")
    else:
        print("❌ Access Denied!")

    log_event(f"Performance Metrics - Challenge: {challenge_time:.4f}s, Signing: {sign_time:.4f}s, Authentication: {auth_time:.4f}s")

if __name__ == "__main__":
    log_event("Starting Secure Vehicle Authentication System...")
    main()
