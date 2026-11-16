from django.urls import path

from .views import (
    ChecklistCriarView, ChecklistPublicarView, ChecklistsView, ChecklistVersaoView,
    ItemRemoverView, ItemView, RascunhoView,
)


app_name = "checklists"
urlpatterns = [
    path("", ChecklistsView.as_view(), name="lista"),
    path("novo/", ChecklistCriarView.as_view(), name="criar"),
    path("<int:pk>/", RascunhoView.as_view(), name="rascunho"),
    path("<int:pk>/itens/novo/", ItemView.as_view(), name="item_novo"),
    path("<int:pk>/itens/<uuid:item_id>/", ItemView.as_view(), name="item_editar"),
    path("<int:pk>/itens/<uuid:item_id>/remover/", ItemRemoverView.as_view(), name="item_remover"),
    path("<int:pk>/publicar/", ChecklistPublicarView.as_view(), name="publicar"),
    path("<int:pk>/versoes/<int:versao_pk>/", ChecklistVersaoView.as_view(), name="versao"),
]
