/* =====================================================================
   03_seed_teamcenter.sql — parts, drawings, CNC programs, controlled
   documents and Engineering Change Notifications.

   Run as ACADEMY_ADMIN after 02_seed_sap.sql.

   Every item carries its full revision history, so "the latest released
   revision" is a real query rather than a lookup. Deliberate states:

     * ECN70000042 is released and requires SWI70000318 revision C, but
       the document is still at revision B -- the change Carla drafts.
     * ECN70000070 is only In Review, so SWI70000402 correctly stays at C.
     * SOP70000114, SWI70000318 and TDS70000044 are past their review date.
     * P7000001042 has an In Work revision D that must not be mistaken for
       the latest released revision (C).

   All values are fictional. See _source/course/scenario.md.
   ===================================================================== */

USE ROLE ACADEMY_ADMIN;
USE WAREHOUSE ACADEMY_ADMIN_WH;
USE SCHEMA AI_ACADEMY.SEED;

SET ANCHOR = (SELECT DATE_TRUNC('MONTH', CURRENT_DATE()));

/* ------------------------------------------------------------------ */
TRUNCATE TABLE TC_PARTS;
INSERT INTO TC_PARTS (PART_NO, REVISION, DESCRIPTION, RELEASE_STATUS, RELEASED_AT)
SELECT v.PART_NO, v.REVISION, v.DESCRIPTION, v.RELEASE_STATUS, DATEADD(day, v.REL_OFF, $ANCHOR)
FROM VALUES
  ('P7000002001','A','Subsea Tree Assembly, XT-V2', 'Superseded',-400),
  ('P7000002001','B','Subsea Tree Assembly, XT-V2', 'Released',  -210),
  ('P7000002010','A','Manifold Assembly, MF-H4',    'Released',  -260),
  ('P7000001042','A','Valve Block, XT-V2',          'Superseded',-380),
  ('P7000001042','B','Valve Block, XT-V2',          'Superseded',-240),
  ('P7000001042','C','Valve Block, XT-V2',          'Released',   -70),
  ('P7000001042','D','Valve Block, XT-V2',          'In Work',   NULL),
  ('P7000001055','A','Flow Loop Spool, 4 in',       'Superseded',-350),
  ('P7000001055','B','Flow Loop Spool, 4 in',       'Released',  -190),
  ('P7000001071','A','Manifold Header Pipe, 10 in', 'Superseded',-300),
  ('P7000001071','B','Manifold Header Pipe, 10 in', 'Released',   -58),
  ('P7000001088','B','Hub Connector, 5-1/8 in',     'Superseded',-330),
  ('P7000001088','C','Hub Connector, 5-1/8 in',     'Superseded',-150),
  ('P7000001088','D','Hub Connector, 5-1/8 in',     'Released',   -40),
  ('P7000001103','A','Gate Valve Body, 5-1/8 in',   'Released',  -290),
  ('P7000001117','A','Choke Bridge Spool',          'Released',  -275),
  ('P7000001125','A','Manifold Frame Weldment',     'Superseded',-320),
  ('P7000001125','B','Manifold Frame Weldment',     'Released',  -180),
  ('P7000001134','A','Test Cap Assembly',           'Released',  -310),
  ('P7000001142','A','Tree Cap, XT-V2',             'Released',  -305),
  ('P7000001156','A','Master Valve Bonnet',         'Superseded',-340),
  ('P7000001156','B','Master Valve Bonnet',         'Released',  -175)
AS v(PART_NO, REVISION, DESCRIPTION, RELEASE_STATUS, REL_OFF);

