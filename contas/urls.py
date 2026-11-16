from django.urls import path

from .views import AcessoView, EntrarView, MeuEstabelecimentoView, SairView


app_name = "contas"
urlpatterns = [
    path("entrar/", EntrarView.as_view(), name="entrar"),
    path("sair/", SairView.as_view(), name="sair"),
    path("acesso/", AcessoView.as_view(), name="acesso"),
    path("estabelecimento/<int:pk>/", MeuEstabelecimentoView.as_view(), name="estabelecimento"),
]
