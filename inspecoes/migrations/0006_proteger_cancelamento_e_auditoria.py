from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [("inspecoes", "0005_cancelamento_e_auditoria")]

    operations = [
        migrations.RunSQL(
            sql="""
                CREATE FUNCTION inspecoes_preservar_historico() RETURNS trigger
                LANGUAGE plpgsql AS $$
                BEGIN
                    RAISE EXCEPTION 'O registro de auditoria é imutável'
                        USING ERRCODE = 'integrity_constraint_violation';
                END;
                $$;

                CREATE TRIGGER inspecoes_historico_imutavel
                    BEFORE UPDATE OR DELETE ON inspecoes_historicoinspecao
                    FOR EACH ROW EXECUTE FUNCTION inspecoes_preservar_historico();

                CREATE TRIGGER inspecoes_confirmacao_imutavel
                    BEFORE UPDATE OR DELETE ON inspecoes_operacaocampo
                    FOR EACH ROW EXECUTE FUNCTION inspecoes_preservar_historico();

                CREATE FUNCTION inspecoes_proteger_cancelamento() RETURNS trigger
                LANGUAGE plpgsql AS $$
                BEGIN
                    IF TG_OP = 'INSERT' THEN
                        IF NEW.estado = 'cancelada' THEN
                            RAISE EXCEPTION 'A inspeção exige cancelamento efetivado'
                                USING ERRCODE = 'integrity_constraint_violation';
                        END IF;
                        RETURN NEW;
                    END IF;
                    IF OLD.estado = 'cancelada' AND (
                        NEW.estado IS DISTINCT FROM OLD.estado OR
                        NEW.cancelada_em IS DISTINCT FROM OLD.cancelada_em
                    ) THEN
                        RAISE EXCEPTION 'O cancelamento efetivado é imutável'
                            USING ERRCODE = 'integrity_constraint_violation';
                    END IF;
                    IF NEW.estado = 'cancelada' AND OLD.estado <> 'cancelada' AND (
                        OLD.estado <> 'em_andamento' OR NOT EXISTS (
                            SELECT 1 FROM inspecoes_pedidocancelamento
                            WHERE inspecao_id = OLD.id AND situacao = 'efetivado'
                              AND efetivada_em = NEW.cancelada_em
                        )
                    ) THEN
                        RAISE EXCEPTION 'A inspeção exige cancelamento efetivado'
                            USING ERRCODE = 'integrity_constraint_violation';
                    END IF;
                    RETURN NEW;
                END;
                $$;

                CREATE FUNCTION inspecoes_proteger_pedido() RETURNS trigger
                LANGUAGE plpgsql AS $$
                BEGIN
                    IF TG_OP = 'INSERT' AND NEW.situacao = 'pendente' THEN
                        RETURN NEW;
                    END IF;
                    IF TG_OP = 'UPDATE' AND ROW(
                        NEW.inspecao_id, NEW.solicitante_id, NEW.justificativa, NEW.solicitada_em,
                        NEW.operacao_solicitacao
                    ) IS NOT DISTINCT FROM ROW(
                        OLD.inspecao_id, OLD.solicitante_id, OLD.justificativa, OLD.solicitada_em,
                        OLD.operacao_solicitacao
                    ) THEN
                        IF OLD.situacao = 'pendente' AND NEW.situacao IN ('aprovado', 'rejeitado') THEN
                            RETURN NEW;
                        END IF;
                        IF OLD.situacao = 'aprovado' AND NEW.situacao = 'efetivado' AND ROW(
                            NEW.decidido_por_id, NEW.decidida_em, NEW.motivo_decisao,
                            NEW.operacao_decisao, NEW.designacao_id
                        ) IS NOT DISTINCT FROM ROW(
                            OLD.decidido_por_id, OLD.decidida_em, OLD.motivo_decisao,
                            OLD.operacao_decisao, OLD.designacao_id
                        ) THEN
                            RETURN NEW;
                        END IF;
                    END IF;
                    RAISE EXCEPTION 'A transição do pedido de cancelamento é inválida'
                        USING ERRCODE = 'integrity_constraint_violation';
                END;
                $$;

                CREATE TRIGGER inspecoes_pedido_cancelamento_protegido
                    BEFORE INSERT OR UPDATE OR DELETE ON inspecoes_pedidocancelamento
                    FOR EACH ROW EXECUTE FUNCTION inspecoes_proteger_pedido();

                CREATE TRIGGER inspecoes_cancelamento_protegido
                    BEFORE INSERT OR UPDATE ON inspecoes_inspecao
                    FOR EACH ROW EXECUTE FUNCTION inspecoes_proteger_cancelamento();
            """,
            reverse_sql="""
                DROP TRIGGER inspecoes_pedido_cancelamento_protegido ON inspecoes_pedidocancelamento;
                DROP FUNCTION inspecoes_proteger_pedido();
                DROP TRIGGER inspecoes_cancelamento_protegido ON inspecoes_inspecao;
                DROP FUNCTION inspecoes_proteger_cancelamento();
                DROP TRIGGER inspecoes_confirmacao_imutavel ON inspecoes_operacaocampo;
                DROP TRIGGER inspecoes_historico_imutavel ON inspecoes_historicoinspecao;
                DROP FUNCTION inspecoes_preservar_historico();
            """,
        ),
    ]
