/* =====================================================================
   02_seed_sap.sql — projects, units, BOM, work orders and operations.

   Run as ACADEMY_ADMIN after 01_seed_tables.sql.

   Dates are stored as offsets in days from an anchor, which is the first
   day of the month the seed is run. RESET_TO() re-applies the same offset
   arithmetic in each sandbox, so "last month" and "this month" questions
   keep working however long after seeding a learner starts.

   Deliberate teaching defects in this file:
     * six operations confirmed twice (same WO_NO + OP_SEQ, two
       CONFIRMATION_NO values): a partial posting that was never reversed,
       followed by the full re-posting. Both rows are in the extract, so
       hours and operation counts are double-counted, and efficiency comes
       out well above 100% for welding at Plant 1 until the stale posting
       is dropped with QUALIFY. The later CONFIRMATION_NO is the one that
       counts;
     * work orders 100004510 and 100004513 reference drawing and CNC
       program revisions that a released ECN has already superseded.

   All values are fictional. See _source/course/scenario.md.
   ===================================================================== */

USE ROLE ACADEMY_ADMIN;
USE WAREHOUSE ACADEMY_ADMIN_WH;
USE SCHEMA AI_ACADEMY.SEED;

SET ANCHOR = (SELECT DATE_TRUNC('MONTH', CURRENT_DATE()));

/* ------------------------------------------------------------------ */
TRUNCATE TABLE SAP_PROJECTS;
INSERT INTO SAP_PROJECTS (PROJECT_ID, PROJECT_NAME, CLIENT_NAME, FIELD_NAME, FAT_DUE_DATE, STATUS)
SELECT v.PROJECT_ID, v.PROJECT_NAME, v.CLIENT_NAME, v.FIELD_NAME,
       DATEADD(day, v.FAT_OFF, $ANCHOR), v.STATUS
FROM VALUES
  ('PRJ-2018','Skarvholm Phase 1 XT Package','Nordvik Energy','Skarvholm',      -150,'Delivered'),
  ('PRJ-2031','Skarvholm Phase 2 XT and Manifold','Nordvik Energy','Skarvholm',   45,'In Progress'),
  ('PRJ-2044','Marlin Deep Manifold Package','Aurora Offshore','Marlin Deep',     96,'In Progress'),
  ('PRJ-2052','Corvina Norte XT Package','Vantia Petroleo','Corvina Norte',      180,'Planning')
AS v(PROJECT_ID, PROJECT_NAME, CLIENT_NAME, FIELD_NAME, FAT_OFF, STATUS);

/* ------------------------------------------------------------------ */
TRUNCATE TABLE SAP_UNITS;
INSERT INTO SAP_UNITS (SERIAL_NO, PRODUCT_TYPE, MODEL, PROJECT_ID, PLANT, STATUS) VALUES
  ('XT-V2-1001','XT',      'V2','PRJ-2018','Plant 1','Delivered'),
  ('XT-V2-1042','XT',      'V2','PRJ-2031','Plant 1','In Manufacturing'),
  ('XT-V2-1043','XT',      'V2','PRJ-2031','Plant 1','In Manufacturing'),
  ('XT-V2-1044','XT',      'V2','PRJ-2031','Plant 1','Planned'),
  ('MF-H4-2007','MANIFOLD','H4','PRJ-2031','Plant 1','In Manufacturing'),
  ('XT-V2-1051','XT',      'V2','PRJ-2044','Plant 2','In Manufacturing'),
  ('XT-V3-1052','XT',      'V3','PRJ-2044','Plant 2','Planned'),
  ('MF-H4-2011','MANIFOLD','H4','PRJ-2044','Plant 2','In Manufacturing'),
  ('XT-V2-1060','XT',      'V2','PRJ-2052','Plant 1','Planned'),
  ('MF-H4-2015','MANIFOLD','H4','PRJ-2052','Plant 1','Planned');

/* ------------------------------------------------------------------ */
TRUNCATE TABLE SAP_BOM_LINES;
INSERT INTO SAP_BOM_LINES (PARENT_PART_NO, COMPONENT_PART_NO, QTY) VALUES
  ('P7000002001','P7000001042',1),
  ('P7000002001','P7000001103',4),
  ('P7000002001','P7000001156',4),
  ('P7000002001','P7000001142',1),
  ('P7000002001','P7000001134',1),
  ('P7000002001','P7000001055',2),
  ('P7000002001','P7000001117',1),
  ('P7000002001','P7000001088',2),
  ('P7000002010','P7000001125',1),
  ('P7000002010','P7000001071',2),
  ('P7000002010','P7000001088',6),
  ('P7000002010','P7000001103',2),
  ('P7000002010','P7000001117',2);

