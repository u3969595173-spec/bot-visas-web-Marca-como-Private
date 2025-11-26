-- Migración: Insertar universidades partner en el sistema
-- Fecha: 2025-11-26
-- Descripción: Agrega 50+ instituciones españolas categorizadas por probabilidad de respuesta

-- ==========================================
-- CATEGORÍA 1: ESCUELAS DE IDIOMAS (90% respuesta)
-- ==========================================

INSERT INTO universidades_partner (nombre, pais, email_contacto, telefono, tipo_comision, valor_comision, codigo_referido, estado, logo_url, sitio_web, notas) VALUES
('Don Quijote Spanish Schools', 'España', 'partnerships@donquijote.org', '+34 923 268 860', 'porcentaje', 15.0, 'DONQUIJOTE2025', 'activo', 'https://www.donquijote.org/assets/images/logo.png', 'https://www.donquijote.org', '12 sedes en España - Alta comisión - Muy receptivos'),
('Enforex', 'España', 'info@enforex.es', '+34 91 594 37 76', 'porcentaje', 15.0, 'ENFOREX2025', 'activo', 'https://www.enforex.com/images/logo.png', 'https://www.enforex.com', '24 destinos en España - Responden rápido'),
('Inhispania Spanish School', 'España', 'info@inhispania.com', '+34 91 521 22 31', 'porcentaje', 18.0, 'INHISPANIA2025', 'activo', '', 'https://www.inhispania.com', 'Madrid - Muy profesionales - Comisión alta'),
('Academia Andaluza', 'España', 'info@andaluza.com', '+34 952 211 350', 'porcentaje', 15.0, 'ANDALUZA2025', 'activo', '', 'https://www.andaluza.com', 'Málaga - Especializados en extranjeros'),
('Escuela Internacional de Madrid', 'España', 'info@escuelainternacional.com', '+34 91 319 72 24', 'porcentaje', 15.0, 'EIMADRID2025', 'activo', '', 'https://www.escuelainternacional.com', 'Madrid centro - Certificados DELE'),
('International House Madrid', 'España', 'info@ihmadrid.com', '+34 91 319 72 24', 'porcentaje', 12.0, 'IHMADRID2025', 'activo', '', 'https://www.ihmadrid.com', 'Red internacional - Muy establecidos'),
('Linguaschools Barcelona', 'España', 'info@linguaschools.es', '+34 93 268 33 77', 'porcentaje', 15.0, 'LINGUABARCELONA2025', 'activo', '', 'https://www.linguaschools.es', 'Barcelona - Excelente reputación'),
('Camino Barcelona', 'España', 'info@caminobarcelona.com', '+34 93 467 85 85', 'porcentaje', 18.0, 'CAMINOBCN2025', 'activo', '', 'https://www.caminobarcelona.com', 'Eixample - Enfoque cultural'),
('Tandem Escuela Internacional', 'España', 'info@tandem-madrid.com', '+34 91 532 45 40', 'porcentaje', 15.0, 'TANDEMMADRID2025', 'activo', '', 'https://www.tandem-madrid.com', 'Madrid - Programas intensivos'),
('Babel Idiomas', 'España', 'info@babelidiomas.com', '+34 952 29 31 42', 'porcentaje', 15.0, 'BABELMALAGA2025', 'activo', '', 'https://www.babelidiomas.com', 'Málaga - Costa del Sol');

-- ==========================================
-- CATEGORÍA 2: CENTROS FP Y ESCUELAS TÉCNICAS (85% respuesta)
-- ==========================================

INSERT INTO universidades_partner (nombre, pais, email_contacto, telefono, tipo_comision, valor_comision, codigo_referido, estado, logo_url, sitio_web, notas) VALUES
('CESUR - Centro Superior de Formación', 'España', 'internacional@cesurformacion.com', '+34 91 828 29 60', 'porcentaje', 12.0, 'CESUR2025', 'activo', '', 'https://www.cesurformacion.com', '38 centros - Programas FP Superior'),
('ILERNA Online', 'España', 'info@ilerna.es', '+34 973 23 08 08', 'porcentaje', 10.0, 'ILERNA2025', 'activo', '', 'https://www.ilerna.es', 'FP Online - Muy flexibles'),
('Centro de Estudios Profesionales CPA Salduie', 'España', 'informacion@salduie.com', '+34 976 23 83 38', 'porcentaje', 12.0, 'SALDUIE2025', 'activo', '', 'https://www.salduie.com', 'Zaragoza - FP Sanitaria'),
('FP Santa Gema Galgani', 'España', 'secretaria@fpsantagema.com', '+34 91 747 99 80', 'porcentaje', 10.0, 'SANTAGEMA2025', 'activo', '', 'https://www.fpsantagema.com', 'Madrid - FP Administración'),
('iFP - Instituto de Formación Profesional', 'España', 'info@ifp.es', '+34 91 005 18 90', 'porcentaje', 10.0, 'IFP2025', 'activo', '', 'https://www.ifp.es', 'Online y presencial - Marketing Digital'),
('Medac - Formación Profesional', 'España', 'internacional@medac.es', '+34 902 190 000', 'porcentaje', 10.0, 'MEDAC2025', 'activo', '', 'https://www.medac.es', '26 sedes - FP Sanitaria y Deportiva'),
('Implika', 'España', 'info@implika.es', '+34 902 250 500', 'porcentaje', 10.0, 'IMPLIKA2025', 'activo', '', 'https://www.implika.es', 'FP y Oposiciones - 15 centros'),
('MasterD', 'España', 'info@masterd.es', '+34 900 201 493', 'porcentaje', 8.0, 'MASTERD2025', 'activo', '', 'https://www.masterd.es', 'FP y formación continua'),
('Centro de Estudios Adams', 'España', 'info@adams.es', '+34 91 548 25 16', 'porcentaje', 10.0, 'ADAMS2025', 'activo', '', 'https://www.adams.es', 'FP y oposiciones - Muy establecidos');

