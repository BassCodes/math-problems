import re

from django.core import validators
from django.utils.deconstruct import deconstructible
from django.utils.translation import gettext_lazy as _


@deconstructible
class CustomAsciiUsernameValidator(validators.RegexValidator):
    regex = r"^[a-z0-9_]+\Z"
    message = _(
        "Enter a valid username. This value may contain only unaccented lowercase a-z "
        "and underscores (_)."
    )
    flags = re.ASCII
