"""
The following enum class is attributed to Anthony Fox
Sauce: http://anthonyfox.io/2017/02/choices-for-choices-in-django-charfields/
"""
from enum import Enum

class ChoiceEnum(Enum):
    @classmethod
    def choices(cls):
        return tuple((x.name, x.value) for x in cls)

class Platforms(ChoiceEnum):
  """
  Enumerator for supported platforms, using encapsulation to restrict the use of this enum to the AppConfig model
  """
  IOS = "iOS"
  WEB = "Web"
  OTHER = "Other"