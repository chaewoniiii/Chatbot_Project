

intent_data = []
ner_data = []

def check_intent(intent):
    return True if intent in intent_data else False

def check_ner(ner):
    return True if ner in ner_data else False
