"""
Plugs Payments Signals
"""

from django.dispatch import Signal

# sent when a validated ifthen payment received
valid_ifthen_payment_received = Signal()

# sent when an invalid payment received
# could be an error with a reference, value or entity
# cannot be the anti phishing key
invalid_ifthen_payment_received = Signal()

# sent when a request to the confirmation callback
# was made with an incorrect or missing anti phisphing key
suspicious_ifthen_payment_received = Signal()

