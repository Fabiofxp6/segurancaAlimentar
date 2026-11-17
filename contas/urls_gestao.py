from django.urls import path

from .views_gestao import UsuarioCriarView, UsuarioEditarView, UsuarioSenhaView, UsuariosView, VinculoView


app_name = "gestao_contas"
urlpatterns = [
    path("", UsuariosView.as_view(), name="lista"),
    path("novo/", UsuarioCriarView.as_view(), name="criar"),
    path("<int:pk>/", UsuarioEditarView.as_view(), name="editar"),
    path("<int:pk>/senha/", UsuarioSenhaView.as_view(), name="senha"),
    path("<int:pk>/vinculo/", VinculoView.as_view(), name="vinculo"),
]
