from open_gallery.api.settings import APISettings
from open_gallery.dishka.providers.settings import BaseSettingsProvider


class SettingsProvider(BaseSettingsProvider):
    root_settings = APISettings
