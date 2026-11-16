from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [("inspecoes", "0011_revisoes_e_correcoes")]

    operations = [
        migrations.RunSQL(
            sql="""
                CREATE TRIGGER inspecoes_pedido_correcao_imutavel
                    BEFORE UPDATE OR DELETE ON inspecoes_pedidocorrecao
                    FOR EACH ROW EXECUTE FUNCTION inspecoes_preservar_historico();

                CREATE TRIGGER inspecoes_decisao_correcao_imutavel
                    BEFORE UPDATE OR DELETE ON inspecoes_decisaocorrecao
                    FOR EACH ROW EXECUTE FUNCTION inspecoes_preservar_historico();

                CREATE FUNCTION inspecoes_proteger_revisao_corrigida() RETURNS trigger
                LANGUAGE plpgsql AS $$
                BEGIN
                    IF NEW.revisao > 1 AND NOT EXISTS (
                        SELECT 1
                        FROM inspecoes_pedidocorrecao p
                        JOIN inspecoes_decisaocorrecao d ON d.pedido_id = p.id
                        JOIN inspecoes_resultadoinspecao b ON b.id = p.base_id
                        WHERE p.id = NEW.correcao_id
                          AND d.aprovada
                          AND d.autor_id <> p.solicitante_id
                          AND b.inspecao_id = NEW.inspecao_id
                          AND b.revisao + 1 = NEW.revisao
                          AND b.versao_checklist_id = NEW.versao_checklist_id
                          AND b.regra_pontuacao = NEW.regra_pontuacao
                          AND (NEW.respostas_utilizadas -> p.item_id::text) - 'revisao' = p.proposto
                    ) THEN
                        RAISE EXCEPTION 'A revisão exige correção aprovada e escopo correspondente'
                            USING ERRCODE = 'integrity_constraint_violation';
                    END IF;
                    RETURN NEW;
                END;
                $$;

                CREATE TRIGGER inspecoes_revisao_corrigida_protegida
                    BEFORE INSERT ON inspecoes_resultadoinspecao
                    FOR EACH ROW EXECUTE FUNCTION inspecoes_proteger_revisao_corrigida();
            """,
            reverse_sql="""
                DROP TRIGGER inspecoes_revisao_corrigida_protegida ON inspecoes_resultadoinspecao;
                DROP FUNCTION inspecoes_proteger_revisao_corrigida();
                DROP TRIGGER inspecoes_decisao_correcao_imutavel ON inspecoes_decisaocorrecao;
                DROP TRIGGER inspecoes_pedido_correcao_imutavel ON inspecoes_pedidocorrecao;
            """,
        ),
    ]
