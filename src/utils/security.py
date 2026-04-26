"""
Security Module
Encryption and decryption for local files
"""

from cryptography.fernet import Fernet
from pathlib import Path
from loguru import logger

from config import Config


class Security:
    """Handles encryption and decryption of local files"""
    
    def __init__(self):
        self.enabled = Config.ENCRYPTION_ENABLED
        self.key = self._load_or_generate_key()
        if self.enabled:
            self.cipher = Fernet(self.key)
        logger.info(f"Security initialized (encryption: {self.enabled})")
    
    def _load_or_generate_key(self):
        """Load existing key or generate new one"""
        if Config.ENCRYPTION_KEY:
            return Config.ENCRYPTION_KEY.encode()
        else:
            # Generate new key
            key = Fernet.generate_key()
            logger.warning("Generated new encryption key. Save this to .env!")
            logger.warning(f"ENCRYPTION_KEY={key.decode()}")
            return key
    
    def encrypt_file(self, file_path):
        """Encrypt a file"""
        if not self.enabled:
            return file_path
        
        try:
            with open(file_path, 'rb') as f:
                data = f.read()
            
            encrypted_data = self.cipher.encrypt(data)
            
            encrypted_path = Path(str(file_path) + '.encrypted')
            with open(encrypted_path, 'wb') as f:
                f.write(encrypted_data)
            
            # Remove original file
            Path(file_path).unlink()
            
            logger.info(f"Encrypted: {file_path}")
            return encrypted_path
            
        except Exception as e:
            logger.error(f"Encryption error: {e}")
            return file_path
    
    def decrypt_file(self, file_path):
        """Decrypt a file"""
        if not self.enabled:
            return file_path
        
        try:
            with open(file_path, 'rb') as f:
                encrypted_data = f.read()
            
            decrypted_data = self.cipher.decrypt(encrypted_data)
            
            # Remove .encrypted extension
            decrypted_path = Path(str(file_path).replace('.encrypted', ''))
            with open(decrypted_path, 'wb') as f:
                f.write(decrypted_data)
            
            logger.info(f"Decrypted: {file_path}")
            return decrypted_path
            
        except Exception as e:
            logger.error(f"Decryption error: {e}")
            return None
    
    def encrypt_text(self, text):
        """Encrypt text string"""
        if not self.enabled:
            return text
        
        encrypted = self.cipher.encrypt(text.encode())
        return encrypted.decode()
    
    def decrypt_text(self, encrypted_text):
        """Decrypt text string"""
        if not self.enabled:
            return encrypted_text
        
        decrypted = self.cipher.decrypt(encrypted_text.encode())
        return decrypted.decode()
