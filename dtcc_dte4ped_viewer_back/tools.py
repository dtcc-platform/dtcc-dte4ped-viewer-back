import os

from django.core.exceptions import ImproperlyConfigured


def get_secret(secret, secrets, default=None):
    if secrets['SECRETS_FROM'] == "ENVVARS":
        return os.environ.get(secret, default)
    else:
        try:
            return secrets[secret]
        except KeyError:
            if default is None:
                error_msg = "Set the {0} environment variable".format(secret)
                raise ImproperlyConfigured(error_msg)
            else:
                return default