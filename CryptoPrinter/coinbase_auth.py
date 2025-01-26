import requests
import json
import time
import os
from hashlib import sha256
from ecdsa import SigningKey, SECP256k1
from dotenv import load_dotenv
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import ec
load_dotenv()  # Load variables from .env file

def convert_pem_to_hex(pem_key):
    """
    Convert PEM-encoded EC private key to hexadecimal format.
    """
    try:
        private_key = serialization.load_pem_private_key(
            pem_key.encode("utf-8"),
            password=None
        )
        raw_key = private_key.private_numbers().private_value
        hex_key = f"{raw_key:064x}"  # Format as a 64-character hexadecimal string
        return hex_key
    except Exception as e:
        raise ValueError(f"Error converting PEM to hex: {e}")

# Example PEM key
pem_key = "-----BEGIN EC PRIVATE KEY-----\nMHcCAQEEIMRyXn0AVHJJg68Z/kVEGa1kHfKYqxQos1OLfIQ+yvWUoAoGCCqGSM49\nAwEHoUQDQgAEB3+6T/tXcpoCk5rTSIjJZ1J0sjua1MHKt4M85/X+NV5BzWPuY5uk\nI7rpkdl8WMkjDTzOuXYTFQzU+1+fTm4vaQ==\n-----END EC PRIVATE KEY-----\n"

# Convert the PEM key to hexadecimal
PRIVATE_KEY_HEX = convert_pem_to_hex(pem_key)
WALLET_NAME = os.getenv("COINBASE_WALLET_NAME")
#PRIVATE_KEY = os.getenv("COINBASE_PRIVATE_KEY") LATER
print(f"wallet_name: {WALLET_NAME}")
print(f"private_key: {PRIVATE_KEY_HEX}")

BASE_URL = "https://api.coinbase.com"  # Adjust if using a different endpoint

def generate_signature(private_key, message):
    """
    Generate an ECDSA signature using the private key.
    """
    try:
        signing_key = SigningKey.from_string(bytes.fromhex(private_key), curve=SECP256k1)
        signature = signing_key.sign(message.encode("utf-8"))
        return signature.hex()
    except Exception as e:
        raise ValueError(f"Error generating signature: {e}")

def authenticate_wallet():
    """
    Authenticate to Coinbase Wallet API using ECDSA signature.
    """
    try:
        # Prepare the request data
        timestamp = str(int(time.time()))
        endpoint = "/v2/user"  # Check if this is the correct endpoint
        message = f"{timestamp}{WALLET_NAME}{endpoint}"
        print(f"Message to sign: {message}")

        # Generate the signature
        signature = generate_signature(PRIVATE_KEY_HEX, message)
        print(f"Generated signature: {signature}")

        # Define headers
        headers = {
            "CB-ACCESS-KEY": WALLET_NAME,
            "CB-ACCESS-SIGN": signature,
            "CB-ACCESS-TIMESTAMP": timestamp,
            "Content-Type": "application/json",
        }
        print(f"Headers: {headers}")

        # Send the request
        url = f"{BASE_URL}{endpoint}"
        print(f"Sending request to: {url}")
        response = requests.get(url, headers=headers)

        # Debug the raw response
        print(f"Status code: {response.status_code}")
        print(f"Raw response: {response.text}")

        # Handle the response
        if response.status_code == 200:
            print("Authentication successful!")
            print("Response:", response.json())
        else:
            print(f"Authentication failed with status code {response.status_code}")
            try:
                print("Parsed JSON response:", response.json())
            except ValueError as e:
                print(f"Failed to parse response as JSON: {e}")
                print("Raw response:", response.text)

    except Exception as e:
        print(f"An error occurred during authentication: {e}")

if __name__ == "__main__":
    authenticate_wallet()
