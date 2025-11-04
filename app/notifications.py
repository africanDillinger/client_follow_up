# app/notifications.py
# Single place to implement real notification providers (Twilio / Africa's Talking).
# For now it's a placeholder that prints to console.

def send_notification(phone, message):
    # replace this implementation with a real provider integration.
    print(f"[Notification] To: {phone} | Message: {message}")
