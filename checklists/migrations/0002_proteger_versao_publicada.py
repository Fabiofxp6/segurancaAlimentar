from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [("checklists", "0001_initial")]

    operations = [
        migrations.RunSQL(
            sql="""
                CREATE FUNCTION checklists_proteger_versao_publicada() RETURNS trigger
                LANGUAGE plpgsql AS $$
                BEGIN
                    RAISE EXCEPTION 'Versão publicada de checklist é imutável'
                        USING ERRCODE = 'integrity_constraint_violation';
                END;
                $$;

                CREATE TRIGGER checklists_versao_publicada_imutavel
                    BEFORE UPDATE OR DELETE ON checklists_versaochecklist
                    FOR EACH ROW EXECUTE FUNCTION checklists_proteger_versao_publicada();
            """,
            reverse_sql="""
                DROP TRIGGER checklists_versao_publicada_imutavel ON checklists_versaochecklist;
                DROP FUNCTION checklists_proteger_versao_publicada();
            """,
        ),
    ]
