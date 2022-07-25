import spacy


def get_spacy_path():
    current_path = "data/en_core_web_lg-2.2.5.tar.gz"
    return str(current_path)


print(get_spacy_path())
nlp = spacy.load(get_spacy_path())
