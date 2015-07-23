# coding=utf-8
"""
Form fields are:
    q37_input37  => age (radio: "18 ומעלה" or "עוד לא 18")
    q4_input4 => name (array: [first, last])
    q17_input17 => cellphone
    q5_input51 => has_smartphone (some long value in hebrew)
    q6_input6 => mail
    q7_input7 => address (array: [addr_line1, addr_line2, city, postal])
    q41_input41 => has_additional_address (radio: כן / לא)
    q40_input40 => addition_address (same as address)
    q22_input22 => id
"""
#TODO: Get all fields
JOTFORM_FIELDS = {
    "q37_input37" : "age",
    "q4_input4" : "name",
    "q17_input17" : "phone",
    "q23_input23" : "spouse_phone",
    "q25_input25" : "children_phone", # Seperated by \n
    "q5_input51" : "has_smartphone",
    "q6_input6" : "mail",
    "q7_input7" : "address",
    "q41_input41" : "has_additional_address",
    "q40_input40" : "addition_address",
    "q22_input22" : "id",
    "q48_input48" : "headstart",
    "q49_input49" : "paypal",
    "q42_input42" : "target_address",
    "q27_clickTo27" : "agreement",
    "q10_input10" : "signature",
    "q43_input43" : "has_spouse"
}

def rename_fields(form):
    """
    Renams a jotform form according to JOTFORM_FIELDS
    :param form: the form to convert
    :return: a converted form
    """
    newForm = {}
    for key, value in form.iteritems():
        newForm[JOTFORM_FIELDS.get(key, key)] = value
    return newForm