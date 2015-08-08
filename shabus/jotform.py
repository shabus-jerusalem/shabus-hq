# coding=utf-8
import json
import time

def get_member_dict(jotform_request):
    member = {}
    member["jotform_submission_id"] = jotform_request["submissionID"]
    jotform_data = json.loads(jotform_request["rawRequest"])

    for jotform_name, shabus_name in JOTFORM_FIELD_NAMES_MAP.items():
        member[shabus_name] = jotform_data[jotform_name]

    member["creation_date"] = time.strftime("%d-%m-%Y %H:%M:%S")
    member["signature_image_url"] = "uploads/shabus/%(form_id)s/%(submission_id)s/%(submission_id)s_base64_10.png" % {
        "form_id": jotform_request["formID"], "submission_id": jotform_request["submissionID"]}
    member["first_name"] = jotform_data["q4_input4"]["first"]
    member["last_name"] = jotform_data["q4_input4"]["last"]
    set_address(jotform_data["q7_input7"], member)
    set_ignored_attributes(member)
    member["comments"] = "jotform-signup"

    return member

def set_address(address_attributes, member):
    for jotform_name, dict_name in ADDRESS_ATTRIBUTE_NAMES_MAP.items():
        member[dict_name] = address_attributes[jotform_name]

def set_ignored_attributes(member):
    OLD_ATTRIBUTES = [
        "first_of_may",
        "used_old_form_to_sign_up",
        "is_manager",
        "is_founder",
        "has_smartphone",
        "desired_ride_time",
        "family_members_have_smartphone",
        "has_additional_address",
        "backed_on_headstart",
        "desired_board_time",
        "desired_return_time",
        "family_member_names",
        "family_member_id_numbers"
    ]

    OLD_ATTRIBUTES += [
        "credit_card_payment_products",
        "credit_card_payer_info",
        "credit_card_payer_address"
    ]

    for prefix in ["additional_address_", "desired_destination_"]:
        OLD_ATTRIBUTES += [prefix + name for name in ADDRESS_ATTRIBUTE_NAMES_MAP.values()]

    for old_attribute in OLD_ATTRIBUTES:
        member[old_attribute] = ""


JOTFORM_FIELD_NAMES_MAP = {
    "q62_input62": "age",
    "q43_input43": "has_family",
    "q17_input17": "phone_number",
    # "input51[]": "has_smartphone",
    # "input18": "desired_ride_time",
    "q6_input6": "email",
    "q22_input22": "id_number",
    "q23_input23": "spouse_phone_number",
    "q25_input25": "children_phone_numbers",
    #"input53[]": "family_members_have_smartphone",
    "q29_input29[]": "family_legal_consent",
    # "input41": "has_additional_address"
    # "input48": "backed_on_headstart",
    # "input35": "desired_board_time",
    # "input36": "desired_return_time",
    "q59_input59": "recommending_member_phone_number",
    #"input55": "family_member_names",
    #"input56": "family_member_id_numbers",
    "q27_clickTo27": "legal_statement"
}

ADDRESS_ATTRIBUTE_NAMES_MAP = {
    "addr_line1": "street",
    "addr_line2": "number",
    "city": "city",
    "state": "neighborhood",
    "postal": "zipcode",
    "country": "country"
}

# safe to ignore (unused in import_members.py):
# repeat_check
# dynamic_support_check
# dynamic_support_or_payment_check
# dynamic_is_eligible_for_membership
# ip_address
