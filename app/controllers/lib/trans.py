from translate import Translator

def translate(text, dest):
    translator = Translator(to_lang=dest)
    return translator.translate(text)