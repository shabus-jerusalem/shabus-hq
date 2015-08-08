# -*- coding: utf-8 -*-
import sys
import os
import csv
import datetime
import logging
localpath = lambda name: os.path.join(os.path.dirname(__file__), name)
sys.path.append(localpath(".."))
from shabus.models import Member, Passenger, Address
from shabus import db

MEMBERS_CSV_FILENAME = localpath("shabus_members_2015-07-30_01-27-00.csv")

def main():
    logging.basicConfig(
        filename=localpath("import_members.log"),
        level=logging.DEBUG,
        format="%(asctime)s %(name)-12s %(levelname)-8s %(message)s")

    import_from_csv()

def unicode_csv_reader(utf8_data, **kwargs):
    csv_reader = csv.reader(utf8_data, **kwargs)
    for row in csv_reader:
        yield [unicode(cell, 'utf-8') for cell in row]

def import_from_csv():
    with open(MEMBERS_CSV_FILENAME) as input_file:
        reader = unicode_csv_reader(input_file)
        recommending_member_phones = {}
        # Skip header row
        next(reader)
        for row_number, member_row in enumerate(reader):
            logging.info("Processing row: %s", row_number)
            if member_row[0] == u"הסתר":
                logging.info("Row is hidden - skipping")
                continue
            try:
                member, recommending_member_phone = process_row(member_row)
                recommending_member_phones[member] = recommending_member_phone
                db.session.commit()
            except Exception as e:
                message = str(e)
                if "duplicate key value" in message:
                    detail = "DETAIL:  "
                    duplicate_value = message[message.find(detail) + len(detail):]
                    logging.error("Failed to process row. Duplicate value found: %s", duplicate_value)
                else:
                    logging.exception("Error while processing row %s: ", row_number)
                db.session.rollback()

    for member, recommending_member_phone in recommending_member_phones.items():
        process_recommending_member_phone(member, recommending_member_phone)

    db.session.commit()

def process_row(member_row):
    member_dict = dict(zip(get_csv_columns(), member_row))
    return add_member(member_dict)

def add_member(member_dict):
    member = Member()
    string_member_attributes = ("age", "email", "desired_ride_time", "desired_board_time",
        "desired_return_time", "legal_statement", "signature_image_url",
        "credit_card_payment_products", "credit_card_payer_info", "credit_card_payer_address",
        "jotform_submission_id", "comments")
    for string_attribute in string_member_attributes:
        save_string(member_dict, member, string_attribute)

    address_attribute_prefixes = {
        "address": "",
        "additional_address": "additional_address_",
        "desired_destination_address": "desired_destination_"}
    for address_name, address_prefix in address_attribute_prefixes.items():
        add_address(member_dict, member, address_name, address_prefix)
    bool_attributes = ("backed_on_headstart", "first_of_may", "used_old_form_to_sign_up",
        "is_founder", "is_manager")
    for bool_attribute in bool_attributes:
        save_bool(member_dict, member, bool_attribute)
    save_datetime(member_dict, member, "creation_date")
    db.session.add(member)

    add_passengers(member_dict, member)

    return member, member_dict["recommending_member_phone_number"]

def add_passengers(member_dict, member):
    main_passenger = get_main_passenger(member_dict, member)
    family_passengers = get_family_passengers(member_dict, member, main_passenger)

    for passenger in [main_passenger] + family_passengers:
        db.session.add(passenger)

def get_main_passenger(member_dict, member):
    # The passenger can already exist if it was a spouse of a previous passenger
    main_passenger = Passenger.query.filter(Passenger.phone_number==member_dict["phone_number"]).first()
    if not (main_passenger and main_passenger.passenger_type == "spouse"):
        main_passenger = Passenger()
    main_passenger.member = member
    member_dict["phone_number"] = clean_phone_number(member_dict["phone_number"])
    member_dict["id_number"] = clean_id_number(member_dict["id_number"])
    main_passenger_attributes = ("last_name", "first_name", "phone_number", "id_number")
    for passenger_attribute in main_passenger_attributes:
        save_string(member_dict, main_passenger, passenger_attribute)
    save_bool(member_dict, main_passenger, "has_smartphone")
    main_passenger.passenger_type = "member"
    return main_passenger

