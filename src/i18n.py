from yaml import safe_load
import os
from babel.dates import format_date

class Translator:
    def __init__(self, translation_folder, locale='en'):
        self.locale = locale
        locale_file = open(f"{translation_folder}/{locale}.yaml", "r")
        self.data = safe_load(locale_file.read())

    def __call__(self, msg_id, **kwargs):
        if msg_id not in self.data:
            return msg_id

        translation = self.data[msg_id]
        if type(translation) == dict:
            if kwargs["count"] in translation:
                translation = translation[kwargs["count"]]
            else:
                translation = translation["default"]

        if "date" in kwargs:
            kwargs["date"] = format_date(kwargs["date"], locale=self.locale)
        if "count" in kwargs:
            count = kwargs["count"]
            s = "s" if count > 1 else ""
            kwargs["s"] = s
        return translation.format(**kwargs)
