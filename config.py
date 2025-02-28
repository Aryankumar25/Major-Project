import os

# ECC Key Paths
ECC_PRIVATE_KEY_FILE = "key_private.pem"
ECC_PUBLIC_KEY_FILE = "key_public.pem"

# Replay Attack Protection
NONCE_LENGTH = 16  # 16-byte random nonce

# Log file
LOG_FILE = "security_system.log"

# Generate fresh keys if not found
GENERATE_NEW_KEYS = not (os.path.exists(ECC_PRIVATE_KEY_FILE) and os.path.exists(ECC_PUBLIC_KEY_FILE))

# Key Rotation Settings
ROTATION_INTERVAL = 24 * 60 * 60  # Rotate every 24 hours (86400 seconds)
LAST_ROTATION_FILE = "last_rotation.txt"
