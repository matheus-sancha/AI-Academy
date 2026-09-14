/* =====================================================================
   10_provision_learner.sql — run ONCE PER LEARNER, by an admin.

   Edit the two values at the top of the block, then run the whole file.

   It creates the two roles the course is built around:

     ACADEMY_LEARNER_<tag>   owns SANDBOX_<tag>, can create and drop in it,
                             and drives its own XSMALL warehouse. This is
                             the role a learner uses in worksheets.

     ACADEMY_AGENT_<tag>     read-only on the same schema, no create
                             rights. This is the ONLY role an agent, a
                             connector or an MCP server ever uses. It is
                             what makes "the agent cannot change the data"
                             a property of the platform rather than a
                             promise in a prompt.

   Both roles are granted to the learner, so they can switch between
   building as themselves and testing as their agent sees the world.
   ===================================================================== */

USE ROLE ACCOUNTADMIN;

EXECUTE IMMEDIATE $$
DECLARE
    -- ---- edit these two -------------------------------------------------
    snowflake_user  STRING DEFAULT 'CHANGE_ME';   -- the learner login, e.g. 'ANA.DUARTE'
    tag             STRING DEFAULT 'CHANGE_ME';   -- identifier suffix, letters digits and _, e.g. 'ADUARTE'
    credit_quota    STRING DEFAULT '5';           -- monthly credits before the warehouse suspends
    -- ---------------------------------------------------------------------
    learner_role    STRING;
    agent_role      STRING;
    warehouse       STRING;
    monitor         STRING;
    sandbox         STRING;
