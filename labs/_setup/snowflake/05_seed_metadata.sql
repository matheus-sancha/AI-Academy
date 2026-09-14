/* =====================================================================
   05_seed_metadata.sql — the metadata RESET_TO() drives itself from.

   Run as ACADEMY_ADMIN after 04_seed_quality_fat.sql.

     SEED_META          the anchor date this seed was built against
     SEED_TABLES        which tables a sandbox is rebuilt from, in order
     SEED_DATE_COLUMNS  every DATE column, so dates can be re-anchored
     MODULES            the module ids RESET_TO() accepts
     MODULE_PREREQS     extra statements to run for a given module

   Re-run this file whenever a table or column is added to the seed.
   ===================================================================== */

USE ROLE ACADEMY_ADMIN;
USE WAREHOUSE ACADEMY_ADMIN_WH;
USE SCHEMA AI_ACADEMY.SEED;

/* ------------------------------------------------------------------
   The anchor. Every date in the seed is a whole number of days from it.
   RESET_TO() shifts a sandbox by the difference between this date and
   the first day of the month the learner runs the reset, so the data
   always looks current no matter how old the seed is.
   ------------------------------------------------------------------ */
CREATE OR REPLACE TABLE SEED_META (
    ANCHOR_DATE  DATE    COMMENT 'First day of the month this seed was loaded.',
    SEEDED_AT    TIMESTAMP_NTZ COMMENT 'When the seed was loaded.'
) COMMENT = 'One row. Read by RESET_TO() to re-anchor dates in a sandbox.';

INSERT INTO SEED_META (ANCHOR_DATE, SEEDED_AT)
SELECT DATE_TRUNC('MONTH', CURRENT_DATE()), CURRENT_TIMESTAMP()::TIMESTAMP_NTZ;

/* ------------------------------------------------------------------
   The data tables, in the order a sandbox is rebuilt.
   ------------------------------------------------------------------ */
CREATE OR REPLACE TABLE SEED_TABLES (
    TABLE_NAME  STRING   COMMENT 'Table cloned into each sandbox.',
    LOAD_ORDER  NUMBER   COMMENT 'Clone order. Parents before children, for readability only.'
) COMMENT = 'The tables RESET_TO() rebuilds. Add a row when a table is added to the seed.';

INSERT INTO SEED_TABLES (TABLE_NAME, LOAD_ORDER) VALUES
  ('SAP_PROJECTS',              10),
  ('SAP_UNITS',                 20),
  ('SAP_BOM_LINES',             30),
  ('SAP_WORK_ORDERS',           40),
  ('SAP_WO_OPERATIONS',         50),
  ('SAP_QUALITY_NOTIFICATIONS', 60),
  ('TC_PARTS',                  70),
  ('TC_DRAWINGS',               80),
  ('TC_CNC_PROGRAMS',           90),
  ('TC_DOCUMENTS',             100),
  ('TC_ECNS',                  110),
  ('TC_ECN_AFFECTED_ITEMS',    120),
  ('FAT_RESULTS',              130);

/* ------------------------------------------------------------------
   Every DATE column in those tables, read straight from the catalogue
   so it can never drift from the DDL.
   ------------------------------------------------------------------ */
CREATE OR REPLACE TABLE SEED_DATE_COLUMNS AS
SELECT c.TABLE_NAME, c.COLUMN_NAME
FROM AI_ACADEMY.INFORMATION_SCHEMA.COLUMNS c
JOIN AI_ACADEMY.SEED.SEED_TABLES t ON t.TABLE_NAME = c.TABLE_NAME
WHERE c.TABLE_SCHEMA = 'SEED'
  AND c.DATA_TYPE = 'DATE'
ORDER BY c.TABLE_NAME, c.ORDINAL_POSITION;

COMMENT ON TABLE SEED_DATE_COLUMNS IS
  'Date columns RESET_TO() re-anchors. Rebuilt by 05_seed_metadata.sql from the catalogue.';

/* ------------------------------------------------------------------
   Modules a learner may reset to.
   ------------------------------------------------------------------ */
CREATE OR REPLACE TABLE MODULES (
    MODULE  STRING   COMMENT 'Roadmap section id, or BASE for the untouched seed.',
    TITLE   STRING   COMMENT 'Module title as it appears in the roadmap.'
) COMMENT = 'Valid arguments for RESET_TO(). Reject anything else so a typo is not silently ignored.';

INSERT INTO MODULES (MODULE, TITLE) VALUES
  ('BASE','Seed data with no module state'),
  ('B5', 'Copilot Studio Basics'),
  ('B6', 'Knowledge and RAG'),
  ('B7', 'Tools, Connectors and MCP'),
  ('B8', 'Skills'),
  ('B9', 'Workflows and Power Automate with AI Builder'),
  ('B10','Data: SQL in Snowflake'),
  ('B11','Safety, Moderation and Responsible AI'),
  ('B12','Environments and Publishing'),
  ('B13','Testing and Evaluation Basics'),
  ('A2', 'Context Engineering'),
  ('A4', 'Agent Skills'),
  ('A5', 'MCP'),
  ('A6', 'Multi-Agent'),
  ('A7', 'Pro-Code Agents'),
  ('A8', 'Advanced RAG'),
  ('A9', 'Snowflake and Cortex'),
  ('A10','Intelligent Automation'),
  ('A12','Evaluation'),
  ('A13','Security'),
  ('A14','ALM and Operations');

/* ------------------------------------------------------------------
   Extra statements per module.

   A module needs a row here only when its start state is more than the
   seed tables -- for example a view an earlier module built that this
   module assumes. {{SANDBOX}} is replaced with the fully qualified
   sandbox schema before the statement runs. Statements run in STEP_NO
   order, after the tables are cloned and re-anchored.

   Example (do not uncomment; it is only the shape of a row):
     INSERT INTO MODULE_PREREQS VALUES ('A9', 10,
       'CREATE OR REPLACE VIEW {{SANDBOX}}.V_WORK_ORDER_STATUS AS SELECT ...');

   Nothing is needed yet: every module written so far starts from the
   seed tables alone.
   ------------------------------------------------------------------ */
CREATE OR REPLACE TABLE MODULE_PREREQS (
    MODULE     STRING  COMMENT 'Module the statement belongs to. Joins MODULES.',
    STEP_NO    NUMBER  COMMENT 'Execution order within the module.',
    STATEMENT  STRING  COMMENT 'SQL to run. {{SANDBOX}} is replaced with the sandbox schema.'
) COMMENT = 'Module start state beyond the seed tables. Empty means the seed tables are the start state.';

SELECT 'Metadata seeded. Next: 06_reset_procedure.sql' AS STATUS;
