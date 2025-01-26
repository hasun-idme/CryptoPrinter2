import json
from coinbase.rest import RESTClient

client = RESTClient() # Uses environment variables for API key and

api_key = "organizations/05d33b32-26e5-4d1c-9eb6-8851a921dc17/apiKeys/f8ce444a-cd59-40f5-9b5d-e93a20cc6c95"
api_secret = "-----BEGIN EC PRIVATE KEY-----\nMHcCAQEEIMRyXn0AVHJJg68Z/kVEGa1kHfKYqxQos1OLfIQ+yvWUoAoGCCqGSM49\nAwEHoUQDQgAEB3+6T/tXcpoCk5rTSIjJZ1J0sjua1MHKt4M85/X+NV5BzWPuY5uk\nI7rpkdl8WMkjDTzOuXYTFQzU+1+fTm4vaQ==\n-----END EC PRIVATE KEY-----\n"


client = RESTClient(api_key=api_key, api_secret=api_secret)

#printing all accounts in wallet
accounts = client.get_accounts()
#print(json.dumps(accounts.to_dict(), indent=2))

#printing market_trades
market_trades = client.get_market_trades(product_id="BTC-USD", limit=5)
print(json.dumps(market_trades.to_dict(), indent=2))