def get_family_passengers(member_dict, member, main_passenger):
    if not is_true(member_dict["has_family"]):
        return []

    family_passengers = []
    if has_spouse(member_dict) and not passenger_exists(member_dict["spouse_phone_number"]):
        family_passengers.append(get_spouse_passenger(member_dict, member))

    if has_value(member_dict["children_phone_numbers"]):
        family_passengers += list(get_child_passengers(member_dict, member))

    family_members_have_smartphone = is_true(member_dict["family_members_have_smartphone"])
    if not family_members_have_smartphone:
        update_family_member_details(member_dict, family_passengers, main_passenger)

    for family_passenger in family_passengers:
        family_passenger.has_smartphone = family_members_have_smartphone

    return family_passengers

def passenger_exists(phone_number):
    return db.session.query(db.exists().where(Passenger.phone_number==phone_number)).scalar()

def has_spouse(member_dict):
    if has_value(member_dict["spouse_phone_number"]):
        return True
    child_phone_numbers_count = get_child_phone_numbers_count(member_dict)
    family_members_without_smartphone_count = get_family_members_without_smartphone_count(member_dict)
    return family_members_without_smartphone_count - child_phone_numbers_count == 1

def get_child_phone_numbers_count(member_dict):
    return get_entity_count_from_multiline_field(member_dict, "children_phone_numbers")

def get_family_members_without_smartphone_count(member_dict):
    return get_entity_count_from_multiline_field(member_dict, "family_member_names")

def get_entity_count_from_multiline_field(member_dict, field_name):
    if not has_value(member_dict[field_name]):
        return 0
    return len(member_dict[field_name].split("\n"))

def get_spouse_passenger(member_dict, member):
    spouse_passenger = Passenger()
    spouse_passenger.member = member
    spouse_passenger.passenger_type = "spouse"
    spouse_passenger.phone_number = clean_phone_number(member_dict["spouse_phone_number"])
    return spouse_passenger

def get_child_passengers(member_dict, member):
    children_phone_numbers = member_dict["children_phone_numbers"].split("\n")
    for child_phone_number in children_phone_numbers:
        child_passenger = Passenger()
        child_passenger.member = member
        child_passenger.passenger_type = "child"
        child_passenger.phone_number = clean_phone_number(child_phone_number)
        yield child_passenger

def update_family_member_details(member_dict, family_passengers, main_passenger):
    if not has_value(member_dict["family_member_names"]) \
        and not has_value(member_dict["family_member_id_numbers"]):
        return

    family_member_names = member_dict["family_member_names"].split("\n")
    family_member_id_numbers = member_dict["family_member_id_numbers"].split("\n")
    assert len(family_member_names) == len(family_passengers)
    assert len(family_member_id_numbers) == len(family_passengers)
    for family_passenger, family_member_name, family_member_id_number in \
        zip(family_passengers, family_member_names, family_member_id_numbers):
        family_passenger.first_name = family_member_name
        family_passenger.last_name = main_passenger.last_name
        family_passenger.id_number = clean_id_number(family_member_id_number)

ADDRESS_ATTRIBUTE_NAMES = ["street", "number", "city", "neighborhood", "zipcode", "country"]
def add_address(member_dict, member, address_name, address_prefix):
    address_attributes = [address_prefix + attribute for attribute in ADDRESS_ATTRIBUTE_NAMES]
    # If all address fields are empty, don't save the address
    if all(not has_value(member_dict[attribute]) for attribute in address_attributes):
        return

    address = Address()
    for attribute in ADDRESS_ATTRIBUTE_NAMES:
        setattr(address, attribute, member_dict[address_prefix + attribute])
    db.session.add(address)

    setattr(member, address_name, address)

