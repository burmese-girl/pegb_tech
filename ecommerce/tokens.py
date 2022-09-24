from django.contrib.auth.tokens import PasswordResetTokenGenerator
import six

class AccountActivationTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        # import pdb;pdb.set_trace()
        return (
            six.text_type(user.pk) + six.text_type(timestamp) +
            six.text_type(user.userprofile.email_confirmed)
        )


account_activation_token = AccountActivationTokenGenerator()