/* =====================================================================
   20_learner_start_here.sql — run this once, before your first lab.

   You have two Snowflake roles, and the difference between them is part
   of the course:

     ACADEMY_LEARNER_<you>   You. Owns your sandbox schema, can create,
                             change and drop things in it. Use this in
                             worksheets.

     ACADEMY_AGENT_<you>     Your agents. Read-only on the same schema,
                             no create rights. Every connector, agent and
                             MCP server you build in this course signs in
                             with this role and no other. An agent that
                             cannot write cannot be talked into writing.

   Replace <you> below with your own tag -- the same suffix your admin
   used when provisioning you. If you are not sure what it is, run:

       SHOW ROLES LIKE 'ACADEMY_%';

   Everything you see here is fictional data about Technik, a made-up
   subsea equipment manufacturer. See the course scenario page.
   ===================================================================== */

-- 1. Become yourself, on your own warehouse, in your own schema. --------
USE ROLE ACADEMY_LEARNER_<you>;
USE WAREHOUSE ACADEMY_WH_<you>;
USE SCHEMA AI_ACADEMY.SANDBOX_<you>;

-- 2. Load the data. Every lab starts with a call like this; the argument
--    is the module you are about to do. 'BASE' is the plain seed.
CALL AI_ACADEMY.SHARED.RESET_TO('BASE');

-- Which modules can you reset to?
SELECT MODULE, TITLE FROM AI_ACADEMY.SEED.MODULES ORDER BY MODULE;

-- 3. Check what you got. ----------------------------------------------
SELECT 'SAP_PROJECTS'              AS TABLE_NAME, COUNT(*) AS ROWS_LOADED FROM SAP_PROJECTS
UNION ALL SELECT 'SAP_UNITS',                     COUNT(*) FROM SAP_UNITS
UNION ALL SELECT 'SAP_BOM_LINES',                 COUNT(*) FROM SAP_BOM_LINES
UNION ALL SELECT 'SAP_WORK_ORDERS',               COUNT(*) FROM SAP_WORK_ORDERS
UNION ALL SELECT 'SAP_WO_OPERATIONS',             COUNT(*) FROM SAP_WO_OPERATIONS
UNION ALL SELECT 'SAP_QUALITY_NOTIFICATIONS',     COUNT(*) FROM SAP_QUALITY_NOTIFICATIONS
UNION ALL SELECT 'TC_PARTS',                      COUNT(*) FROM TC_PARTS
UNION ALL SELECT 'TC_DRAWINGS',                   COUNT(*) FROM TC_DRAWINGS
UNION ALL SELECT 'TC_CNC_PROGRAMS',               COUNT(*) FROM TC_CNC_PROGRAMS
UNION ALL SELECT 'TC_DOCUMENTS',                  COUNT(*) FROM TC_DOCUMENTS
UNION ALL SELECT 'TC_ECNS',                       COUNT(*) FROM TC_ECNS
UNION ALL SELECT 'TC_ECN_AFFECTED_ITEMS',         COUNT(*) FROM TC_ECN_AFFECTED_ITEMS
UNION ALL SELECT 'FAT_RESULTS',                   COUNT(*) FROM FAT_RESULTS
ORDER BY TABLE_NAME;

-- Expected: 4, 10, 13, 27, 85, 18, 22, 19, 8, 17, 6, 12, 10.

-- 4. Three sanity checks you can read without knowing the data. --------

-- a) Where is work order 100004521? It should be at operation 0030,
--    Welding, in process -- and there should be an open notification
--    against it explaining why.
SELECT o.OP_SEQ, o.OPERATION, o.WORK_CENTER, o.STATUS
FROM SAP_WO_OPERATIONS o
WHERE o.WO_NO = '100004521'
ORDER BY o.OP_SEQ;

-- b) The latest released revision of drawing DU700001042, and the ECN
--    that changed it.
SELECT d.DRAWING_NO, d.REVISION, d.RELEASED_AT, e.ECN_NO, e.TITLE
FROM TC_DRAWINGS d
LEFT JOIN TC_ECN_AFFECTED_ITEMS a ON a.ITEM_NO = d.DRAWING_NO AND a.TO_REV = d.REVISION
LEFT JOIN TC_ECNS e ON e.ECN_NO = a.ECN_NO
WHERE d.DRAWING_NO = 'DU700001042'
  AND d.RELEASE_STATUS = 'Released';

-- c) The data has deliberate defects. This one finds them: operations
--    confirmed twice. You will meet it again in B10.
SELECT WO_NO, OP_SEQ, COUNT(*) AS CONFIRMATIONS
FROM SAP_WO_OPERATIONS
GROUP BY WO_NO, OP_SEQ
HAVING COUNT(*) > 1
ORDER BY WO_NO;

-- 5. Now look at the same schema the way your agents will. -------------
USE ROLE ACADEMY_AGENT_<you>;
USE WAREHOUSE ACADEMY_WH_<you>;

-- This works: the agent role can read.
SELECT COUNT(*) AS WORK_ORDERS_VISIBLE_TO_THE_AGENT
FROM AI_ACADEMY.SANDBOX_<you>.SAP_WORK_ORDERS;

-- This must fail with an "insufficient privileges" error. If it succeeds,
-- stop and tell your admin: your agent role is too powerful.
-- DELETE FROM AI_ACADEMY.SANDBOX_<you>.SAP_WORK_ORDERS WHERE WO_NO = '100004521';

-- 6. Back to being yourself.
USE ROLE ACADEMY_LEARNER_<you>;
