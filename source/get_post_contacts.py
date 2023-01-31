import requests
import logging
from typing import List
from datetime import datetime
from decouple import config


class GetPostDatacose:
    def __init__(self):
        logging.basicConfig(level=logging.INFO)
        # Using empty string default in case the first arg is not in the .env file to avoid errors
        self.user = config('API_USER', default='')
        self.passw = config('API_PASSW', default='')
        self.api_key = config('API_KEY', default='')
        self.get_url = "https://challenge-automation-engineer-xij5xxbepq-uc.a.run.app/people/"
        self.post_url = "https://challenge-automation-engineer-xij5xxbepq-uc.a.run.app/contacts/"

    def get_contacts_data(self) -> List[dict]:
        """
        Method to get all the contacts data from the /people/ endpoint.
        """

        people_data = []
        get_headers = {
            "Accept": "application/json",
            "Authorization": self.api_key
        }
        try:
            res = requests.get(self.get_url, headers=get_headers)
            res.raise_for_status()  # To raise status for the exception to catch
            contacts_data = res.json()  # Parse data as json
            for contact in contacts_data:
                people_data.append(contact)  # Make a list of dicts to return them forward
        except requests.exceptions.HTTPError as err:
            logging.error(err)
            raise SystemExit
        logging.info(f"Stored data for {len(people_data)} contacts succesfully!")
        return people_data

    def transform_contacts_data(self, data: List[dict]) -> List[dict]:
        """
        Method that cleans the data received from the /people/ endpoint.
        """

        if not data:
            raise EmptyDataList(message=f"There is no data in the contact list for "
                                        f"{self.transform_contacts_data.__name__}")
        transformed_contacts = []

        # Iterate through the contacts, clean the data and send them forward as the correct dict obj
        for contact in data:
            contact_obj = {
                "first_name": contact['fields']['firstName'].strip(),
                "last_name": contact['fields']['lastName'].strip(),
                "birthdate": datetime.strptime(contact['fields']['dateOfBirth'],
                                               "%d-%m-%Y").strftime("%Y-%m-%d"),
                "email": contact['fields']['email'],
                "custom_properties": {
                    "airtable_id": contact['id'],
                    "lifetime_value": float \
                        (contact['fields']['lifetime_value'].replace("$", ""))
                }
            }
            transformed_contacts.append(contact_obj)
        logging.info(f"Finished cleaning data for {len(transformed_contacts)} contacts!")
        return transformed_contacts

    def post_contacts_data(self, data: List[dict]) -> None:
        """
        Method to post all the cleaned contacts data to the /contacts/ endpoint.
        """

        if not data:
            raise EmptyDataList(message=f"There is no data in the contact list for "
                                        f"{self.post_contacts_data.__name__}")

        post_headers = {
            "Accept": "application/json",
            "Content-Type": "application/json"
        }

        # For each contact send a post req, using basic auth and the data in a json body
        for contact in data:
            try:
                res = requests.post(self.post_url, auth=(self.user, self.passw),
                                    headers=post_headers,
                                    json=contact)
                res.raise_for_status()
            except requests.exceptions.HTTPError as err:
                logging.error(err)
                raise SystemExit
        logging.info(f"POST Request succesfully made for all {len(data)} contacts!")


class EmptyDataList(Exception):
    """
    Custom error raised when the data list for contacts is empty.
    """

    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__(message)