def process_recommending_member_phone(member, recommending_member_phone):
    if not has_value(recommending_member_phone):
        return True
    recommending_passenger = Passenger.query.filter(Passenger.phone_number==recommending_member_phone).first()
    if not recommending_passenger:
        logging.error(
            "Invalid recommending member phone number '%s' for member with email '%s'" % (
                recommending_member_phone, member.email))
        return False

    recommending_member = recommending_passenger.member
    if recommending_member == member:
        logging.error("Member %s recommended himself" % member.email)
        return False

    member.recommending_member = recommending_passenger.member
    db.session.commit()
    return True

def get_csv_columns():
    return (
        "repeat_check", "creation_date", "age", "last_name", "first_name", "phone_number",
        "has_smartphone", "email", "street", "number", "city", "neighborhood", "zipcode",
        "country", "has_additional_address", "additional_address_street", "additional_address_number",
        "additional_address_city", "additional_address_neighborhood", "additional_address_zipcode",
        "additional_address_country", "id_number", "has_family", "spouse_phone_number",
        "children_phone_numbers", "family_members_have_smartphone", "family_member_names",
        "family_member_id_numbers", "family_legal_consent", "desired_destination_street",
        "desired_destination_number", "desired_destination_city",
        "desired_destination_neighborhood", "desired_destination_zipcode",
        "desired_destination_country", "desired_ride_time", "first_of_may",
        "desired_board_time", "desired_return_time", "recommending_member_phone_number",
        "legal_statement", "signature_image_url", "backed_on_headstart",
        "credit_card_payment_products", "credit_card_payer_info", "credit_card_payer_address",
        "ip_address", "jotform_submission_id", "used_old_form_to_sign_up", "dynamic_support_check",
        "dynamic_support_or_payment_check", "dynamic_is_eligible_for_membership", "is_manager",
        "is_founder", "comments")

def clean_id_number(id_number):
    if id_number == "":
        logging.error("Found empty id number")
        return ""
    if not id_number.isdigit() or len(id_number) > 9:
        logging.error("Found invalid id number: %s", id_number)
        return id_number
    return id_number.zfill(9)

def clean_phone_number(phone_number):
    if phone_number == "":
        logging.error("Found empty phone number")
        return ""
    stripped_number = phone_number.replace("-", "")
    if stripped_number == "":
        logging.error("Found invalid phone number: %s", phone_number)
        return ""

    if not stripped_number.isdigit() or len(stripped_number) != 10 \
        or not stripped_number.startswith("05") or stripped_number == "":
        logging.error("Found invalid phone number: %s", phone_number)
        return phone_number

    return stripped_number

def save_value(attribute_dict, entity, attribute_name, parsing_function):
    parsed_value = parsing_function(attribute_dict[attribute_name])
    setattr(entity, attribute_name, parsed_value)

def make_save_function(parsing_function):
    def save_func(attribute_dict, entity, attribute_name):
        save_value(attribute_dict, entity, attribute_name, parsing_function)
    return save_func

def is_true(string_bool_value):
    if string_bool_value == u"לא" or not has_value(string_bool_value):
        return False
    return True

def parse_datetime(datetime_string):
    try:
        return datetime.datetime.strptime(datetime_string, "%d.%m.%Y %H:%M:%S")
    except ValueError:
        try:
            return datetime.datetime.strptime(datetime_string, "%d/%m/%Y %H:%M:%S")
        except ValueError:
            return datetime.datetime.strptime(datetime_string, "%d-%m-%Y %H:%M:%S")

def has_value(value):
    return value.strip() != ""

def get_string_value(value):
    if not has_value(value):
        return None
    return value

save_string = make_save_function(get_string_value)
save_bool = make_save_function(is_true)
save_datetime = make_save_function(parse_datetime)

if __name__ == "__main__":
    main()