/* ------------------------------------------------------------------ */
TRUNCATE TABLE SAP_WORK_ORDERS;
INSERT INTO SAP_WORK_ORDERS (WO_NO, PART_NO, SERIAL_NO, PROJECT_ID, PLANT, RELEASED_AT, COMPLETED_AT, STATUS)
SELECT v.WO_NO, v.PART_NO, v.SERIAL_NO, v.PROJECT_ID, v.PLANT,
       DATEADD(day, v.REL_OFF, $ANCHOR), DATEADD(day, v.COMP_OFF, $ANCHOR), v.STATUS
FROM VALUES
  -- Plant 1, PRJ-2031
  ('100004501','P7000001042','XT-V2-1042','PRJ-2031','Plant 1', -62, -47,'TECO'),
  ('100004502','P7000001103','XT-V2-1042','PRJ-2031','Plant 1', -60, -41,'TECO'),
  ('100004503','P7000001156','XT-V2-1042','PRJ-2031','Plant 1', -58, -39,'TECO'),
  ('100004504','P7000001055','XT-V2-1042','PRJ-2031','Plant 1', -55, -30,'TECO'),
  ('100004505','P7000002001','XT-V2-1042','PRJ-2031','Plant 1', -28, NULL,'PCNF'),
  ('100004506','P7000001042','XT-V2-1043','PRJ-2031','Plant 1', -40, -22,'TECO'),
  ('100004507','P7000001103','XT-V2-1043','PRJ-2031','Plant 1', -38, -19,'TECO'),
  ('100004508','P7000001156','XT-V2-1043','PRJ-2031','Plant 1', -35, NULL,'PCNF'),
  ('100004509','P7000001055','XT-V2-1043','PRJ-2031','Plant 1', -20, NULL,'PCNF'),
  ('100004510','P7000001042','XT-V2-1044','PRJ-2031','Plant 1',  -8, NULL,'REL'),
  ('100004511','P7000001125','MF-H4-2007','PRJ-2031','Plant 1', -70, -44,'TECO'),
  ('100004512','P7000001071','MF-H4-2007','PRJ-2031','Plant 1', -50, -25,'TECO'),
  ('100004513','P7000001088','MF-H4-2007','PRJ-2031','Plant 1', -33, NULL,'PCNF'),
  ('100004514','P7000002010','MF-H4-2007','PRJ-2031','Plant 1',  -5, NULL,'REL'),
  ('100004515','P7000001142','XT-V2-1044','PRJ-2031','Plant 1',NULL, NULL,'CRTD'),
  -- Plant 2, PRJ-2044
  ('100004520','P7000001071','MF-H4-2011','PRJ-2044','Plant 2', -66, -43,'TECO'),
  ('100004521','P7000001088','MF-H4-2011','PRJ-2044','Plant 2', -45, NULL,'PCNF'),
  ('100004522','P7000001125','MF-H4-2011','PRJ-2044','Plant 2', -52, -29,'TECO'),
  ('100004523','P7000001117','MF-H4-2011','PRJ-2044','Plant 2', -30, -11,'TECO'),
  ('100004524','P7000001042','XT-V2-1051','PRJ-2044','Plant 2', -36, -14,'TECO'),
  ('100004525','P7000001103','XT-V2-1051','PRJ-2044','Plant 2', -34, -12,'TECO'),
  ('100004526','P7000001055','XT-V2-1051','PRJ-2044','Plant 2', -18, NULL,'PCNF'),
  ('100004527','P7000001134','XT-V2-1051','PRJ-2044','Plant 2', -10,  -2,'TECO'),
  ('100004528','P7000002010','MF-H4-2011','PRJ-2044','Plant 2',NULL, NULL,'CRTD'),
  ('100004529','P7000001142','XT-V2-1051','PRJ-2044','Plant 2',  -6, NULL,'REL'),
  -- Plant 1, PRJ-2018 (delivered, used for historical comparisons)
  ('100004490','P7000001042','XT-V2-1001','PRJ-2018','Plant 1',-175,-150,'TECO'),
  ('100004491','P7000002001','XT-V2-1001','PRJ-2018','Plant 1',-148,-120,'TECO')
