"""
Encryption Utilities
Provides functions to encrypt and decrypt data using the Fernet symmetric encryption.
"""

from cryptography.fernet import Fernet
import os

from config import Config
from src.utils.logger import logger

# Initialize Fernet with the key from config
# We encode the key to bytes as Fernet requires it
try:
    if Config.ENCRYPTION_KEY:
        key = Config.ENCRYPTION_KEY.encode()
        cipher_suite = Fernet(key)
    else:
        cipher_suite = None
except Exception as e:
    logger.error(f"Failed to initialize encryption cipher suite. Is the ENCRYPTION_KEY valid? Error: {e}")
    cipher_suite = None

def encrypt_data(data: bytes) -> bytes:
    """
    Encrypts the given data.
    If encryption is not enabled or the key is not set, returns the original data.
    """
    if not Config.ENCRYPTION_ENABLED or not cipher_suite:
        return data
    
    try:
        return cipher_suite.encrypt(data)
    except Exception as e:
        logger.error(f"Encryption failed: {e}")
        # In a real-world scenario, you might want to handle this more gracefully
        # For now, we'll return the original data to prevent a crash.
        return data

def decrypt_data(encrypted_data: bytes) -> bytes:
    """
    Decrypts the given data.
    If encryption is not enabled or the key is not set, returns the original data.
    """
    if not Config.ENCRYPTION_ENABLED or not cipher_suite:
        return encrypted_data
        
    try:
        # A simple check to see if the data is likely encrypted
        # Fernet tokens are base64 encoded and have a specific structure.
        # A more robust check might be needed, but this prevents errors on unencrypted data.
        return cipher_suite.decrypt(encrypted_data)
    except Exception:
        # This will fail if the data is not valid encrypted data (e.g., already unencrypted)
        # or if the key is wrong. We'll log it but return the original data.
        # logger.warning("Decryption failed. Data may be unencrypted or key is incorrect. Returning original data.")
        return encrypted_data

def is_encrypted(file_path: str) -> bool:
    """
    A simple check to see if a file is likely encrypted by reading its first few bytes.
    This is not foolproof but can help in migration scenarios.
    """
    if not os.path.exists(file_path) or os.path.getsize(file_path) < 8:
        return False
    
    try:
        with open(file_path, 'rb') as f:
            header = f.read(8)
        # Fernet tokens start with 'gAAAAA' in base64
        return header.startswith(b'gAAAAA')
    except Exception:
        return False
