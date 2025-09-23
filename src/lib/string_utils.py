def clean_name(name: str):
    to_be_removed = ["\u2122", "\u00ae", "\u2019"]
    for string in to_be_removed:
        name = name.replace(string, "")

    return name