AS v(WO_NO, PART_NO, SERIAL_NO, PROJECT_ID, PLANT, REL_OFF, COMP_OFF, STATUS);

/* ------------------------------------------------------------------
   Operations. One row per confirmation.
   Rows marked "duplicate" are the deliberate defect: a second
   confirmation posted against an operation that was already confirmed.
   ------------------------------------------------------------------ */
TRUNCATE TABLE SAP_WO_OPERATIONS;
INSERT INTO SAP_WO_OPERATIONS
  (WO_NO, OP_SEQ, OPERATION, WORK_CENTER, ROUTING_HOURS, ACTUAL_HOURS,
   PLANNED_START, ACTUAL_START, ACTUAL_END, STATUS,
   DRAWING_NO, DRAWING_REV, CNC_PROGRAM_NO, CNC_PROGRAM_REV, WORK_INSTRUCTION_NO,
   CONFIRMATION_NO, CONFIRMED_AT)
SELECT v.WO_NO, v.OP_SEQ, v.OPERATION, v.WORK_CENTER, v.ROUTING_HOURS, v.ACTUAL_HOURS,
       DATEADD(day, v.PLAN_OFF, $ANCHOR), DATEADD(day, v.START_OFF, $ANCHOR), DATEADD(day, v.END_OFF, $ANCHOR),
       v.STATUS, v.DRAWING_NO, v.DRAWING_REV, v.CNC_PROGRAM_NO, v.CNC_PROGRAM_REV, v.WORK_INSTRUCTION_NO,
       v.CONFIRMATION_NO, DATEADD(day, v.CONF_OFF, $ANCHOR)