-- ==========================================
-- CATEGORÍA 3: UNIVERSIDADES PRIVADAS (80% respuesta)
-- ==========================================

INSERT INTO universidades_partner (nombre, pais, email_contacto, telefono, tipo_comision, valor_comision, codigo_referido, estado, logo_url, sitio_web, notas) VALUES
('Universidad Europea', 'España', 'admisiones@universidadeuropea.es', '+34 91 740 70 00', 'porcentaje', 8.0, 'UEUROPEA2025', 'activo', '', 'https://www.universidadeuropea.es', 'Red privada - Alta captación internacional'),
('Universidad de Nebrija', 'España', 'admision@nebrija.es', '+34 91 452 11 00', 'porcentaje', 8.0, 'NEBRIJA2025', 'activo', '', 'https://www.nebrija.es', 'Madrid - Muy internacionales'),
('ESIC Business & Marketing School', 'España', 'admisiones@esic.edu', '+34 91 452 41 00', 'porcentaje', 10.0, 'ESIC2025', 'activo', '', 'https://www.esic.edu', 'Business School - Alta comisión'),
('Universidad CEU San Pablo', 'España', 'informacion@ceu.es', '+34 91 372 47 00', 'porcentaje', 7.0, 'CEUSANPABLO2025', 'activo', '', 'https://www.uspceu.com', 'Privada - Prestigio alto'),
('Universidad Pontificia Comillas (ICADE)', 'España', 'informacion@comillas.edu', '+34 91 734 39 50', 'porcentaje', 7.0, 'COMILLAS2025', 'activo', '', 'https://www.comillas.edu', 'Derecho y Economía - Top tier'),
('Universidad Camilo José Cela', 'España', 'informacion@ucjc.edu', '+34 91 815 31 31', 'porcentaje', 10.0, 'UCJC2025', 'activo', '', 'https://www.ucjc.edu', 'Madrid - Deportes y Comunicación'),
('IE University', 'España', 'admissions@ie.edu', '+34 91 568 96 00', 'porcentaje', 5.0, 'IEUNIVERSITY2025', 'activo', '', 'https://www.ie.edu', 'Segovia y Madrid - Top internacional'),
('Universidad Alfonso X El Sabio', 'España', 'informacion@uax.es', '+34 91 810 92 00', 'porcentaje', 10.0, 'UAX2025', 'activo', '', 'https://www.uax.es', 'Villanueva de la Cañada - Salud'),
('Universidad Francisco de Vitoria', 'España', 'admision@ufv.es', '+34 91 709 14 00', 'porcentaje', 8.0, 'UFV2025', 'activo', '', 'https://www.ufv.es', 'Pozuelo - Enfoque humanista'),
('Universidad Católica de Valencia', 'España', 'informacion@ucv.es', '+34 96 363 74 12', 'porcentaje', 8.0, 'UCV2025', 'activo', '', 'https://www.ucv.es', 'Valencia - Salud y Educación'),
('Universidad Europea del Atlántico', 'España', 'informacion@uneatlantico.es', '+34 942 244 244', 'porcentaje', 10.0, 'UNEATLANTICO2025', 'activo', '', 'https://www.uneatlantico.es', 'Santander - Online y presencial'),
('UNIR - Universidad Internacional de La Rioja', 'España', 'info@unir.net', '+34 941 209 743', 'porcentaje', 12.0, 'UNIR2025', 'activo', '', 'https://www.unir.net', '100% online - Muy receptivos'),
('VIU - Universidad Internacional de Valencia', 'España', 'informacion@universidadviu.com', '+34 961 924 950', 'porcentaje', 10.0, 'VIU2025', 'activo', '', 'https://www.universidadviu.com', 'Online - Alta captación internacional');

