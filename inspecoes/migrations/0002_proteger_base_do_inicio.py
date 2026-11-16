from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [("inspecoes", "0001_initial")]

    operations = [
        migrations.RunSQL(
            sql="""
                CREATE FUNCTION inspecoes_proteger_base_do_inicio() RETURNS trigger
                LANGUAGE plpgsql AS $$
                BEGIN
                    IF OLD.versao_checklist_id IS NOT NULL AND (
                        NEW.versao_checklist_id IS DISTINCT FROM OLD.versao_checklist_id OR
                        NEW.iniciada_em IS DISTINCT FROM OLD.iniciada_em OR
                        NEW.iniciada_por_id IS DISTINCT FROM OLD.iniciada_por_id OR
                        NEW.identificacao_estabelecimento IS DISTINCT FROM OLD.identificacao_estabelecimento OR
                        NEW.estabelecimento_id IS DISTINCT FROM OLD.estabelecimento_id OR
                        NEW.acao_id IS DISTINCT FROM OLD.acao_id
                    ) THEN
                        RAISE EXCEPTION 'A base original da inspeção é imutável'
                            USING ERRCODE = 'integrity_constraint_violation';
                    END IF;
                    RETURN NEW;
                END;
                $$;

                CREATE TRIGGER inspecoes_base_do_inicio_imutavel
                    BEFORE UPDATE ON inspecoes_inspecao
                    FOR EACH ROW EXECUTE FUNCTION inspecoes_proteger_base_do_inicio();
            """,
            reverse_sql="""
                DROP TRIGGER inspecoes_base_do_inicio_imutavel ON inspecoes_inspecao;
                DROP FUNCTION inspecoes_proteger_base_do_inicio();
            """,
        ),
    ]
