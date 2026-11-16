from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [("inspecoes", "0013_adiamento_e_reanalise")]

    operations = [
        migrations.RunSQL(
            sql="""
                CREATE FUNCTION inspecoes_preservar_pedido_adiamento() RETURNS trigger
                LANGUAGE plpgsql AS $$
                BEGIN
                    IF TG_OP = 'DELETE' OR OLD.situacao <> 'pendente' OR NEW.situacao = 'pendente'
                       OR ROW(OLD.id, OLD.inspecao_id, OLD.solicitante_id, OLD.solicitada_em, OLD.operacao_id,
                              OLD.data_proposta, OLD.justificativa)
                          IS DISTINCT FROM
                          ROW(NEW.id, NEW.inspecao_id, NEW.solicitante_id, NEW.solicitada_em, NEW.operacao_id,
                              NEW.data_proposta, NEW.justificativa)
                    THEN
                        RAISE EXCEPTION 'O pedido original de adiamento deve ser preservado'
                            USING ERRCODE = 'integrity_constraint_violation';
                    END IF;
                    RETURN NEW;
                END;
                $$;

                CREATE TRIGGER inspecoes_pedido_adiamento_protegido
                    BEFORE UPDATE OR DELETE ON inspecoes_pedidoadiamento
                    FOR EACH ROW EXECUTE FUNCTION inspecoes_preservar_pedido_adiamento();

                CREATE TRIGGER inspecoes_reanalise_imutavel
                    BEFORE UPDATE OR DELETE ON inspecoes_reanalisedocumento
                    FOR EACH ROW EXECUTE FUNCTION inspecoes_preservar_historico();
            """,
            reverse_sql="""
                DROP TRIGGER inspecoes_reanalise_imutavel ON inspecoes_reanalisedocumento;
                DROP TRIGGER inspecoes_pedido_adiamento_protegido ON inspecoes_pedidoadiamento;
                DROP FUNCTION inspecoes_preservar_pedido_adiamento();
            """,
        ),
    ]
