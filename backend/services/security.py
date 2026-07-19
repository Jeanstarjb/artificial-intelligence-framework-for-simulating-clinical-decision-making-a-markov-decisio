from fastapi import HTTPException, status
import hmac
import hashlib
import os

def verify_webhook_signature(payload_body: bytes, signature_header: str):
    secret = os.getenv('EHR_WEBHOOK_SECRET')
    if not secret:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Webhook secret not configured"
        )
    digest = hmac.new(secret.encode(), payload_body, hashlib.sha256).hexdigest()
    if not hmac.compare_digest(digest, signature_header):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid webhook signature"
        )