from django.contrib.auth.views import redirect_to_login
from django.urls import reverse


class GestaoMixin:
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.is_active:
            return redirect_to_login(request.path, reverse("contas:entrar"))
        return super().dispatch(request, *args, **kwargs)
