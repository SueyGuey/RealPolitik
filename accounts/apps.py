from django.apps import AppConfig


class AccountsConfig(AppConfig):
    name = 'accounts'
    #automatically creates profile
    def ready(self):
    	import accounts.signals
