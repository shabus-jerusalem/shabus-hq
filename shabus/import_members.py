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
    db.session.add()

    return member, recommending_member_phone_number

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
