import json

def dictToJson(dict_Text):
    # ESTA FUNÇÃO SUBSTITUÍ O CARACTERE ' PELO CARACTERE "
    correct_text = ""
    for i in range(0,len(dict_Text)):
        if dict_Text[i] == "'":

            correct_text = correct_text + '"'
        else:
            correct_text = correct_text + dict_Text[i]
    
    jsonData = json.loads(correct_text)

    return jsonData