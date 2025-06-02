import re


class PascalCaseToSnakeCase:
    # https://stackoverflow.com/questions/1175208/elegant-python-function-to-convert-camelcase-to-snake-case
    pattern = re.compile(r"(?<!^)(?=[A-Z])")

    @classmethod
    def convert(cls, name):
        return cls.pattern.sub("_", name).lower()
