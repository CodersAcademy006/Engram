"""
Text Cleaning & PII Redaction Module
Senior feature: Removes sensitive information
"""

import re
from loguru import logger


class TextCleaner:
    """Handles text cleaning and PII redaction"""
    
    # PII patterns
    EMAIL_PATTERN = re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b')
    PHONE_PATTERN = re.compile(r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b')
    SSN_PATTERN = re.compile(r'\b\d{3}-\d{2}-\d{4}\b')
    CREDIT_CARD_PATTERN = re.compile(r'\b\d{4}[-\s]?\d{4}[-\s]?\d{4}[-\s]?\d{4}\b')
    
    def __init__(self):
        logger.info("Text cleaner initialized")
    
    def clean(self, text):
        """Basic text cleaning"""
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        # Remove special characters
        text = text.strip()
        return text
    
    def redact_pii(self, text):
        """Redact personally identifiable information"""
        text = self.EMAIL_PATTERN.sub('[EMAIL]', text)
        text = self.PHONE_PATTERN.sub('[PHONE]', text)
        text = self.SSN_PATTERN.sub('[SSN]', text)
        text = self.CREDIT_CARD_PATTERN.sub('[CREDIT_CARD]', text)
        return text
    
    def process(self, text, redact=True):
        """Complete text processing pipeline"""
        text = self.clean(text)
        if redact:
            text = self.redact_pii(text)
        return text
