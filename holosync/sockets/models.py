from django.db import models
import uuid
from .enums import Platforms

class App_Config(models.Model):
  """
  An app configuration (with exception to historical relations) will be unique for each app on each platform
  that integrates with openWorld.  This model inherits a 1 App Configuration to N Permission relationship,
  and the historical iteration model, both outlined above.  App_Name and App_Version are self explanatory.
  App_Platform is an enum that indicates the platform the app is developed for.
  The App_Link links to the app in the platform’s store.
  """

  MAX_NAME_LENGTH = 255    # Per iOS development guide
  MAX_VERSION_LENGTH = 127 # Why on earth would you have a version number longer than 127 characters?
  MAX_URL_LENGTH = 2083    # Seems arbitrary, huh? Nope, it's the standard!
  MAX_PLATFORM_LENGTH = 64 # Seriously common who the hell is gonna make their platform name a sentence in length?

  app_id = models.UUIDField(primary_key=True, default=uuid.uuid4(), editable=False)
  app_secret = models.UUIDField(unique=True, default=uuid.uuid4(), editable=False)
  app_name = models.CharField(max_length=MAX_NAME_LENGTH)
  app_version = models.CharField(max_length=MAX_VERSION_LENGTH)
  app_icon = models.BinaryField()
  platform = models.CharField(max_length=MAX_PLATFORM_LENGTH, choices=Platforms.choices(), default=Platforms.OTHER)
  app_link = models.CharField(max_length=MAX_URL_LENGTH)

  class Meta:
    unique_together = (('app_version','platform'),)



