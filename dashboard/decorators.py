# dashboard/decorators.py
from django.contrib.auth.decorators import user_passes_test

superuser_required = user_passes_test(
    lambda u: u.is_superuser, login_url="dashboard:login"
)
