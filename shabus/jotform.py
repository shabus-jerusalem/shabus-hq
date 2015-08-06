# coding=utf-8
import time

def get_member_dict(jotform_data):
    member = {}
    for jotform_name, shabus_name in JOTFORM_FIELD_NAMES_MAP.items():
        member[shabus_name] = jotform_data[jotform_name]
    member["creation_date"] = time.strftime("%d-%m-%Y %H:%M:%S")
    member["signature_image_url"] = "uploads/shabus/%(form_id)s/%(submission_id)s/%(submission_id)s_base64_10.png" % {
        "form_id": jotform_data["formID"], "submission_id": jotform_data["submission_id"]}

    member["last_name"], member["first_name"] = request.form.getlist("input4[]")
    add_address(request.form.getlist("input7[]"), "", member)
    # add_address(request.form.getlist("input40[]"), "additional_address_", member)
    # add_address(request.form.getlist("input42[]"), "desired_destination_", member)

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
        OLD_ATTRIBUTES += [prefix + name for name in ADDRESS_ATTRIBUTE_NAMES]

    for old_attribute in OLD_ATTRIBUTES:
        member[old_attribute] = ""

    member["comments"] = "jotform-signup"

    # paypal_data = request.form.getlist("input49[]")
    # paypal_field_names = (
    #     "credit_card_payment_products",
    #     "credit_card_payer_info",
    #     "credit_card_payer_address")
    # paypal_fields = zip(paypal_field_names, paypal_data)
    # for name, value in paypal_fields.items():
    #     member[name] = value

    return member

ADDRESS_ATTRIBUTE_NAMES = ["street", "number", "city", "neighborhood", "zipcode", "country"]

def add_address(values, prefix, member):
    address_attributes = zip(ADDRESS_ATTRIBUTE_NAMES, values)
    for name, value in address_attributes.items():
        member[prefix + name] = value


JOTFORM_FIELD_NAMES_MAP = {
    "submission_id": "jotform_submission_id",
    "input62": "age",
    "input43": "has_family",
    "input17": "phone_number",
    # "input51[]": "has_smartphone",
    # "input18": "desired_ride_time",
    "input6": "email",
    "input22": "id_number",
    "input23": "spouse_phone_number",
    "input25": "children_phone_numbers",
    #"input53[]": "family_members_have_smartphone",
    "input29[]": "family_legal_consent",
    # "input41": "has_additional_address"
    # "input48": "backed_on_headstart",
    # "input35": "desired_board_time",
    # "input36": "desired_return_time",
    "input59": "recommending_member_phone_number",
    #"input55": "family_member_names",
    #"input56": "family_member_id_numbers",
    "clickto27": "legal_statement"
}

# safe to ignore (unused in import_members.py):
# repeat_check
# dynamic_support_check
# dynamic_support_or_payment_check
# dynamic_is_eligible_for_membership
# ip_address
