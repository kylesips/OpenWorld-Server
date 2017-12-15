from django.db import models
import uuid
from .enums import Platforms
from django.utils.crypto import get_random_string


class App_Config(models.Model):
  """
  An app configuration (with exception to historical relations) will be unique for each app on each platform
  that integrates with openWorld.  This model inherits a 1 App Configuration to N Permission relationship,
  and the historical iteration model, both outlined above.  App_Name and App_Version are self explanatory.
  App_Platform is an enum that indicates the platform the app is developed for.
  The App_Link links to the app in the platform’s store.
  """

  MAX_NAME_LENGTH = 255  # Per iOS development guide
  MAX_VERSION_LENGTH = 127  # Why on earth would you have a version number longer than 127 characters?
  MAX_URL_LENGTH = 2083  # Seems arbitrary, huh? Nope, it's the standard!
  MAX_PLATFORM_LENGTH = 64  # Seriously common who the hell is gonna make their platform name a sentence in length?
  SECRET_LENGTH = 32

  app_id = models.UUIDField(primary_key=True, default=uuid.uuid4(), editable=False, unique=True)
  app_secret = models.CharField(max_length=SECRET_LENGTH, unique=True, default=get_random_string(SECRET_LENGTH),
                                editable=False)
  app_name = models.CharField(max_length=MAX_NAME_LENGTH)
  app_version = models.CharField(max_length=MAX_VERSION_LENGTH)
  app_icon = models.BinaryField()
  platform = models.CharField(max_length=MAX_PLATFORM_LENGTH, choices=Platforms.choices(), default=Platforms.OTHER)
  app_link = models.CharField(max_length=MAX_URL_LENGTH)

  class Meta:
    unique_together = (('app_version', 'platform'),)


class Device_Browser(models.Model):
  """
  Normalized table used to store information relating to a device of type browser that
  was used to instantiate a particular app instance
  """
  browser_id = models.UUIDField(primary_key=True, default=uuid.uuid4(), editable=False, unique=True)
  browser_name = models.CharField(max_length=App_Config.MAX_NAME_LENGTH)
  browser_manufacturer = models.CharField(max_length=App_Config.MAX_NAME_LENGTH)
  browser_version = models.CharField(max_length=App_Config.MAX_VERSION_LENGTH)
  browser_user_agent = models.CharField(max_length=App_Config.MAX_NAME_LENGTH, unique=True)

  class Meta:
    unique_together = (('browser_version', 'browser_user_agent'),)

class Device_Platform(models.Model):
  """
  Normalized table used to store information relating to a device of type platform that
  was used to instantiate a particular app instance
  """
  platform_id = models.UUIDField(primary_key=True, default=uuid.uuid4(), editable=False, unique=True)
  platform_version = models.CharField(max_length=App_Config.MAX_VERSION_LENGTH)

class App_User(models.Model):
  """
  Normalized table used to store information relating to a user that instantiated a particular app instance
  """
  user_id = models.UUIDField(primary_key=True, default=uuid.uuid4(), editable=False, unique=True)
  user_secret = models.CharField(max_length=App_Config.SECRET_LENGTH, unique=True,
                                 default=get_random_string(App_Config.SECRET_LENGTH), editable=False)


class App_User_Metadata_Language(models.Model):
  language_id = models.UUIDField(primary_key=True, default=uuid.uuid4(), editable=False, unique=True)
  user = models.ForeignKey(App_User, on_delete=models.CASCADE)
  language_title = models.CharField(max_length=App_Config.MAX_NAME_LENGTH)



class App_Instance(models.Model):
  """
   When a device wants to connect for the first time to openWorld, the device sends the App_ID and App_Secret
   to openWorld.  Once a valid combination is authenticated then openWorld will generate a unique App Instance,
   and will respond to the device with a User_ID and User_Secret.  The User_ID is issued by openWorld for an
   individual user per  app per device.  Unless the app syncs the User tokens with their services, we treat
   every login as a new user.  The first time a device connects they will also send Platform_Version, and
   Device_Identifiers.  If the application is a website running in a browser, then the Browser_Version and
   Browser_User_Agent will also be included.
  """
  instance_id = models.UUIDField(primary_key=True, default=uuid.uuid4(), editable=False, unique=True)
  app = models.ForeignKey(App_Config, on_delete=models.PROTECT)
  platform = models.OneToOneField(Device_Platform, on_delete=models.PROTECT)
  browser = models.OneToOneField(Device_Browser, on_delete=models.PROTECT)
  user = models.OneToOneField(App_User, on_delete=models.PROTECT)
