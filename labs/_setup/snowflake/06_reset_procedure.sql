/* =====================================================================
   06_reset_procedure.sql — AI_ACADEMY.SHARED.RESET_TO(<module>)

   Run as ACADEMY_ADMIN after 05_seed_metadata.sql.

   Every lab starts with step 0:

       USE ROLE ACADEMY_LEARNER_<user>;
       CALL AI_ACADEMY.SHARED.RESET_TO('B7');

   That puts the learner sandbox back to the start state for that module,
   whatever they did in the previous one. The procedure:

     1. drops every view and every non-seed table in the sandbox;
     2. zero-copy clones the seed tables into it (instant, no storage);
     3. re-anchors all dates so the data still looks current;
     4. runs any extra start-state statements for the module;
     5. re-grants read access to the learner agent role.

   It runs EXECUTE AS CALLER and derives the sandbox from the caller's
   role, so a learner can only ever reset their own schema.
   ===================================================================== */

USE ROLE ACADEMY_ADMIN;
USE WAREHOUSE ACADEMY_ADMIN_WH;
USE SCHEMA AI_ACADEMY.SHARED;

CREATE OR REPLACE PROCEDURE AI_ACADEMY.SHARED.RESET_TO(MODULE_ID STRING)
RETURNS STRING
LANGUAGE SQL
EXECUTE AS CALLER
COMMENT = 'Reset the caller sandbox to the start state of a module, for example CALL RESET_TO(''B7'').'
AS
$$
DECLARE
    role_name    STRING;
    learner      STRING;
    schema_name  STRING;
    sandbox      STRING;
    module_up    STRING;
    known        INTEGER;
    shift_days   INTEGER;
    n_tables     INTEGER DEFAULT 0;
    n_dropped    INTEGER DEFAULT 0;
    n_steps      INTEGER DEFAULT 0;
    stmt         STRING DEFAULT '(no statement yet)';
BEGIN
    -- Who is calling, and which sandbox is theirs.
    role_name := CURRENT_ROLE();
    IF (LEFT(role_name, 16) <> 'ACADEMY_LEARNER_') THEN
        RETURN 'Run "USE ROLE ACADEMY_LEARNER_<user>;" first. The current role is ' || role_name || '.';
    END IF;
    learner     := SUBSTR(role_name, 17);
    schema_name := 'SANDBOX_' || learner;
    sandbox     := 'AI_ACADEMY.' || schema_name;

    -- Reject an unknown module rather than silently resetting to the seed.
    module_up := UPPER(TRIM(MODULE_ID));
    SELECT COUNT(*) INTO :known FROM AI_ACADEMY.SEED.MODULES m WHERE m.MODULE = :module_up;
    IF (known = 0) THEN
        RETURN 'Unknown module "' || module_up ||
               '". Run SELECT * FROM AI_ACADEMY.SEED.MODULES ORDER BY MODULE; to see the list.';
    END IF;

    -- 1a. Drop every view in the sandbox.
    LET rs_views RESULTSET := (EXECUTE IMMEDIATE
        'SELECT TABLE_NAME AS N FROM AI_ACADEMY.INFORMATION_SCHEMA.VIEWS WHERE TABLE_SCHEMA = ''' || schema_name || '''');
    LET c_views CURSOR FOR rs_views;
    FOR r IN c_views DO
        stmt := 'DROP VIEW IF EXISTS ' || sandbox || '.' || r.N;
        EXECUTE IMMEDIATE :stmt;
        n_dropped := n_dropped + 1;
    END FOR;

    -- 1b. Drop tables the learner added that are not part of the seed.
    LET rs_extra RESULTSET := (EXECUTE IMMEDIATE
        'SELECT t.TABLE_NAME AS N FROM AI_ACADEMY.INFORMATION_SCHEMA.TABLES t '
        || 'WHERE t.TABLE_SCHEMA = ''' || schema_name || ''' AND t.TABLE_TYPE = ''BASE TABLE'' '
        || 'AND t.TABLE_NAME NOT IN (SELECT s.TABLE_NAME FROM AI_ACADEMY.SEED.SEED_TABLES s)');
    LET c_extra CURSOR FOR rs_extra;
    FOR r IN c_extra DO
        stmt := 'DROP TABLE IF EXISTS ' || sandbox || '.' || r.N;
        EXECUTE IMMEDIATE :stmt;
        n_dropped := n_dropped + 1;
    END FOR;

    -- 2. Clone the seed tables. A clone shares storage, so this is instant and free.
    LET rs_tables RESULTSET := (SELECT s.TABLE_NAME AS N FROM AI_ACADEMY.SEED.SEED_TABLES s ORDER BY s.LOAD_ORDER);
    LET c_tables CURSOR FOR rs_tables;
    FOR r IN c_tables DO
        stmt := 'CREATE OR REPLACE TABLE ' || sandbox || '.' || r.N || ' CLONE AI_ACADEMY.SEED.' || r.N;
        EXECUTE IMMEDIATE :stmt;
        n_tables := n_tables + 1;
    END FOR;

    -- 3. Re-anchor dates on the month the learner is actually working in.
    SELECT DATEDIFF('day', m.ANCHOR_DATE, DATE_TRUNC('MONTH', CURRENT_DATE()))
      INTO :shift_days
      FROM AI_ACADEMY.SEED.SEED_META m;
    IF (shift_days <> 0) THEN
        LET rs_dates RESULTSET := (SELECT d.TABLE_NAME AS T, d.COLUMN_NAME AS C FROM AI_ACADEMY.SEED.SEED_DATE_COLUMNS d);
        LET c_dates CURSOR FOR rs_dates;
        FOR r IN c_dates DO
            stmt := 'UPDATE ' || sandbox || '.' || r.T
                 || ' SET ' || r.C || ' = DATEADD(day, ' || TO_VARCHAR(shift_days) || ', ' || r.C || ')'
                 || ' WHERE ' || r.C || ' IS NOT NULL';
            EXECUTE IMMEDIATE :stmt;
        END FOR;
    END IF;

    -- 4. Anything this module needs beyond the seed tables.
    LET rs_pre RESULTSET := (EXECUTE IMMEDIATE
        'SELECT p.STATEMENT AS S FROM AI_ACADEMY.SEED.MODULE_PREREQS p '
        || 'WHERE p.MODULE = ''' || module_up || ''' ORDER BY p.STEP_NO');
    LET c_pre CURSOR FOR rs_pre;
    FOR r IN c_pre DO
        stmt := REPLACE(r.S, '{{SANDBOX}}', sandbox);
        EXECUTE IMMEDIATE :stmt;
        n_steps := n_steps + 1;
    END FOR;

    -- 5. The clones are new objects, so make sure the agent role can still read them.
    stmt := 'GRANT SELECT ON ALL TABLES IN SCHEMA ' || sandbox || ' TO ROLE ACADEMY_AGENT_' || learner;
    EXECUTE IMMEDIATE :stmt;

    RETURN sandbox || ' is at the start state for ' || module_up || '. '
        || TO_VARCHAR(n_tables) || ' tables restored, '
        || TO_VARCHAR(n_dropped) || ' objects removed, '
        || TO_VARCHAR(n_steps) || ' module steps applied, dates shifted by '
        || TO_VARCHAR(shift_days) || ' days.';

EXCEPTION
    WHEN OTHER THEN
        RETURN 'RESET_TO failed while running: ' || stmt || CHR(10) || 'Snowflake said: ' || SQLERRM;
END;
$$;

SELECT 'RESET_TO created. Next: 10_provision_learner.sql, once per learner.' AS STATUS;
