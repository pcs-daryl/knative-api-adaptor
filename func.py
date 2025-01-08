from parliament import Context, event
import os
import requests

@event
def main(context: Context):
    """
    Function template
    The context parameter contains the Flask request object and any
    CloudEvent received with the request.
    """

    # Add your business logic here

    # The return value here will be applied as the data attribute
    # of a CloudEvent returned to the function invoker

    url = os.getenv("API_URL")
    if not url:
        raise ValueError(f"The environment variable 'API_URL' is not set or empty.")

    verify_tls = os.getenv("VERIFY_TLS") if os.getenv("VERIFY_TLS") else False

    try:
        # Perform the HTTP GET request
        response = requests.get(url, verify=verify_tls)
        response.raise_for_status()  # Raise an exception for HTTP errors
        
        # Try to parse the response as JSON
        try:
            return response.json()
        except ValueError:
            # If response isn't JSON, return as text
            return response.text
    except requests.RequestException as e:
        raise RuntimeError(f"Failed to fetch data from '{url}': {e}")