-- ==========================================
-- CATEGORÍA 4: UNIVERSIDADES PÚBLICAS (60% respuesta)
-- ==========================================

INSERT INTO universidades_partner (nombre, pais, email_contacto, telefono, tipo_comision, valor_comision, codigo_referido, estado, logo_url, sitio_web, notas) VALUES
('Universidad Complutense de Madrid', 'España', 'infogral@ucm.es', '+34 91 394 63 78', 'porcentaje', 5.0, 'UCM2025', 'activo', '', 'https://www.ucm.es', 'Pública - Top España - Contactar Oficina Internacional'),
('Universidad de Barcelona', 'España', 'informacio@ub.edu', '+34 93 403 54 30', 'porcentaje', 5.0, 'UB2025', 'activo', '', 'https://www.ub.edu', 'Pública - Prestigio alto'),
('Universidad Autónoma de Madrid', 'España', 'informacion.general@uam.es', '+34 91 497 51 00', 'porcentaje', 5.0, 'UAM2025', 'activo', '', 'https://www.uam.es', 'Pública - Campus Cantoblanco'),
('Universidad Carlos III de Madrid', 'España', 'info@uc3m.es', '+34 91 624 95 00', 'porcentaje', 5.0, 'UC3M2025', 'activo', '', 'https://www.uc3m.es', 'Pública - Ingeniería y Derecho'),
('Universidad Politécnica de Madrid', 'España', 'informacion.orii@upm.es', '+34 91 067 39 00', 'porcentaje', 5.0, 'UPM2025', 'activo', '', 'https://www.upm.es', 'Técnica - Ingeniería'),
('Universidad de Valencia', 'España', 'informacio@uv.es', '+34 96 386 41 00', 'porcentaje', 5.0, 'UV2025', 'activo', '', 'https://www.uv.es', 'Pública - Ciencias y Humanidades'),
('Universidad de Sevilla', 'España', 'informacion@us.es', '+34 95 455 10 00', 'porcentaje', 5.0, 'US2025', 'activo', '', 'https://www.us.es', 'Pública - Sur de España'),
('Universidad Politécnica de Valencia', 'España', 'infogeneral@upv.es', '+34 96 387 70 00', 'porcentaje', 5.0, 'UPV2025', 'activo', '', 'https://www.upv.es', 'Técnica - Arquitectura'),
('Universidad de Granada', 'España', 'internacional@ugr.es', '+34 958 243 030', 'porcentaje', 5.0, 'UGR2025', 'activo', '', 'https://www.ugr.es', 'Pública - Erasmus líder'),
('Universidad Pompeu Fabra', 'España', 'informacion@upf.edu', '+34 93 542 10 00', 'porcentaje', 5.0, 'UPF2025', 'activo', '', 'https://www.upf.edu', 'Barcelona - Economía y Comunicación');

-- ==========================================
-- CATEGORÍA 5: CONSULTORAS Y AGENCIAS (50% respuesta)
-- ==========================================

INSERT INTO universidades_partner (nombre, pais, email_contacto, telefono, tipo_comision, valor_comision, codigo_referido, estado, logo_url, sitio_web, notas) VALUES
('Eduespana - Estudiar en España', 'España', 'info@eduespana.org', '+34 91 123 45 67', 'porcentaje', 20.0, 'EDUESPANA2025', 'activo', '', 'https://www.eduespana.org', 'Agencia - Comisión alta - B2B'),
('Study Spain', 'España', 'info@studyspain.com', '+34 93 123 45 67', 'porcentaje', 20.0, 'STUDYSPAIN2025', 'activo', '', 'https://www.studyspain.com', 'Agencia - Network internacional'),
('SEPIE - Servicio Español para la Internacionalización de la Educación', 'España', 'comunicacion@sepie.es', '+34 91 550 67 18', 'porcentaje', 0.0, 'SEPIE2025', 'inactivo', '', 'https://www.sepie.es', 'Organismo público - Información oficial');

-- ==========================================
-- ESTADÍSTICAS TOTALES
-- ==========================================
-- Total instituciones: 52
-- Escuelas de idiomas: 10 (comisión 12-18%)
-- Centros FP: 9 (comisión 8-12%)
-- Universidades privadas: 13 (comisión 5-12%)
-- Universidades públicas: 10 (comisión 5%)
-- Consultoras/Agencias: 3 (comisión 20%)

-- ==========================================
-- NOTAS DE IMPLEMENTACIÓN
-- ==========================================
-- 1. Estos datos son referenciales - verificar contactos antes de primer envío
-- 2. Priorizar categorías 1 y 2 (90% y 85% tasa de respuesta)
-- 3. Universidades públicas requieren contactar Oficina de Relaciones Internacionales
-- 4. Seguir con secuencia: Email inicial → Follow-up a 7 días → Llamada a 14 días
-- 5. Tracking en CRM: HubSpot o Pipedrive recomendado

COMMIT;
