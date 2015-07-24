from shabus import db
import csv
import os

MEMBERS_CSV_FILENAME = os.path.join(os.path.dirname(__file__), "shabus_members_2015-07-24_15-45-00.csv")

def unicode_csv_reader(utf8_data, **kwargs):
    csv_reader = csv.reader(utf8_data, **kwargs)
    for row in csv_reader:
        yield [unicode(cell, 'utf-8') for cell in row]

def main():
    with open(MEMBERS_CSV_FILENAME) as input_file:
        reader = unicode_csv_reader(input_file)
        recommending_member_phones = {}
        for member_row in reader:
            member, recommending_member_phone = process_row(member_row)
            recommending_member_phones[member] = recommending_member_phone

    for member, recommending_member_phone in recommending_member_phones.items():
        if recommending_member_phone == "":
            continue
        recommending_member = db.query.Member.query.get(phone_number=recommending_member_phone)
        member.recommending_member = recommending_member

    db.session.commit()

def process_row(member_row):
    member_dict = dict(zip(get_csv_columns(), member_row))

    member = db.Member()
    string_member_attributes = ("age", "email", "desired_ride_time", "desired_board_time",
        "desired_return_time", "legal_statement", "signature_image_url",
        "credit_card_payment_products", "credit_card_payer_info", "credit_card_payer_address",
        "jotform_submission_id", "comments")
    for string_attribute in string_member_attributes:
        save_string(member_dict, member, string_attribute)

    address_attribute_prefixes = ("", "additional", "desired_destination")
    for address_prefix in address_attribute_prefixes:
        save_address(member_dict, member, address_prefix)
    bool_attributes = ("backed_on_headstart", "first_of_may", "used_old_form_to_sign_up",
        "is_founder", "is_manager")
    for bool_attribute in bool_attributes:
        save_bool(member_dict, member, bool_attribute)
    save_datetime(member_dict, member, "submission_date")
    db.session.add(member)

    add_passengers(member_dict, member)

    return member, recommending_member_phone_number

def add_passengers(member_dict, member):
    main_passenger = get_main_passenger(member_dict, member)
    family_passengers = get_family_passengers(member_dict, member, main_passenger)

    for passenger in [main_passenger] + family_passengers:
        db.session.add(passenger)

def get_main_passenger(member_dict, member):
    main_passenger = db.Passenger()
    main_passenger.member = member
    main_passenger_attributes = ("last_name", "first_name", "phone_number", "id_number")
    for passenger_attribute in main_passenger_attributes:
        save_string(member_dict, passenger, passenger_attribute)
    save_bool(member_dict, passenger, "has_smartphone")
    main_passenger.passenger_type = "member"
    return main_passenger

def get_family_passengers(member_dict, member, main_passenger):
    if not is_true(member_dict["has_family"])
        return []

    family_passengers = []
    if has_value(member_dict["spouse_phone_number"]):
        family_passengers.append(get_spouse_passenger(member_dict, member))

    if has_value(member_dict["children_phone_numbers"]):
        family_passengers += list(get_child_passengers(member_dict, member))

    family_members_have_smartphone = is_true(member_dict["family_members_have_smartphone"])
    if not family_members_have_smartphone:
        update_family_member_details(member_dict, family_passengers, main_passenger)

    for family_passenger in family_passengers:
        family_passenger.has_smartphone = family_members_have_smartphone

    return family_passengers

def get_spouse_passenger(member_dict, member):
    spouse_passenger = db.Passenger()
    spouse_passenger.member = member
    spouse_passenger.type = "spouse"
    spouse_passenger.phone_number = member_dict["spouse_phone_number"]
    return spouse_passenger

def get_child_passengers(member_dict, member):
    children_phone_numbers = member_dict["children_phone_numbers"].split("\n")
    for child_phone_number in children_phone_numbers:
        child_passenger = db.Passenger()
        child_passenger.member = member
        child_passenger.type = "child"
        child_passenger.phone_number = child_phone_number
        yield child_passenger

def update_family_member_details(member_dict, family_passengers, main_passenger):
    family_member_names = member_dict["family_member_names"].split("\n")
    family_member_id_numbers = member_dict["family_member_id_numbers"].split("\n")
    assert len(family_member_names) == len(family_passengers)
    assert len(family_member_id_numbers) == len(family_passengers)
    for family_passenger, family_member_name, family_member_id_number in \
        zip(family_passengers, family_member_names, family_member_id_numbers):
        family_passenger.first_name = family_member_name
        family_passenger.last_name = main_passenger.last_name
        family_passenger.id_number = family_member_id_number

def get_csv_columns():
    return (
        "repeat_check", "submission_date", "age", "last_name", "first_name", "phone_number",
        "has_smartphone", "email", "street", "house_number", "city", "neighborhood", "zipcode",
        "country", "has_additional_address", "additional_address_street", "additional_address_house_number",
        "additional_address_city", "additional_address_neighborhood", "additional_address_zipcode",
        "additional_address_country", "id_number", "has_family", "spouse_phone_number",
        "children_phone_numbers", "family_members_have_smartphone", "family_member_names",
        "family_member_id_numbers", "family_legal_consent", "desired_destination_street",
        "desired_destination_house_number", "desired_destination_house_city",
        "desired_destination_house_neighborhood", "desired_destination_zipcode",
        "desired_destination_country", "desired_ride_time", "first_of_may",
        "desired_board_time", "desired_return_time", "recommending_member_phone_number",
        "legal_statement", "signature_image_url", "backed_on_headstart",
        "credit_card_payment_products", "credit_card_payer_info", "credit_card_payer_address",
        "ip_address", "jotform_submission_id", "used_old_form_to_sign_up", "dynamic_support_check",
        "dynamic_support_or_payment_check", "dynamic_is_eligible_for_membership", "is_manager",
        "is_founder", "comments")


if __name__ == "__main__":
    main()