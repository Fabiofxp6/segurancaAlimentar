from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.test.runner import DiscoverRunner


def validate_test_database(database: dict) -> None:
    expected = {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "seguranca_alimentar_test",
        "USER": "seguranca_test",
        "HOST": "127.0.0.1",
        "PORT": "55433",
    }
    if any(str(database.get(key)) != value for key, value in expected.items()):
        raise ImproperlyConfigured(
            "Use o banco de testes isolado descrito no README."
        )


class IsolatedTestRunner(DiscoverRunner):
    def run_tests(self, test_labels, **kwargs):
        if settings.SETTINGS_MODULE != "config.settings.test":
            raise ImproperlyConfigured("A execução dos testes exige config.settings.test.")
        validate_test_database(settings.DATABASES["default"])
        return super().run_tests(test_labels, **kwargs)
