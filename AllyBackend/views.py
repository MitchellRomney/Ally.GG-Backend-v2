from Website.functions.general import account_activation_token
from Website.models import Profile
from django.contrib.auth.models import User
from django.shortcuts import redirect


def activate(request, username, token):
    try:
        # Get the relevant user.
        user = User.objects.get(username=username)

    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):

        # Confirm email on the Profile.
        profile = Profile.objects.get(user=user)
        profile.email_confirmed = True
        profile.save()

        return redirect('https://www.ally.gg/?email_confirmed=true')

