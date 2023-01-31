from get_post_contacts import GetPostDatacose


def main():
    cls = GetPostDatacose()
    initial_data = cls.get_contacts_data()
    transformed_data = cls.transform_contacts_data(initial_data)
    cls.post_contacts_data(transformed_data)


if __name__ == "__main__":
    main()
