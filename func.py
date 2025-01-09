from parliament import Context, event
import os
import requests
import logging
import sys

logger = logging.getLogger()
handler = logging.StreamHandler(sys.stdout)  # Write to stdout
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.INFO)

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

    data = context.cloud_event.data
    keys_to_check = ['API_URL']
    if not all(key in data for key in keys_to_check):
        return {"error" : "data keys invalid"}

    logger.info("Polling " + data["API_URL"]) 
    try:
        # Perform the HTTP GET request
        response = requests.get(data['API_URL'])
        response.raise_for_status()  # Raise an exception for HTTP errors
        
        # Try to parse the response as JSON
        try:
            return response.json()
        except ValueError:
            # If response isn't JSON, return as text
            return response.text
    except requests.RequestException as e:
        raise RuntimeError(f"Failed to fetch data from '{data['API_URL']}': {e}")
