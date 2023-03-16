from datetime import datetime


def test_transform_contacts_data_correct_types(data_input):
    for contact in data_input:
        assert isinstance(contact['first_name'], str)
        assert isinstance(contact['custom_properties']['lifetime_value'], float)
        assert isinstance(contact['custom_properties']['airtable_id'], str)


def test_transform_contacts_data_inccorect_types(data_input):
    for contact in data_input:
        assert not isinstance(contact['birthdate'], int)
        assert not isinstance(contact['email'], float)
        assert not isinstance(contact['last_name'], bool)


def test_transform_contacts_data_whitespaces(data_input):
    for contact in data_input:
        assert not contact['first_name'].startswith(" ")
        assert not contact['first_name'].endswith(" ")
        assert not contact['last_name'].startswith(" ")
        assert not contact['last_name'].endswith(" ")


def test_transform_contacts_data_birthday_format(data_input):
    for contact in data_input:
        assert datetime.strptime(contact['birthdate'], "%Y-%m-%d")

