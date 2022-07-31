def get_game_category(queue_id):
    # REFERENCE LINK
    #https://static.developer.riotgames.com/docs/lol/queues.json

    category = ""
    if queue_id == 420:
        category = "Ranked Solo"
    elif queue_id == 400:
        category = "Normal Alternado"
    elif queue_id == 430:
        category = "Normal Às cegas"
    elif queue_id == 450:
        category = "ARAM"
    elif queue_id == 440:
        category = "Ranked Flex"
    elif queue_id == 830:
        category = "Coop vs AI Introdução"
    elif queue_id == 840:
        category = "Coop vs AI Iniciante"
    elif queue_id == 850:
        category = "Coop vs AI Intermediário"
    elif queue_id == 900:
        category = "ARURF"
    elif queue_id == 700:
        category = "Clash"
    else:
        category = "Special Game Mode"

    return category