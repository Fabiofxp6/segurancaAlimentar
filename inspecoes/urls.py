from django.urls import path

from .cancelamento_views import (
    AuditoriaInspecaoView, CancelamentoConexaoView, CancelamentoView, DecidirCancelamentoView,
    PedidosCancelamentoView, SolicitarCancelamentoView,
)
from .campo_views import (
    CampoAnexarView, CampoBaixarView, CampoConexaoView, CampoItemView, CampoListaView, CampoResponderView,
)
from .conclusao_views import ConcluirView, ConclusaoConexaoView, ConclusaoView
from .documentos_views import (
    DocumentosBaixarView, DocumentosConexaoView, DocumentosEnviarView, DocumentosInspecaoView, DocumentosListaView,
)
from .views import (
    AtribuirView, EquipeView, InicioDiretoView, InicioView, InspecaoView, InspecoesView, SupervisaoView,
)


app_name = "inspecoes"
urlpatterns = [
    path("", InspecoesView.as_view(), name="lista"),
    path("atribuir/", AtribuirView.as_view(), name="atribuir"),
    path("documentos/", DocumentosListaView.as_view(), name="documentos"),
    path("<int:pk>/documentos/", DocumentosInspecaoView.as_view(), name="documentos_inspecao"),
    path("<int:pk>/documentos/conexao/", DocumentosConexaoView.as_view(), name="documentos_conexao"),
    path("<int:pk>/documentos/enviar/", DocumentosEnviarView.as_view(), name="documentos_enviar"),
    path("<int:pk>/documentos/<int:documento_id>/", DocumentosBaixarView.as_view(), name="documentos_baixar"),
    path("iniciar/", InicioDiretoView.as_view(), name="inicio_direto"),
    path("<int:pk>/", InspecaoView.as_view(), name="detalhe"),
    path("<int:pk>/iniciar/", InicioView.as_view(), name="inicio"),
    path("<int:pk>/equipe/", EquipeView.as_view(), name="equipe"),
    path("cancelamentos/", PedidosCancelamentoView.as_view(), name="cancelamentos"),
    path("<int:pk>/cancelamento/", CancelamentoView.as_view(), name="cancelamento"),
    path("<int:pk>/cancelamento/conexao/", CancelamentoConexaoView.as_view(), name="cancelamento_conexao"),
    path("<int:pk>/cancelamento/solicitar/", SolicitarCancelamentoView.as_view(), name="cancelamento_solicitar"),
    path("<int:pk>/cancelamento/<int:pedido_id>/decidir/", DecidirCancelamentoView.as_view(), name="cancelamento_decidir"),
    path("<int:pk>/conclusao/", ConclusaoView.as_view(), name="conclusao"),
    path("<int:pk>/conclusao/confirmar/", ConcluirView.as_view(), name="conclusao_confirmar"),
    path("<int:pk>/conclusao/conexao/", ConclusaoConexaoView.as_view(), name="conclusao_conexao"),
    path("<int:pk>/auditoria/", AuditoriaInspecaoView.as_view(), name="auditoria"),
    path("<int:pk>/campo/", CampoListaView.as_view(), name="campo"),
    path("<int:pk>/campo/<uuid:item_id>/", CampoItemView.as_view(), name="campo_item"),
    path("<int:pk>/campo/<uuid:item_id>/conexao/", CampoConexaoView.as_view(), name="campo_conexao"),
    path("<int:pk>/campo/<uuid:item_id>/resposta/", CampoResponderView.as_view(), name="campo_responder"),
    path("<int:pk>/campo/<uuid:item_id>/evidencias/", CampoAnexarView.as_view(), name="campo_anexar"),
    path("<int:pk>/campo/<uuid:item_id>/evidencias/<int:evidencia_id>/", CampoBaixarView.as_view(), name="campo_baixar"),
    path("acoes/<int:pk>/supervisao/", SupervisaoView.as_view(), name="supervisao"),
]
