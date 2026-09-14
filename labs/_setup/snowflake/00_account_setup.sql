/* =====================================================================
   AI-Academy — Snowflake lab environment
   00_account_setup.sql — run ONCE per Snowflake account, by an admin.

   Creates the shared objects every learner sandbox is built from:

     AI_ACADEMY                 database
       .SEED                    read-only golden copy of the Technik data
       .SHARED                  RESET_TO() and other helper procedures
       .SANDBOX_<user>          one schema per learner (created in 10_provision_learner.sql)

     ACADEMY_ADMIN              role that owns the database and runs the seed
     ACADEMY_ADMIN_WH           XSMALL warehouse used only for seeding

   Run order:  00 -> 01 -> 02 -> 03 -> 04 -> 05 -> 06 -> 10 (per learner)
   All data is fictional. See _source/course/scenario.md.
   ===================================================================== */

USE ROLE ACCOUNTADMIN;

-- ---------------------------------------------------------------------
-- Admin role and warehouse
-- ---------------------------------------------------------------------
CREATE ROLE IF NOT EXISTS ACADEMY_ADMIN
    COMMENT = 'Owns the AI-Academy database and seeds the Technik training data.';
GRANT ROLE ACADEMY_ADMIN TO ROLE SYSADMIN;

CREATE WAREHOUSE IF NOT EXISTS ACADEMY_ADMIN_WH
    WAREHOUSE_SIZE      = 'XSMALL'
    AUTO_SUSPEND        = 60
    AUTO_RESUME         = TRUE
    INITIALLY_SUSPENDED = TRUE
    COMMENT = 'Seeding and maintenance only. Learners use their own ACADEMY_WH_<user>.';
GRANT USAGE, OPERATE ON WAREHOUSE ACADEMY_ADMIN_WH TO ROLE ACADEMY_ADMIN;

-- ---------------------------------------------------------------------
-- Database and schemas
-- ---------------------------------------------------------------------
CREATE DATABASE IF NOT EXISTS AI_ACADEMY
    COMMENT = 'AI Engineering on Microsoft — training data for the fictional company Technik.';
GRANT OWNERSHIP ON DATABASE AI_ACADEMY TO ROLE ACADEMY_ADMIN COPY CURRENT GRANTS;

USE ROLE ACADEMY_ADMIN;
USE WAREHOUSE ACADEMY_ADMIN_WH;

CREATE SCHEMA IF NOT EXISTS AI_ACADEMY.SEED
    COMMENT = 'Golden copy of the Technik data. Never edited by learners; sandboxes are cloned from here.';
CREATE SCHEMA IF NOT EXISTS AI_ACADEMY.SHARED
    COMMENT = 'Helper procedures shared by every learner, including RESET_TO().';

DROP SCHEMA IF EXISTS AI_ACADEMY.PUBLIC;

SELECT 'Account setup complete. Next: 01_seed_tables.sql' AS STATUS;