BEGIN
    tag := UPPER(TRIM(tag));
    IF (tag = 'CHANGE_ME' OR tag IS NULL OR tag = '') THEN
        RETURN 'Set snowflake_user and tag at the top of the block before running it.';
    END IF;
    IF (NOT REGEXP_LIKE(tag, '[A-Z][A-Z0-9_]*')) THEN
        RETURN 'tag must start with a letter and contain only letters, digits and underscores. Got "' || tag || '".';
    END IF;

    learner_role := 'ACADEMY_LEARNER_' || tag;
    agent_role   := 'ACADEMY_AGENT_'   || tag;
    warehouse    := 'ACADEMY_WH_'      || tag;
    monitor      := 'ACADEMY_RM_'      || tag;
    sandbox      := 'AI_ACADEMY.SANDBOX_' || tag;

    -- Roles -------------------------------------------------------------
    EXECUTE IMMEDIATE 'CREATE ROLE IF NOT EXISTS ' || learner_role
        || ' COMMENT = ''Owns the AI-Academy sandbox for ' || tag || '.''';
    EXECUTE IMMEDIATE 'CREATE ROLE IF NOT EXISTS ' || agent_role
        || ' COMMENT = ''Read-only role for agents, connectors and MCP servers belonging to ' || tag || '. Never used for authoring.''';
    EXECUTE IMMEDIATE 'GRANT ROLE ' || learner_role || ' TO USER "' || snowflake_user || '"';
    EXECUTE IMMEDIATE 'GRANT ROLE ' || agent_role   || ' TO USER "' || snowflake_user || '"';
    EXECUTE IMMEDIATE 'GRANT ROLE ' || learner_role || ' TO ROLE ACADEMY_ADMIN';
    EXECUTE IMMEDIATE 'GRANT ROLE ' || agent_role   || ' TO ROLE ACADEMY_ADMIN';

    -- Warehouse with a spending cap --------------------------------------
    EXECUTE IMMEDIATE 'CREATE RESOURCE MONITOR IF NOT EXISTS ' || monitor
        || ' WITH CREDIT_QUOTA = ' || credit_quota || ' FREQUENCY = MONTHLY START_TIMESTAMP = IMMEDIATELY'
        || ' TRIGGERS ON 80 PERCENT DO NOTIFY'
        || '          ON 100 PERCENT DO SUSPEND'
        || '          ON 110 PERCENT DO SUSPEND_IMMEDIATE';
    EXECUTE IMMEDIATE 'CREATE WAREHOUSE IF NOT EXISTS ' || warehouse
        || ' WAREHOUSE_SIZE = ''XSMALL'' AUTO_SUSPEND = 60 AUTO_RESUME = TRUE INITIALLY_SUSPENDED = TRUE'
        || ' COMMENT = ''AI-Academy labs for ' || tag || '.''';
    EXECUTE IMMEDIATE 'ALTER WAREHOUSE ' || warehouse || ' SET RESOURCE_MONITOR = ' || monitor;
    EXECUTE IMMEDIATE 'GRANT USAGE, OPERATE ON WAREHOUSE ' || warehouse || ' TO ROLE ' || learner_role;
    EXECUTE IMMEDIATE 'GRANT USAGE ON WAREHOUSE ' || warehouse || ' TO ROLE ' || agent_role;

    -- Read access to the golden data and the shared procedures ------------
    EXECUTE IMMEDIATE 'GRANT USAGE ON DATABASE AI_ACADEMY TO ROLE ' || learner_role;
    EXECUTE IMMEDIATE 'GRANT USAGE ON DATABASE AI_ACADEMY TO ROLE ' || agent_role;
    EXECUTE IMMEDIATE 'GRANT USAGE ON SCHEMA AI_ACADEMY.SEED TO ROLE ' || learner_role;
    EXECUTE IMMEDIATE 'GRANT SELECT ON ALL TABLES IN SCHEMA AI_ACADEMY.SEED TO ROLE ' || learner_role;
    EXECUTE IMMEDIATE 'GRANT SELECT ON FUTURE TABLES IN SCHEMA AI_ACADEMY.SEED TO ROLE ' || learner_role;
    EXECUTE IMMEDIATE 'GRANT USAGE ON SCHEMA AI_ACADEMY.SHARED TO ROLE ' || learner_role;
    EXECUTE IMMEDIATE 'GRANT USAGE ON ALL PROCEDURES IN SCHEMA AI_ACADEMY.SHARED TO ROLE ' || learner_role;
    EXECUTE IMMEDIATE 'GRANT USAGE ON FUTURE PROCEDURES IN SCHEMA AI_ACADEMY.SHARED TO ROLE ' || learner_role;

    -- The sandbox ---------------------------------------------------------
    EXECUTE IMMEDIATE 'CREATE SCHEMA IF NOT EXISTS ' || sandbox
        || ' COMMENT = ''Personal AI-Academy sandbox for ' || tag || '. Rebuilt by AI_ACADEMY.SHARED.RESET_TO().''';
    EXECUTE IMMEDIATE 'GRANT USAGE ON SCHEMA ' || sandbox || ' TO ROLE ' || agent_role;
    EXECUTE IMMEDIATE 'GRANT SELECT ON ALL TABLES  IN SCHEMA ' || sandbox || ' TO ROLE ' || agent_role;
    EXECUTE IMMEDIATE 'GRANT SELECT ON FUTURE TABLES IN SCHEMA ' || sandbox || ' TO ROLE ' || agent_role;
    EXECUTE IMMEDIATE 'GRANT SELECT ON ALL VIEWS   IN SCHEMA ' || sandbox || ' TO ROLE ' || agent_role;
    EXECUTE IMMEDIATE 'GRANT SELECT ON FUTURE VIEWS IN SCHEMA ' || sandbox || ' TO ROLE ' || agent_role;
    -- Ownership last, so the grants above survive the transfer.
    EXECUTE IMMEDIATE 'GRANT OWNERSHIP ON SCHEMA ' || sandbox || ' TO ROLE ' || learner_role || ' COPY CURRENT GRANTS';

    RETURN 'Provisioned ' || tag || ': roles ' || learner_role || ' and ' || agent_role
        || ', warehouse ' || warehouse || ' capped by ' || monitor || ', schema ' || sandbox
        || '. The learner runs 20_learner_start_here.sql next.';

EXCEPTION
    WHEN OTHER THEN
        RETURN 'Provisioning failed: ' || SQLERRM;
END;
$$;
