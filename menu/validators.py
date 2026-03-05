from django.core.exceptions import ValidationError


def normalize_name(self):
    splited_name = self.name.strip().split(" ")
    normalized_name = []

    for word in splited_name:
        if len(word) > 3: #if one of the words inside the name has more than 3 letters, it should be capitalized.
            normalized_name.append(word.capitalize())
        else: #if not, it is only a compound word and should not be capitalized
            normalized_name.append(word)
    self.name = " ".join(normalized_name)


def normalize_description(self):
    splited_description = self.description.strip().split(".")
    normalized_description = []

    for phrase in splited_description:
        normalized_description.append(phrase.strip().capitalize())
    self.description = ". ".join(normalized_description)