from django.apps import AppConfig
from django.core import checks
from .checks import templates_do_not_do_queries


class MoreChecksConfig(AppConfig):
    name = 'morechecks'
    verbose_name = "More checks"

    def ready(self):
        checks.register('morechecks', 'templates', 'context_processors')(templates_do_not_do_queries)