/* ------------------------------------------------------------------ */
TRUNCATE TABLE TC_DRAWINGS;
INSERT INTO TC_DRAWINGS (DRAWING_NO, REVISION, PART_NO, TITLE, RELEASE_STATUS, RELEASED_AT)
SELECT v.DRAWING_NO, v.REVISION, v.PART_NO, v.TITLE, v.RELEASE_STATUS, DATEADD(day, v.REL_OFF, $ANCHOR)
FROM VALUES
  ('DU700002001','B','P7000002001','XT-V2 Tree General Arrangement',      'Released',  -210),
  ('DU700002010','A','P7000002010','MF-H4 Manifold General Arrangement',  'Released',  -260),
  ('DU700001042','A','P7000001042','Valve Block, XT-V2',                  'Superseded',-380),
  ('DU700001042','B','P7000001042','Valve Block, XT-V2',                  'Superseded',-240),
  ('DU700001042','C','P7000001042','Valve Block, XT-V2',                  'Released',   -70),
  ('DU700001055','A','P7000001055','Flow Loop Spool, 4 in',               'Superseded',-350),
  ('DU700001055','B','P7000001055','Flow Loop Spool, 4 in',               'Released',  -190),
  ('DU700001071','A','P7000001071','Manifold Header Pipe, 10 in',         'Superseded',-300),
  ('DU700001071','B','P7000001071','Manifold Header Pipe, 10 in',         'Released',   -58),
  ('DU700001088','C','P7000001088','Hub Connector, 5-1/8 in',             'Superseded',-150),
  ('DU700001088','D','P7000001088','Hub Connector, 5-1/8 in',             'Released',   -40),
  ('DU700001103','A','P7000001103','Gate Valve Body, 5-1/8 in',           'Released',  -290),
  ('DU700001117','A','P7000001117','Choke Bridge Spool',                  'Released',  -275),
  ('DU700001125','A','P7000001125','Manifold Frame Weldment',             'Superseded',-320),
  ('DU700001125','B','P7000001125','Manifold Frame Weldment',             'Released',  -180),
  ('DU700001134','A','P7000001134','Test Cap Assembly',                   'Released',  -310),
  ('DU700001142','A','P7000001142','Tree Cap, XT-V2',                     'Released',  -305),
  ('DU700001156','A','P7000001156','Master Valve Bonnet',                 'Superseded',-340),
  ('DU700001156','B','P7000001156','Master Valve Bonnet',                 'Released',  -175)
AS v(DRAWING_NO, REVISION, PART_NO, TITLE, RELEASE_STATUS, REL_OFF);

/* ------------------------------------------------------------------ */
TRUNCATE TABLE TC_CNC_PROGRAMS;
INSERT INTO TC_CNC_PROGRAMS (PROGRAM_NO, REVISION, PART_NO, MACHINE, RELEASE_STATUS, RELEASED_AT)
SELECT v.PROGRAM_NO, v.REVISION, v.PART_NO, v.MACHINE, v.RELEASE_STATUS, DATEADD(day, v.REL_OFF, $ANCHOR)
FROM VALUES
  ('T7000000217','A','P7000001042','MAZAK-INTEGREX-1','Superseded',-240),
  ('T7000000217','B','P7000001042','MAZAK-INTEGREX-1','Released',   -70),
  ('T7000000224','A','P7000001103','MAZAK-INTEGREX-1','Released',  -290),
  ('T7000000231','C','P7000001088','DMG-DMU-2',       'Superseded',-150),
  ('T7000000231','D','P7000001088','DMG-DMU-2',       'Released',   -40),
  ('T7000000248','A','P7000001156','DMG-DMU-2',       'Released',  -175),
  ('T7000000255','A','P7000001142','MAZAK-INTEGREX-2','Released',  -305),
  ('T7000000262','A','P7000001134','MAZAK-INTEGREX-2','Released',  -310)
AS v(PROGRAM_NO, REVISION, PART_NO, MACHINE, RELEASE_STATUS, REL_OFF);

/* ------------------------------------------------------------------ */
TRUNCATE TABLE TC_DOCUMENTS;
INSERT INTO TC_DOCUMENTS (DOC_NO, DOC_TYPE, REVISION, TITLE, OWNER, STATUS, RELEASED_AT, NEXT_REVIEW_DATE)
SELECT v.DOC_NO, v.DOC_TYPE, v.REVISION, v.TITLE, v.OWNER, v.STATUS,
       DATEADD(day, v.REL_OFF, $ANCHOR), DATEADD(day, v.REVIEW_OFF, $ANCHOR)
