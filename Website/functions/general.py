from Website.models import AccessCode
from django.utils.crypto import get_random_string
from django.contrib.auth.tokens import PasswordResetTokenGenerator


class TokenGenerator(PasswordResetTokenGenerator):

    # Create email confirmation token.
    def _make_hash_value(self, user, timestamp):
        return (
            str(user.pk) + str(timestamp) + str(user.is_active)
        )


def is_new_version(current, new):
    current_list = current.split('.')
    new_list = new.split('.')

    if int(new_list[0]) > int(current_list[0]):
        return True
    elif int(new_list[0]) == int(current_list[0]):
        if int(new_list[1]) > int(current_list[1]):
            return True

    return False

def generate_summoner_verification_code():

    # Generate the key.
    unique_id = get_random_string(length=12)

    # Return the generate key.
    return unique_id


def generate_early_access_code():

    # Generate the key.
    unique_id = get_random_string(length=32)

    # Add the key to the database.
    AccessCode.objects.create(
        key=unique_id,
    )

    # Return the generate key.
    return unique_id


account_activation_token = TokenGenerator()
