import json

def dictToJson(dict_Text):
    # THIS FUNCTION REPLACES THE CHARACTER ' BY CHARACTER "
    correct_text = ""
    for i in range(0,len(dict_Text)):
        if dict_Text[i] == "'":

            correct_text = correct_text + '"'
        else:
            correct_text = correct_text + dict_Text[i]
    
    jsonData = json.loads(correct_text)

    return jsonData