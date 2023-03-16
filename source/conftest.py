import pytest
from get_post_contacts import GetPostDatacose


# Setup to use once per module
@pytest.fixture(scope="module")
def data_input():
    cls = GetPostDatacose()
    initial_data = cls.get_contacts_data()
    transformed_data_ouput = cls.transform_contacts_data(initial_data)
    return transformed_data_ouput
