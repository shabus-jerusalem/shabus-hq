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



"""
submission_id:YYYY
formID:XXXX
ip:11.22.33.11
input62:24
input43:כן
input4[]:ישראלי
input4[]:ישראל
input17:0525949618
input51[]:יש לי טלפון חכם (שמאפשר הורדת אפליקציה וגלישה סלולרית)
input6:matsatl@gasc.com
input7[]:יוחנן
input7[]:13
input7[]:ירושלים
input7[]:
input7[]:
input7[]:Haiti
input40[]:
input40[]:
input40[]:
input40[]:
input40[]:
input40[]:
input22:242350893
input23:0525981524
input25:
input53[]:יש לכל בני המשפחה טלפונים חכמים (שמאפשרים הורדת אפליקציה וגלישה סלולרית)
input29[]:כל הפרטים שלעיל שייכים אך ורק לבן/בת זוגי וילדי עד גיל 18
input42[]:
input42[]:
input42[]:
input42[]:
input42[]:
input42[]:Israel
input59:2415125125
clickto27:אני <u>תחיל</u> תעודת זהות <u>87987987</u> כתובת <u>לחילחי</u> מבקש/ת בזה להתקבל כחבר/ה ב"האגודה לתחבורה שיתופית בע"מ". אם אתקבל כחבר/ה באגודה, הנני מתחייב/ת למלא אחר הוראות תקנון האגודה. הנני מסכים/ה, כי כל הרשום בספרי האגודה יחייב אותי בקשר לכל ענין הנוגע לחובותיי כלפי האגודה או לתביעותיי מהאגודה. אני מתחייב/ת שלא לפעול בניגוד לעקרונות האגודה, בניגוד לעקרונות התנועה הקואופרטיבית, או בניגוד לאינטרסים של האגודה. אני מצהיר/ה, כי הוראות תקנון האגודה ידועות לי.
אני מעוניין/ת להיות חבר/ה באגודה לתחבורה שיתופית בירושלים. אני תומך/ת באגודה ובמטרותיה.
input10:data:image/png;base64,blabla=
"""
