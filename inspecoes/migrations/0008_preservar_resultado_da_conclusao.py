from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [("inspecoes", "0007_conclusao_e_resultado")]

    operations = [
        migrations.RunSQL(
            sql="""
                CREATE TRIGGER inspecoes_resultado_imutavel
                    BEFORE UPDATE OR DELETE ON inspecoes_resultadoinspecao
                    FOR EACH ROW EXECUTE FUNCTION inspecoes_preservar_historico();

                CREATE FUNCTION inspecoes_proteger_conclusao() RETURNS trigger
                LANGUAGE plpgsql AS $$
                BEGIN
                    IF TG_OP = 'INSERT' THEN
                        IF NEW.estado = 'concluida' THEN
                            RAISE EXCEPTION 'A inspeção exige resultado confirmado'
                                USING ERRCODE = 'integrity_constraint_violation';
                        END IF;
                        RETURN NEW;
                    END IF;
                    IF OLD.estado = 'concluida' THEN
                        IF NEW.estado IS DISTINCT FROM OLD.estado OR
                           NEW.versao_checklist_id IS DISTINCT FROM OLD.versao_checklist_id THEN
                            RAISE EXCEPTION 'A conclusão registrada é imutável'
                                USING ERRCODE = 'integrity_constraint_violation';
                        END IF;
                    ELSIF NEW.estado = 'concluida' AND (
                        OLD.estado <> 'em_andamento'
                        OR NEW.versao_checklist_id IS DISTINCT FROM OLD.versao_checklist_id
                        OR NOT EXISTS (
                            SELECT 1 FROM inspecoes_resultadoinspecao r
                            JOIN checklists_versaochecklist v ON v.id = r.versao_checklist_id
                            WHERE r.inspecao_id = OLD.id
                              AND r.versao_checklist_id = OLD.versao_checklist_id
                              AND r.regra_pontuacao = v.regra_pontuacao
                        )
                    ) THEN
                        RAISE EXCEPTION 'A inspeção exige resultado confirmado'
                            USING ERRCODE = 'integrity_constraint_violation';
                    END IF;
                    RETURN NEW;
                END;
                $$;

                CREATE TRIGGER inspecoes_conclusao_protegida
                    BEFORE INSERT OR UPDATE ON inspecoes_inspecao
                    FOR EACH ROW EXECUTE FUNCTION inspecoes_proteger_conclusao();
            """,
            reverse_sql="""
                DROP TRIGGER inspecoes_conclusao_protegida ON inspecoes_inspecao;
                DROP FUNCTION inspecoes_proteger_conclusao();
                DROP TRIGGER inspecoes_resultado_imutavel ON inspecoes_resultadoinspecao;
            """,
        ),
    ]
