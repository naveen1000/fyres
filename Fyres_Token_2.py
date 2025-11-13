# Import the required module from the fyers_apiv3 package
from fyers_apiv3 import fyersModel

# Replace these values with your actual API credentials
client_id = "DUDIBC46PY-100"
secret_key = "AKFYIB3Q54"
redirect_uri = "http://127.0.0.1:5000/"
response_type = "code"  
state = "sample_state"

# Create a session model with the provided credentials
session = fyersModel.SessionModel(
    client_id=client_id,
    secret_key=secret_key,
    redirect_uri=redirect_uri,
    response_type=response_type
)

# Generate the auth code using the session model
response = session.generate_authcode()

# Print the auth code received in the response
print(response)

'''
# Import the required module from the fyers_apiv3 package
from fyers_apiv3 import fyersModel

# Define your Fyers API credentials
client_id = "DUDIBC46PY-100"  # Replace with your client ID
secret_key = "AKFYIB3Q54"  # Replace with your secret key
redirect_uri = "http://127.0.0.1:5000"  # Replace with your redirect URI
response_type = "code" 
grant_type = "authorization_code"  

# The authorization code received from Fyers after the user grants access
auth_code = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhcHBfaWQiOiJEVURJQkM0NlBZIiwidXVpZCI6ImU3ODc3NTZlNjY1NDRiOTQ5MWEyYTBkOWE5MThmNTcwIiwiaXBBZGRyIjoiIiwibm9uY2UiOiIiLCJzY29wZSI6IiIsImRpc3BsYXlfbmFtZSI6IllTNTQ3MDQiLCJvbXMiOiJLMSIsImhzbV9rZXkiOiIwYTc4YTAyNzUxNzY0MzhmZTBhYjM1NjgzMTI2NmMyNjZlYzZiZmVlYWYwYTczOWNiNmQ3ZmI2OCIsImlzRGRwaUVuYWJsZWQiOiJZIiwiaXNNdGZFbmFibGVkIjoiTiIsImF1ZCI6IltcImQ6MVwiLFwiZDoyXCIsXCJ4OjBcIixcIng6MVwiLFwieDoyXCJdIiwiZXhwIjoxNzYyOTc2NDM2LCJpYXQiOjE3NjI5NDY0MzYsImlzcyI6ImFwaS5sb2dpbi5meWVycy5pbiIsIm5iZiI6MTc2Mjk0NjQzNiwic3ViIjoiYXV0aF9jb2RlIn0.raGvBzwJHcDuZ8ZuGE9fKiJh_SmxjhRv-vRRPrKxRBk"

# Create a session object to handle the Fyers API authentication and token generation
session = fyersModel.SessionModel(
    client_id=client_id,
    secret_key=secret_key, 
    redirect_uri=redirect_uri, 
    response_type=response_type, 
    grant_type=grant_type
)

# Set the authorization code in the session object
session.set_token(auth_code)

# Generate the access token using the authorization code
response = session.generate_token()

# Print the response, which should contain the access token and other details
print(response)'''



