import json

def dictToJson(dict_text):
    # THIS FUNCTION REPLACES THE CHARACTER ' BY CHARACTER "
    if dict_text:
        correct_text = ""
        for char in dict_text:
            if char == "'":
                correct_text = correct_text + '"'
            else:
                correct_text = correct_text + char
        json_data = json.loads(correct_text)
        return json_data
    else:
        return {}