FROM VALUES
  ('SOP70000101','SOP','B','Quality Notification Handling',                 'Bruno Alves','Released',-220, 120),
  ('SOP70000114','SOP','A','Engineering Change Notification Process',        'Carla Reis', 'Released',-260, -20),
  ('SOP70000129','SOP','A','Work Order Release and Confirmation',            'Ana Duarte', 'Released',-200, 160),
  ('SWI70000290','SWI','C','Machining Setup and First-Article Inspection',   'Diego Matos','Released',-150, 210),
  ('SWI70000318','SWI','A','Cladding Preparation and Inspection',            'Carla Reis', 'Superseded',-400,NULL),
  ('SWI70000318','SWI','B','Cladding Preparation and Inspection',            'Carla Reis', 'Released',-180,  -5),
  ('SWI70000355','SWI','B','Structural Welding of Manifold Frames',          'Bruno Alves','Released',-170, 190),
  ('SWI70000366','SWI','A','Pipe Bending and Ovality Check',                 'Carla Reis', 'Released',-280,  80),
  ('SWI70000377','SWI','B','Surface Preparation and Coating Application',    'Carla Reis', 'Released',-140, 220),
  ('SWI70000402','SWI','C','Hydrostatic Test During Assembly and Testing',   'Bruno Alves','Released',-130, 230),
  ('SWI70000411','SWI','A','Nitrogen Leak Test',                             'Bruno Alves','In Review',NULL,NULL),
  ('LWI70000211','LWI','A','Weld Prep Inspection, Plant 1',                  'Bruno Alves','Released',-190, 170),
  ('GWI70000027','GWI','D','Controlled Document Authoring Template',         'Carla Reis', 'Released',-240, 120),
  ('DGL70000009','DGL','B','Cladding Design Guidelines',                     'Carla Reis', 'Released',-210, 150),
  ('DCP70000076','DCP','A','Machining Data Collection Points',               'Diego Matos','Released',-100, 260),
  ('TDS70000044','TDS','A','Inconel 625 Overlay Technical Datasheet',        'Carla Reis', 'Released',-230, -10),
  ('LST70000005','LST','C','Controlled Document List, Manufacturing',        'Ana Duarte', 'Released', -60, 300)
AS v(DOC_NO, DOC_TYPE, REVISION, TITLE, OWNER, STATUS, REL_OFF, REVIEW_OFF);

/* ------------------------------------------------------------------ */
TRUNCATE TABLE TC_ECNS;
INSERT INTO TC_ECNS (ECN_NO, TITLE, REASON, STATUS, CREATED_AT, RELEASED_AT)
SELECT v.ECN_NO, v.TITLE, v.REASON, v.STATUS,
       DATEADD(day, v.CREATED_OFF, $ANCHOR), DATEADD(day, v.REL_OFF, $ANCHOR)
FROM VALUES
  ('ECN70000042','Revise cladding preparation acceptance criteria','Field feedback on overlay porosity limits',        'Released', -95, -75),
  ('ECN70000051','Update valve block machining datum scheme',      'Fixture redesign after first-article findings',     'Released', -90, -70),
  ('ECN70000063','Increase overlay thickness on header pipe bore', 'Erosion allowance for high-sand service',           'Released', -80, -58),
  ('ECN70000070','Add hydrostatic hold-time requirement',          'Client specification update',                       'In Review',-25,NULL),
  ('ECN70000078','Replace hub connector seal groove profile',      'Supplier changed the seal',                         'Released', -62, -40),
  ('ECN70000085','Manifold frame weld sequence change',            'Distortion control after welding',                  'In Work',  -12,NULL)
AS v(ECN_NO, TITLE, REASON, STATUS, CREATED_OFF, REL_OFF);

/* ------------------------------------------------------------------ */
TRUNCATE TABLE TC_ECN_AFFECTED_ITEMS;
INSERT INTO TC_ECN_AFFECTED_ITEMS (ECN_NO, ITEM_NO, ITEM_TYPE, FROM_REV, TO_REV) VALUES
  ('ECN70000042','SWI70000318','Document',   'B','C'),
  ('ECN70000051','P7000001042','Part',       'B','C'),
  ('ECN70000051','DU700001042','Drawing',    'B','C'),
  ('ECN70000051','T7000000217','CNC Program','A','B'),
  ('ECN70000063','P7000001071','Part',       'A','B'),
  ('ECN70000063','DU700001071','Drawing',    'A','B'),
  ('ECN70000070','SWI70000402','Document',   'C','D'),
  ('ECN70000078','P7000001088','Part',       'C','D'),
  ('ECN70000078','DU700001088','Drawing',    'C','D'),
  ('ECN70000078','T7000000231','CNC Program','C','D'),
  ('ECN70000085','P7000001125','Part',       'B','C'),
  ('ECN70000085','DU700001125','Drawing',    'B','C');

SELECT 'Teamcenter data seeded. Next: 04_seed_quality_fat.sql' AS STATUS;
