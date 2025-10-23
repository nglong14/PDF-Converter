import re

def clean_text(text):
    text = re.sub(r"\s+", " ", text) #white spaces
    text = re.sub(r"([.,!?:;])(?=\S)", r"\1", text) #add space after punctuation
    text = re.sub(r"\s([?.!](?:\s|$))", r"\1", text) #remove space before punctuation
    return text.strip()