FROM VALUES
  -- 100004501  Valve block for XT-V2-1042
  ('100004501','0010','Machining',         'MACH-01',24,25.0,-61,  -61,  -58,'CNF',   'DU700001042','C','T7000000217','B','SWI70000290','9000010001', -58),
  ('100004501','0020','Cladding',          'CLAD-01',16,17.5,-57,  -57,  -53,'CNF',   'DU700001042','C',NULL,         NULL,'SWI70000318','9000010002', -53),
  ('100004501','0030','Coating',           'COAT-01', 8, 7.5,-52,  -52,  -48,'CNF',   NULL,         NULL,NULL,        NULL,'SWI70000377','9000010003', -48),
  -- 100004502  Gate valve body for XT-V2-1042
  ('100004502','0010','Machining',         'MACH-02',18,19.5,-59,  -59,  -55,'CNF',   'DU700001103','A','T7000000224','A','SWI70000290','9000010011', -55),
  ('100004502','0020','Cladding',          'CLAD-01',12, 7.0,-54,  -54,  -50,'CNF',   'DU700001103','A',NULL,         NULL,'SWI70000318','9000010012', -50),  -- partial posting, never reversed
  ('100004502','0020','Cladding',          'CLAD-01',12,13.0,-54,  -54,  -50,'CNF',   'DU700001103','A',NULL,         NULL,'SWI70000318','9000010013', -49),  -- full re-posting: the figure that counts
  ('100004502','0030','Coating',           'COAT-01', 6, 5.5,-46,  -46,  -42,'CNF',   NULL,         NULL,NULL,        NULL,'SWI70000377','9000010014', -42),
  -- 100004503  Bonnet for XT-V2-1042
  ('100004503','0010','Machining',         'MACH-02',10, 9.5,-57,  -57,  -54,'CNF',   'DU700001156','B','T7000000248','A','SWI70000290','9000010021', -54),
  ('100004503','0020','Cladding',          'CLAD-01', 8, 8.5,-53,  -53,  -49,'CNF',   'DU700001156','B',NULL,         NULL,'SWI70000318','9000010022', -49),
  ('100004503','0030','Coating',           'COAT-01', 4, 4.0,-44,  -44,  -40,'CNF',   NULL,         NULL,NULL,        NULL,'SWI70000377','9000010023', -40),
  -- 100004504  Flow loop spool for XT-V2-1042
  ('100004504','0010','Machining',         'MACH-01', 6, 6.5,-54,  -54,  -52,'CNF',   'DU700001055','B',NULL,         NULL,'SWI70000290','9000010031', -52),
  ('100004504','0020','Welding',           'WELD-01',14, 9.0,-51,  -51,  -45,'CNF',   'DU700001055','B',NULL,         NULL,'SWI70000355','9000010032', -45),  -- partial posting, never reversed
  ('100004504','0020','Welding',           'WELD-01',14,15.0,-51,  -51,  -45,'CNF',   'DU700001055','B',NULL,         NULL,'SWI70000355','9000010033', -44),  -- full re-posting: the figure that counts
  ('100004504','0030','Bending',           'BEND-01', 5, 4.5,-43,  -43,  -38,'CNF',   'DU700001055','B',NULL,         NULL,'SWI70000366','9000010034', -38),
  ('100004504','0040','Coating',           'COAT-01', 6, 6.0,-36,  -36,  -31,'CNF',   NULL,         NULL,NULL,        NULL,'SWI70000377','9000010035', -31),
  -- 100004505  Tree assembly XT-V2-1042
  ('100004505','0010','Assembly & Testing','ASSY-01',60,58.0,-27,  -27,  -14,'CNF',   'DU700002001','B',NULL,         NULL,'SWI70000402','9000010041', -14),
  ('100004505','0020','Assembly & Testing','TEST-01',24,NULL,-13,  -13, NULL,'INPROC','DU700002001','B',NULL,         NULL,'SWI70000402',NULL,        NULL),
  -- 100004506  Valve block for XT-V2-1043
  ('100004506','0010','Machining',         'MACH-01',24,14.0,-39,  -39,  -36,'CNF',   'DU700001042','C','T7000000217','B','SWI70000290','9000010051', -36),  -- partial posting, never reversed
  ('100004506','0010','Machining',         'MACH-01',24,23.0,-39,  -39,  -36,'CNF',   'DU700001042','C','T7000000217','B','SWI70000290','9000010052', -35),  -- full re-posting: the figure that counts
  ('100004506','0020','Cladding',          'CLAD-01',16,18.0,-35,  -35,  -30,'CNF',   'DU700001042','C',NULL,         NULL,'SWI70000318','9000010053', -30),
  ('100004506','0030','Coating',           'COAT-01', 8, 8.0,-28,  -28,  -23,'CNF',   NULL,         NULL,NULL,        NULL,'SWI70000377','9000010054', -23),
  -- 100004507  Gate valve body for XT-V2-1043
  ('100004507','0010','Machining',         'MACH-02',18,17.0,-37,  -37,  -33,'CNF',   'DU700001103','A','T7000000224','A','SWI70000290','9000010061', -33),
  ('100004507','0020','Cladding',          'CLAD-01',12,14.5,-32,  -32,  -26,'CNF',   'DU700001103','A',NULL,         NULL,'SWI70000318','9000010062', -26),
  ('100004507','0030','Coating',           'COAT-01', 6, 6.5,-24,  -24,  -20,'CNF',   NULL,         NULL,NULL,        NULL,'SWI70000377','9000010063', -20),
  -- 100004508  Bonnet for XT-V2-1043
  ('100004508','0010','Machining',         'MACH-02',10,10.5,-34,  -34,  -31,'CNF',   'DU700001156','B','T7000000248','A','SWI70000290','9000010071', -31),
  ('100004508','0020','Cladding',          'CLAD-01', 8,NULL,-30,  -16, NULL,'INPROC','DU700001156','B',NULL,         NULL,'SWI70000318',NULL,        NULL),
  ('100004508','0030','Coating',           'COAT-01', 4,NULL,-12, NULL, NULL,'OPEN',  NULL,         NULL,NULL,        NULL,'SWI70000377',NULL,        NULL),
  -- 100004509  Flow loop spool for XT-V2-1043
  ('100004509','0010','Machining',         'MACH-01', 6, 6.0,-19,  -19,  -17,'CNF',   'DU700001055','B',NULL,         NULL,'SWI70000290','9000010081', -17),
  ('100004509','0020','Welding',           'WELD-01',14,NULL,-16,   -9, NULL,'INPROC','DU700001055','B',NULL,         NULL,'SWI70000355',NULL,        NULL),
  ('100004509','0030','Bending',           'BEND-01', 5,NULL, -6, NULL, NULL,'OPEN',  'DU700001055','B',NULL,         NULL,'SWI70000366',NULL,        NULL),
  ('100004509','0040','Coating',           'COAT-01', 6,NULL, -3, NULL, NULL,'OPEN',  NULL,         NULL,NULL,        NULL,'SWI70000377',NULL,        NULL),
  -- 100004510  Valve block for XT-V2-1044 -- released on superseded revisions (ECN70000051)
  ('100004510','0010','Machining',         'MACH-01',24,NULL, -7, NULL, NULL,'OPEN',  'DU700001042','B','T7000000217','A','SWI70000290',NULL,        NULL),
  ('100004510','0020','Cladding',          'CLAD-01',16,NULL, -2, NULL, NULL,'OPEN',  'DU700001042','B',NULL,         NULL,'SWI70000318',NULL,        NULL),
  ('100004510','0030','Coating',           'COAT-01', 8,NULL,  4, NULL, NULL,'OPEN',  NULL,         NULL,NULL,        NULL,'SWI70000377',NULL,        NULL),
  -- 100004511  Manifold frame weldment for MF-H4-2007
  ('100004511','0010','Welding',           'WELD-02',40,28.0,-69,  -69,  -55,'CNF',   'DU700001125','B',NULL,         NULL,'SWI70000355','9000010091', -55),  -- partial posting, never reversed
  ('100004511','0010','Welding',           'WELD-02',40,46.0,-69,  -69,  -55,'CNF',   'DU700001125','B',NULL,         NULL,'SWI70000355','9000010092', -54),  -- full re-posting: the figure that counts
  ('100004511','0020','Coating',           'COAT-01',12,13.0,-52,  -52,  -45,'CNF',   NULL,         NULL,NULL,        NULL,'SWI70000377','9000010093', -45),
  -- 100004512  Header pipe for MF-H4-2007
  ('100004512','0010','Machining',         'MACH-01', 8, 8.5,-49,  -49,  -46,'CNF',   'DU700001071','B',NULL,         NULL,'SWI70000290','9000010101', -46),
  ('100004512','0020','Cladding',          'CLAD-01',20,22.5,-45,  -45,  -38,'CNF',   'DU700001071','B',NULL,         NULL,'SWI70000318','9000010102', -38),
  ('100004512','0030','Welding',           'WELD-01',12, 8.0,-37,  -37,  -31,'CNF',   'DU700001071','B',NULL,         NULL,'SWI70000355','9000010103', -31),  -- partial posting, never reversed
  ('100004512','0030','Welding',           'WELD-01',12,13.0,-37,  -37,  -31,'CNF',   'DU700001071','B',NULL,         NULL,'SWI70000355','9000010104', -30),  -- full re-posting: the figure that counts
  ('100004512','0040','Coating',           'COAT-01', 7, 7.0,-29,  -29,  -26,'CNF',   NULL,         NULL,NULL,        NULL,'SWI70000377','9000010105', -26),
  -- 100004513  Hub connector for MF-H4-2007 -- released on superseded revisions (ECN70000078)
  ('100004513','0010','Machining',         'MACH-02',14,15.5,-32,  -32,  -28,'CNF',   'DU700001088','C','T7000000231','C','SWI70000290','9000010111', -28),
  ('100004513','0020','Cladding',          'CLAD-01',10,NULL,-27,  -20, NULL,'INPROC','DU700001088','C',NULL,         NULL,'SWI70000318',NULL,        NULL),
  ('100004513','0030','Welding',           'WELD-02', 6,NULL,-16, NULL, NULL,'OPEN',  'DU700001088','C',NULL,         NULL,'SWI70000355',NULL,        NULL),
  ('100004513','0040','Coating',           'COAT-01', 5,NULL,-12, NULL, NULL,'OPEN',  NULL,         NULL,NULL,        NULL,'SWI70000377',NULL,        NULL),
  -- 100004514  Manifold assembly MF-H4-2007
  ('100004514','0010','Assembly & Testing','ASSY-01',80,NULL, -4,   -2, NULL,'INPROC','DU700002010','A',NULL,         NULL,'SWI70000402',NULL,        NULL),
  ('100004514','0020','Assembly & Testing','TEST-01',30,NULL, 12, NULL, NULL,'OPEN',  'DU700002010','A',NULL,         NULL,'SWI70000402',NULL,        NULL),
  -- 100004515  Tree cap for XT-V2-1044 (not yet released)
  ('100004515','0010','Machining',         'MACH-02', 6,NULL,  3, NULL, NULL,'OPEN',  'DU700001142','A','T7000000255','A','SWI70000290',NULL,        NULL),
  ('100004515','0020','Coating',           'COAT-01', 3,NULL,  8, NULL, NULL,'OPEN',  NULL,         NULL,NULL,        NULL,'SWI70000377',NULL,        NULL),
  -- 100004520  Header pipe for MF-H4-2011 (Plant 2)
  ('100004520','0010','Machining',         'MACH-21', 8, 9.0,-65,  -65,  -62,'CNF',   'DU700001071','A',NULL,         NULL,'SWI70000290','9000010121', -62),
  ('100004520','0020','Cladding',          'CLAD-21',20,21.0,-61,  -61,  -54,'CNF',   'DU700001071','A',NULL,         NULL,'SWI70000318','9000010122', -54),
  ('100004520','0030','Welding',           'WELD-21',12,14.5,-53,  -53,  -47,'CNF',   'DU700001071','A',NULL,         NULL,'SWI70000355','9000010123', -47),
  ('100004520','0040','Coating',           'COAT-21', 7, 7.5,-46,  -46,  -44,'CNF',   NULL,         NULL,NULL,        NULL,'SWI70000377','9000010124', -44),
  -- 100004521  Hub connector for MF-H4-2011 -- held at Welding by QN 300001237
  ('100004521','0010','Machining',         'MACH-21',14,13.5,-44,  -44,  -40,'CNF',   'DU700001088','C','T7000000231','C','SWI70000290','9000010131', -40),
  ('100004521','0020','Cladding',          'CLAD-21',10,11.0,-39,  -39,  -33,'CNF',   'DU700001088','C',NULL,         NULL,'SWI70000318','9000010132', -33),
  ('100004521','0030','Welding',           'WELD-21', 6,NULL,-32,  -24, NULL,'INPROC','DU700001088','C',NULL,         NULL,'SWI70000355',NULL,        NULL),
  ('100004521','0040','Coating',           'COAT-21', 5,NULL,-20, NULL, NULL,'OPEN',  NULL,         NULL,NULL,        NULL,'SWI70000377',NULL,        NULL),
  -- 100004522  Manifold frame weldment for MF-H4-2011
  ('100004522','0010','Welding',           'WELD-21',40,42.0,-51,  -51,  -38,'CNF',   'DU700001125','B',NULL,         NULL,'SWI70000355','9000010141', -38),
  ('100004522','0020','Coating',           'COAT-21',12,11.5,-36,  -36,  -30,'CNF',   NULL,         NULL,NULL,        NULL,'SWI70000377','9000010142', -30),
  -- 100004523  Choke bridge spool for MF-H4-2011
  ('100004523','0010','Machining',         'MACH-21', 7, 7.5,-29,  -29,  -26,'CNF',   'DU700001117','A',NULL,         NULL,'SWI70000290','9000010151', -26),
  ('100004523','0020','Welding',           'WELD-21', 9, 9.5,-25,  -25,  -18,'CNF',   'DU700001117','A',NULL,         NULL,'SWI70000355','9000010152', -18),
  ('100004523','0030','Coating',           'COAT-21', 4, 4.0,-16,  -16,  -12,'CNF',   NULL,         NULL,NULL,        NULL,'SWI70000377','9000010153', -12),
  -- 100004524  Valve block for XT-V2-1051
  ('100004524','0010','Machining',         'MACH-22',24,15.0,-35,  -35,  -30,'CNF',   'DU700001042','C','T7000000217','B','SWI70000290','9000010161', -30),  -- partial posting, never reversed
  ('100004524','0010','Machining',         'MACH-22',24,26.0,-35,  -35,  -30,'CNF',   'DU700001042','C','T7000000217','B','SWI70000290','9000010162', -29),  -- full re-posting: the figure that counts
  ('100004524','0020','Cladding',          'CLAD-21',16,16.5,-28,  -28,  -22,'CNF',   'DU700001042','C',NULL,         NULL,'SWI70000318','9000010163', -22),
  ('100004524','0030','Coating',           'COAT-21', 8, 8.5,-20,  -20,  -15,'CNF',   NULL,         NULL,NULL,        NULL,'SWI70000377','9000010164', -15),
  -- 100004525  Gate valve body for XT-V2-1051
  ('100004525','0010','Machining',         'MACH-22',18,16.5,-33,  -33,  -29,'CNF',   'DU700001103','A','T7000000224','A','SWI70000290','9000010171', -29),
  ('100004525','0020','Cladding',          'CLAD-21',12,12.5,-27,  -27,  -21,'CNF',   'DU700001103','A',NULL,         NULL,'SWI70000318','9000010172', -21),
  ('100004525','0030','Coating',           'COAT-21', 6, 6.0,-19,  -19,  -13,'CNF',   NULL,         NULL,NULL,        NULL,'SWI70000377','9000010173', -13),
  -- 100004526  Flow loop spool for XT-V2-1051
  ('100004526','0010','Machining',         'MACH-21', 6, 5.5,-17,  -17,  -15,'CNF',   'DU700001055','B',NULL,         NULL,'SWI70000290','9000010181', -15),
  ('100004526','0020','Welding',           'WELD-21',14,15.5,-14,  -14,   -9,'CNF',   'DU700001055','B',NULL,         NULL,'SWI70000355','9000010182',  -9),
  ('100004526','0030','Bending',           'BEND-21', 5,NULL, -8,   -6, NULL,'INPROC','DU700001055','B',NULL,         NULL,'SWI70000366',NULL,        NULL),
  ('100004526','0040','Coating',           'COAT-21', 6,NULL, -4, NULL, NULL,'OPEN',  NULL,         NULL,NULL,        NULL,'SWI70000377',NULL,        NULL),
  -- 100004527  Test cap for XT-V2-1051
  ('100004527','0010','Machining',         'MACH-22', 5, 5.0, -9,   -9,   -7,'CNF',   'DU700001134','A','T7000000262','A','SWI70000290','9000010191',  -7),
  ('100004527','0020','Coating',           'COAT-21', 3, 3.5, -6,   -6,   -3,'CNF',   NULL,         NULL,NULL,        NULL,'SWI70000377','9000010192',  -3),
  -- 100004528  Manifold assembly MF-H4-2011 (not yet released)
  ('100004528','0010','Assembly & Testing','ASSY-21',80,NULL, 10, NULL, NULL,'OPEN',  'DU700002010','A',NULL,         NULL,'SWI70000402',NULL,        NULL),
  ('100004528','0020','Assembly & Testing','TEST-21',30,NULL, 25, NULL, NULL,'OPEN',  'DU700002010','A',NULL,         NULL,'SWI70000402',NULL,        NULL),
  -- 100004529  Tree cap for XT-V2-1051
  ('100004529','0010','Machining',         'MACH-22', 6,NULL, -5, NULL, NULL,'OPEN',  'DU700001142','A','T7000000255','A','SWI70000290',NULL,        NULL),
  ('100004529','0020','Coating',           'COAT-21', 3,NULL,  0, NULL, NULL,'OPEN',  NULL,         NULL,NULL,        NULL,'SWI70000377',NULL,        NULL),
  -- 100004490 / 100004491  PRJ-2018, delivered. Correct revisions for their time.
  ('100004490','0010','Machining',         'MACH-01',24,27.0,-174,-174,-170,'CNF',   'DU700001042','B','T7000000217','A','SWI70000290','9000009001',-170),
  ('100004490','0020','Cladding',          'CLAD-01',16,19.0,-169,-169,-160,'CNF',   'DU700001042','B',NULL,         NULL,'SWI70000318','9000009002',-160),
  ('100004490','0030','Coating',           'COAT-01', 8, 8.5,-158,-158,-151,'CNF',   NULL,         NULL,NULL,        NULL,'SWI70000377','9000009003',-151),
  ('100004491','0010','Assembly & Testing','ASSY-01',60,64.0,-147,-147,-132,'CNF',   'DU700002001','B',NULL,         NULL,'SWI70000402','9000009011',-132),
  ('100004491','0020','Assembly & Testing','TEST-01',24,25.0,-131,-131,-121,'CNF',   'DU700002001','B',NULL,         NULL,'SWI70000402','9000009012',-121)
AS v(WO_NO, OP_SEQ, OPERATION, WORK_CENTER, ROUTING_HOURS, ACTUAL_HOURS,
     PLAN_OFF, START_OFF, END_OFF, STATUS,
     DRAWING_NO, DRAWING_REV, CNC_PROGRAM_NO, CNC_PROGRAM_REV, WORK_INSTRUCTION_NO,
     CONFIRMATION_NO, CONF_OFF);

SELECT 'SAP data seeded. Next: 03_seed_teamcenter.sql' AS STATUS;
