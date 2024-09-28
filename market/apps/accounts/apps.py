from django.apps import AppConfig
import importlib

class AccountsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.accounts'

    def ready(self):
        importlib.import_module('apps.accounts.signals')