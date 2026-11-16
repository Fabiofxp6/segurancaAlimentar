from django.urls import path

from .views import EstabelecimentoCriarView, EstabelecimentoEditarView, EstabelecimentosView


app_name = "estabelecimentos"
urlpatterns = [
    path("", EstabelecimentosView.as_view(), name="lista"),
    path("novo/", EstabelecimentoCriarView.as_view(), name="criar"),
    path("<int:pk>/", EstabelecimentoEditarView.as_view(), name="editar"),
]
