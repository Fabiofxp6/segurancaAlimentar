from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [("inspecoes", "0009_termo_e_liberacao")]

    operations = [
        migrations.RunSQL(
            sql="""
                CREATE TRIGGER inspecoes_termo_imutavel
                    BEFORE UPDATE OR DELETE ON inspecoes_termoinspecao
                    FOR EACH ROW EXECUTE FUNCTION inspecoes_preservar_historico();

                CREATE TRIGGER inspecoes_liberacao_imutavel
                    BEFORE UPDATE OR DELETE ON inspecoes_liberacaotermo
                    FOR EACH ROW EXECUTE FUNCTION inspecoes_preservar_historico();
            """,
            reverse_sql="""
                DROP TRIGGER inspecoes_liberacao_imutavel ON inspecoes_liberacaotermo;
                DROP TRIGGER inspecoes_termo_imutavel ON inspecoes_termoinspecao;
            """,
        ),
    ]
