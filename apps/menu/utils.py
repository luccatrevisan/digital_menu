def normalize_name(value):
    splited_name = value.strip().split(" ")
    normalized_name = []

    for word in splited_name:
        if len(word) > 3: # if one of the words inside the name has more than 3 letters, it should be capitalized.
            normalized_name.append(word.capitalize())
        else: #if not, it is only a compound word and should not be capitalized
            normalized_name.append(word)
    value = " ".join(normalized_name)
    return value


def normalize_description(value):
    splited_description = value.strip().split(".")
    normalized_description = []

    for phrase in splited_description:
        normalized_description.append(phrase.strip().capitalize())
    value = ". ".join(normalized_description)
    return value