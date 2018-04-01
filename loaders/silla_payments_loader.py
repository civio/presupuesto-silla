# -*- coding: UTF-8 -*-
import datetime
import re

from budget_app.loaders import PaymentsLoader
from budget_app.models import Budget

class SillaPaymentsLoader(PaymentsLoader):

    # take the year into account
    def load(self, entity, year, path):
        self.year = year
        PaymentsLoader.load(self, entity, year, path)

    # Parse an input line into fields
    def parse_item(self, budget, line):

        # Programme codes have changed in 2015, due to new laws. Since the application expects a code-programme
        # mapping to be constant over time, we are forced to amend budget data prior to 2015.
        # See https://github.com/dcabo/presupuestos-aragon/wiki/La-clasificaci%C3%B3n-funcional-en-las-Entidades-Locales
        programme_mapping = {
            # old programme: new programme
            '1550': '1532',     # Vías públicas
            '1540': '1521',     # Agencia de la vivienda
            '1551': '1531',     # Obras
            '1611': '1600',     # Alcantarillado y tratamiento de aguas
            '1620': '1630',     # Limpieza viaria
            '1720': '1721',     # Protección y mejora medio ambiente
            '2111': '2211',     # Segur. protec. y prom. soc.
            '2300': '2310',     # Asistencia social
            '2320': '2315',     # Departamento de la mujer
            '2321': '2316',     # Centro de día para menores
            '2322': '2318',     # Educador de Calle
            '2323': '2313',     # Prevención drogodependencias
            '2324': '2314',     # Entidades no lucrativas
            '2325': '2314',     # Entidades no lucrativas
            '2330': '2312',     # Asistencia domiciliaria
            '2331': '2319',     # Ayuda a la dependencia
            '3130': '3110',     # Medicamentos y prod sanitarios
            '3131': '3111',     # Salud Pública
            '3132': '3112',     # Desinfeccion y desratización
            '3133': '3113',     # Ciudades sanas
            '3134': '3121',     # Servicio Médico
            '3210': '3230',     # Enseñanza Preescolar
            '3211': '3231',     # Enseñanza Primaria
            '3240': '3262',     # Becas estudios
            '3241': '3263',     # Becas comedor
            '3242': '3264',     # Gabinete psicopedagógico
            '3243': '3265',     # OOAA Conservatorio Música
            '3350': '3330',     # Escuela de teatro
            '3351': '3331',     # Representaciones teatrales
            '4310': '4312',     # Mercados, abastos y lonjas
        }

        # Programme codes have changed also in 2010. We are forced to amend budget data prior to 2010
        # in order to mantain the code-programme mapping constant.
        programme_mapping_2010 = {
            # old programme: new programme
            '0112': '0112',     # Entitats Financeres
            '0115': '0112',     # Entitats Financeres
            '1110': '9120',     # Organs de Govern
            '1111': '9121',     # Grups Politics
            '1112': '9120',     # Organs de Govern
            '1113': '4911',     # Gabinet de comunicació
            '1114': '9120',     # Òrgans de Govern
            '1210': '9200',     # Serveis Generals
            '1211': '9201',     # Secretaria
            '1212': '9202',     # Oficines Municipals
            '1213': '9203',     # Edificis Municipals
            '1214': '4920',     # Societat de la informació
            '1214': '9204',     # Societat de la informació
            '1215': '9203',     # Magatzem
            '1216': '9206',     # Bens Municipals
            '1217': '9207',     # Jutjat
            '1218': '9292',     # Taller
            '1219': '9209',     # Departament de Personal
            '1230': '9205',     # Aseso. i defensa lletrada
            '1240': '9209',     # Oposicions i concursos
            '2220': '1320',     # Policia Local
            '2221': '1330',     # Control de Tràfic
            '2222': '1331',     # Recollida de vehicles
            '3110': '2210',     # Segurs Socials
            '3120': '2210',     # Personal Actiu
            '3121': '2211',     # Segure., protecc. i prom.
            '3130': '2330',     # Asistència Domiciliaria
            '3131': '2311',     # Acció Social
            '3132': '2300',     # Asistència Social
            '3133': '2320',     # Departament de la Dona
            '3135': '3379',     # Associacio de Jubilats
            '3136': '3379',     # Centre Tercera Edat
            '3139': '2321',     # Centre dia per a menors
            '3210': '2322',     # Educador de Carrer
            '3220': '2410',     # Escola Taller
            '3222': '2411',     # Ocupació
            '3223': '2411',     # Promoció Econòmica
            '3224': '2411',     # Ocupació
            '3230': '2324',     # Pau i solidaritat:immigra
            '3233': '2323',     # Prevenció Drogodependenc.
            '4110': '3133',     # Salut pública
            '4120': '3134',     # Servei Mèdic
            '4131': '3131',     # Servei Recollida Gossos
            '4132': '3132',     # Desinfeccio i Desratitza.
            '4134': '3133',     # Ciutats sanes
            '4220': '3211',     # Col.legis E.G.B.
            '4221': '3200',     # Ponencia d'Educació
            '4221': '3211',     # Ponencia d'Educació
            '4223': '3261',     # Escola Permanent d'Adults
            '4226': '3243',     # OOAA Conservatori Música
            '4230': '3242',     # Gabinet Psicopedagògic
            '4260': '2317',     # Menjador Escolar
            '4260': '3241',     # Menjador Escolar
            '4310': '9203',     # Edificis Corporació
            '4312': '1510',     # Agencia de l'habitatge
            '4314': '1510',     # Pla especial rehabilitaci
            '4320': '1510',     # Urbanisme
            '4321': '1551',     # Obres
            '4322': '1510',     # Urbanisme i Arquitectura
            '4323': '1330',     # Senyalit. vert. i horitz
            '4340': '1650',     # Enllumenat Públic
            '4341': '1650',     # Altres Conexions
            '4342': '1650',     # Enllumenta Públic
            '4351': '1700',     # Parcs i Jardins
            '4352': '1700',     # Parcs i Jardins
            '4410': '1610',     # Servei d'Aigua Potable
            '4411': '1611',     # Clavegueram i Vessam.Aigu
            '4413': '1611',     # Font del Manano
            '4420': '1620',     # Recollida Fem i Net.viari
            '4422': '1620',     # Tractament Residus Solids
            '4424': '1620',     # Cancel.lació deute EMTRE
            '4430': '1640',     # Cementeri Municipal
            '4440': '1550',     # Vies Públiques
            '4441': '1551',     # Brigada Vies i Obres
            '4442': '1551',     # Obres i Serveis
            '4460': '1700',     # Medi Ambient
            '4461': '1550',     # Zones Degradades
            '4461': '4121',     # Zones Degradades
            '4470': '4930',     # O.M.I.C.
            '4480': '4310',     # Mercat Municipal
            '4510': '3320',     # Biblioteques i Arxius
            '4511': '3343',     # Campanya Animació lectura
            '4512': '3344',     # Projectes cultur. Europeu
            '4513': '3243',     # OOAA Conservatori Música
            '4514': '3350',     # Escola de Teatre
            '4515': '3300',     # Animador Cultural
            '4516': '3340',     # Ponència de Cultura
            '4517': '3341',     # Casa de la Cultura
            '4518': '3370',     # Ponencia de Joventut
            '4519': '3347',     # Promocio d'Us Valencia
            '4520': '3420',     # Piscina Municipal
            '4521': '3421',     # Polisportiu Municipal
            '4522': '3410',     # Ponencia d'Esports
            '4531': '3360',     # Prot. Patrimoni  Hist-art
            '4540': '3380',     # Festes
            '4610': '3345',     # Bandes de Música
            '4631': '4910',     # Mitjans de comunicació
            '4640': '3380',     # Junta Local Fallera
            '4641': '3380',     # Comissions falles
            '4650': '2311',     # Entitats no Lucratives
            '4651': '3371',     # Consell Local de Joventut
            '4653': '2324',     # Pau i solidaritat: ONG
            '5110': '1550',     # Vies Publiques
            '5111': '1550',     # Vies Publiques
            '5112': '1550',     # vies Publiques
            '5120': '1611',     # Recursos Hidraulics
            '5310': '4190',     # Pla Ecològic ramad. agric
            '5330': '1700',     # Millora Medi Natural
            '6110': '9310',     # Serveis Econòmics
            '6113': '9320',     # Recaptació
            '6220': '4311',     # Fira Sant Sebastià
            '6320': '9240',     # Participació Ciutadana
            '7110': '4100',     # Consell Local Agrari
            '7111': '4190',     # Guarderia Rural
            '7310': '1650',     # Energia electrica
            '9112': '9420',     # Federació Municipis
            '9114': '9430',     # Mancomunitat L'Horta Sud
            '9116': '9430',     # Cancel.lacio deute Mancom
            '9210': '9291',     # Indemnitzacions A. Publiq
        }

        # Programme codes have changed also in 2010. We are forced to amend budget data prior to 2010
        # in order to mantain the code-programme mapping constant, although the mapping goes from
        # pre-2010 to pre-2015.
        fc_code = line[1].strip().rjust(4, '0') # We need four digits, including leading zeroes
        year = self.year
        if int(year) < 2010:
            fc_code = programme_mapping_2010.get(fc_code, fc_code)
        if int(year) < 2015:
            fc_code = programme_mapping.get(fc_code, fc_code)

        policy_id = fc_code[:2] # First two digits of the programme make the policy id
        # But what we want as area is the policy description
        policy = Budget.objects.get_all_descriptions(budget.entity)['functional'][policy_id]

        date = line[6].strip()

        # Normalize payee data
        # remove triling spaces
        payee = line[9].strip()
        # default value
        payee = ("Varios" if payee == "" else payee)
        # remove commas
        payee = payee.replace(', ', ' ').replace(',', ' ')
        # remove extra spaces
        payee = re.sub('\s\s+', ' ', payee)
        # normalize company types
        payee = re.sub(r'CB$', 'C.B.', payee)
        payee = re.sub(r'SL$', 'S.L.', payee)
        payee = re.sub(r'SLL$', 'S.L.L.', payee)
        payee = re.sub(r'SL.L.$', 'S.L.L.', payee)
        payee = re.sub(r'SLU$', 'S.L.U.', payee)
        payee = re.sub(r'SA$', 'S.A.', payee)
        payee = re.sub(r'SAU$', 'S.A.U.', payee)
        # titleize to avoid all caps
        payee = self._titlecase(payee)
        # put small words in lower case
        payee = re.sub(r' E ', ' e ', payee)
        payee = re.sub(r' I ', ' i ', payee)
        payee = re.sub(r' Y ', ' y ', payee)
        payee = re.sub(r' D\'', ' d\'', payee)
        payee = re.sub(r' De ', ' de ', payee)
        payee = re.sub(r' Del ', ' del ', payee)
        payee = re.sub(r' La ', ' la ', payee)
        payee = re.sub(r' Lo ', ' lo ', payee)
        payee = re.sub(r' En ', ' en ', payee)
        # put abbreviatons in upper case
        payee = re.sub(r'^A i C ', 'A.I.C. ', payee)
        payee = re.sub(r'^Mrw ', 'MRW ', payee)
        payee = re.sub(r'^Ute ', 'UTE ', payee)
        payee = re.sub(r'^Mhp ', 'MHP ', payee)
        payee = re.sub(r' Xxi ', ' XXI ', payee)
        # amend remaining
        payee = re.sub(r'^Assoc\.Jubilats i Pensioni$', u'Associació Jubilats i Pensionistes', payee)
        payee = re.sub(r'^Ros Marti Lluis$', u'Ros Martí Lluis', payee)
        payee = re.sub(r'^Parroquia San Roque$', 'Parroquia San Roque de Silla', payee)
        payee = re.sub(r'^Regidor/A$', 'Regidor/Regidora', payee)
        payee = re.sub(r'^Regidor/Regidora/La$', 'Regidor/Regidora', payee)
        payee = re.sub(r'^Serv\.Valencia D Ocupacio i Formacio \(Servef\)$', u'Servei Valencià d\'Ocupació i Formació (SERVEF)', payee)
        payee = re.sub(r'^Serv\.Valencia d\'Ocupacio i Formacio \(Servef\)$', u'Servei Valencià d\'Ocupació i Formació (SERVEF)', payee)
        payee = re.sub(r' Cont\.Admin ', u' Contenciós Administratiu ', payee)
        payee = re.sub(r' Cont\.Adm\.', u' Contenciós Administratiu Núm. ', payee)
        payee = re.sub(r' C-Adm ', u' Contenciós Administratiu ', payee)
        payee = re.sub(ur' C-Adv Nº 6$', u' Contenciós Administratiu Núm. 6 de València', payee)
        payee = re.sub(r' Contencios Admin\.6$', u' Contenciós Administratiu Núm. 6 de València', payee)
        payee = re.sub(r' Contencios Admin\. ', u' Contenciós Administratiu ', payee)
        payee = re.sub(r' Cont\.Advo ', u' Contenciós Administratiu Núm. ', payee)
        payee = re.sub(r' Numero ', u' Núm. ', payee)
        payee = re.sub(r' Num\.', u' Núm.', payee)
        payee = re.sub(ur' Núm ', u' Núm. ', payee)
        payee = re.sub(r' N\.1 ', u' Núm. 1 ', payee)
        payee = re.sub(r' Num\.(\d) ', u' Núm. \g<1> ', payee)
        payee = re.sub(ur' Núm\.(\d) ', u' Núm. \g<1> ', payee)
        payee = re.sub(ur' Núm\. 7$', u' Núm. 7 de València', payee)
        payee = re.sub(r' Contencios ', u' Contenciós ', payee)
        payee = re.sub(r'1 Inst\.Num\.2 Carlet$', u'de Primera Instància Núm. 2 de Carlet', payee)
        payee = re.sub(r'de Valencia$', u'de València', payee)
        payee = re.sub(r'(\d) Valencia$', u'\g<1> de València', payee)
        payee = re.sub(r'1O Valencia$', u'10 de València', payee)
        payee = re.sub(r'^Administracion General del Estado$', u'Administración General del Estado', payee)
        payee = re.sub(r'^Administracion del General Estado$', u'Administración General del Estado', payee)
        payee = re.sub(r'^Administracion del Estado$', u'Administración General del Estado', payee)
        payee = re.sub(r'^B.Santander Central Hispa$', 'Banco Santander Central Hispano', payee)
        payee = re.sub(r'^B.Santander Central Hispano$', 'Banco Santander Central Hispano', payee)
        payee = re.sub(r'^Banco de Santander S\.A\.$', 'Banco Santander Central Hispano', payee)
        payee = re.sub(r'^Banco Santander C\.H\. S\.A\.$', 'Banco Santander Central Hispano', payee)
        payee = re.sub(r'^Banco Bilbao Vizcaya$', 'Banco Bilbao Vizcaya Argentaria', payee)
        payee = re.sub(r'^Banco Bilbao Vizcaya Argentaria \(Bcl\)$', 'Banco Bilbao Vizcaya Argentaria', payee)
        payee = re.sub(r'^Banc Sabadell$', 'Banco de Sabadell', payee)
        payee = re.sub(r'^Banco de Sabadell S\.A\.$', 'Banco de Sabadell', payee)
        payee = re.sub(r'^Banco Sabadell Urb 243$', 'Banco de Sabadell', payee)
        payee = re.sub(r'^C\.A\.M\.$', u'Caja de Ahorros del Mediterráneo', payee)
        payee = re.sub(r'^C\.A\.M\. S\.A\.U\.$', u'Caja de Ahorros del Mediterráneo', payee)
        payee = re.sub(r'^C\.A\.M\. Sau Sabadellcam$', u'Caja de Ahorros del Mediterráneo', payee)
        payee = re.sub(r'^C\.A\.M\. sucursal 3130$', u'Caja de Ahorros del Mediterráneo', payee)
        payee = re.sub(r'^C\.A\.Mediterraneo$', u'Caja de Ahorros del Mediterráneo', payee)
        payee = re.sub(r'^Caja Ahorros Mediterraneo$', u'Caja de Ahorros del Mediterráneo', payee)
        payee = re.sub(r'^Caja Ahorros del Mediterraneo$', u'Caja de Ahorros del Mediterráneo', payee)
        payee = re.sub(r'^Caja de Ahorros del Mediterraneo$', u'Caja de Ahorros del Mediterráneo', payee)
        payee = re.sub(r'^C\.A\.M\.$', u'Caja de Ahorros del Mediterráneo', payee)
        payee = re.sub(r'^Caja de Rural Torrent$', 'Caja Rural de Torrent', payee)
        payee = re.sub(r'^Club Frontenis Incusa-Silla$', 'Club Frontenis Silla', payee)
        payee = re.sub(r'^Club Piraguisme$', u'Club Piragüisme Silla', payee)
        payee = re.sub(r'^Club Piraguismo Silla$', u'Club Piragüisme Silla', payee)
        payee = re.sub(r'^Cobo de Medina Juan Dios$', 'Cobo Medina Juan de Dios', payee)
        payee = re.sub(r'^Comercial y Derivados Ele$', 'Comercial y Derivados Electricos', payee)
        payee = re.sub(r'^Comunidad Propie\.V\.Aleixa$', 'Comunidad de Propietarios Vicente Aleixandre', payee)
        payee = re.sub(r'^Comunidad Propietaris Vicente Aleixandre$', 'Comunidad de Propietarios Vicente Aleixandre', payee)
        payee = re.sub(r'^Coop\.Agric\.La Union Silla$', u'Cooperativa Agricola La Unión de Silla', payee)
        payee = re.sub(r'^Coop\.Agricola V la Union Silla$', u'Cooperativa Agricola La Unión de Silla', payee)
        payee = re.sub(r'^Didactic Sport S\.L\.$', 'Didactic Esport S.L.', payee)
        payee = re.sub(r'^Diputacio de Valencia Bop$', u'Diputació de València', payee)
        payee = re.sub(ur'^Diputacio de València$', u'Diputació de València', payee)
        payee = re.sub(r'^Domenech Merin M\.Angeles$', 'Domenech Merin M Angeles', payee)
        payee = re.sub(r'^Encuadernaciones Ruiz$', 'Encuadernaciones Ruiz S.L.', payee)
        payee = re.sub(r'^Esquerra Unida del Pais V$', u'Esquerra Unida del Pais Valencià', payee)
        payee = re.sub(r'^Europea Servicio e Higien$', 'Europea de Servicio e Higiene S.A.', payee)
        payee = re.sub(r'^Europea Servicios Pub\.S\.A$', 'Europea de Servicio e Higiene S.A.', payee)
        payee = re.sub(r'^Farmacia Moliner Fernandez Luis V$', 'Farmacia Moliner Fernandez Luis V.', payee)
        payee = re.sub(r'^Farmacia Solanes Calatayud Inmacul$', 'Farmacia Solanes Calatayud Inmaculada', payee)
        payee = re.sub(r'^Farmacia Solanes Calatayud Maria I$', 'Farmacia Solanes Calatayud Inmaculada', payee)
        payee = re.sub(r'^Finsanzia Autorenting S\.A\.$', 'Finanzia Autorenting S.A.', payee)
        payee = re.sub(r'^Gas Natural Union Fenos\.A\.$', 'Gas Natural Union Fenosa S.A.', payee)
        payee = re.sub(r'^Gossos d\'Alpe S\.C\.$', 'Gossos Alpe S.C.', payee)
        payee = re.sub(r'^Els Verds$', 'Grup Els Verds de Silla', payee)
        payee = re.sub(r'^Iborra Ferradis Mayte$', 'Iborra Ferrandis Maria Teresa', payee)
        payee = re.sub(r'^Iborra Ferrandis Maria Teres\.A\.$', 'Iborra Ferrandis Maria Teresa', payee)
        payee = re.sub(r'^Innocarp$', 'Innocarp Stands S.L.', payee)
        payee = re.sub(ur'^Iranzo del Pontes Mª Pila$', u'Iranzo Pontes Mª Pilar', payee)
        payee = re.sub(ur'^Iranzo Pontes Mª [Dd]el Pila$', u'Iranzo Pontes Mª Pilar', payee)
        payee = re.sub(ur'^Jean[\s-]François Alberghi$', u'Alberghi Jean François', payee)
        payee = re.sub(r'^Jefatura Provincial Trafi$', u'Jefatura Provincial de Tráfico', payee)
        payee = re.sub(r'^Jefatura Provincial Trafico$', u'Jefatura Provincial de Tráfico', payee)
        payee = re.sub(r'^La Caixa A\. y Pens\.Barcel$', 'Caja de Ahorros y pensiones de Barcelona "La Caixa"', payee)
        payee = re.sub(r'^La Caixa A\. y Pens\.Barcelona$', 'Caja de Ahorros y pensiones de Barcelona "La Caixa"', payee)
        payee = re.sub(r'^Mapfre \(Seguros Generales$', 'Mapfre (Seguros Generales)', payee)
        payee = re.sub(r'^Mapfre Caucion y Credito$', 'Mapfre (Seguros Generales)', payee)
        payee = re.sub(r'^Mapfre Familiar S\.A\.$', 'Mapfre (Seguros Generales)', payee)
        payee = re.sub(r'^Mapfre S\.A\.$', u'Mapfre (Seguros Generales)', payee)
        payee = re.sub(r'^Mapfre Seguros de Empresas Cia de Seguros y Reaseguros S\.A$', 'Mapfre (Seguros Generales)', payee)
        payee = re.sub(r'^Mapfre Vida S\.A\.$', 'Mapfre (Seguros Generales)', payee)
        payee = re.sub(r'^Maq.Agric.Hernandez S\.L\.$', u'Maquinaria Agrícola Hernandez S.L.', payee)
        payee = re.sub(r'^Maquin.Agr.Hernandez S\.L\.$', u'Maquinaria Agrícola Hernandez S.L.', payee)
        payee = re.sub(r'^Mediterranea de Eventos Taurinos C\.B\.$', u'Mediterránea de Eventos Taurinos S.L', payee)
        payee = re.sub(r'^Mediterranea Eventos Taurinos S\.L\.$', u'Mediterránea de Eventos Taurinos S.L', payee)
        payee = re.sub(r'^Olivares Alfonso Teres\.A\.$', 'Olivares Alfonso Teresa (Papereria)', payee)
        payee = re.sub(r'^Olivares Alfonso Teresa \(Imprimax\)\.*', 'Olivares Alfonso Teresa (Papereria)', payee)
        payee = re.sub(ur'^Rentokil Initial España$', u'Rentokil Initial España S.A.', payee)
        payee = re.sub(ur'^Rentokil Initial España S$', u'Rentokil Initial España S.A.', payee)
        payee = re.sub(r'^Seguridad Social$', u'Seguridad Social Dirección Provincial Valencia', payee)
        payee = re.sub(r'^Seguridad Social Dir\. Prov\. Valencia$', u'Seguridad Social Dirección Provincial Valencia', payee)
        payee = re.sub(r'^Club Futbol Silla Atletic$', u'Silla Club de Futbol', payee)
        payee = re.sub(ur'^S\.Españ\.Radiodifusion S\.A$', u'Sociedad Española Radiodifusion S.L.', payee)
        payee = re.sub(ur'^Telefonica de España S\.A\.$', u'Telefónica de España S.A.', payee)
        payee = re.sub(ur'^Telefonica Moviles España$', u'Telefónica Moviles España S.A.', payee)
        payee = re.sub(r'^Trama de Gasllar S\.A\.$', 'Trama de Gasllar S.L.', payee)
        payee = re.sub(r'^Viversilla Coop\.Val\.$', 'Viver - Silla Coop. Valenciana', payee)
        payee = re.sub(r'^Viversilla Planta Ornamental S\.L\.$', 'Viversilla Planta Ornamental S.L.L.', payee)
        payee = re.sub(ur'^Vodafone España S\.A\.$', u'Vodafone España S.A.U.', payee)
        payee = re.sub(r'^Org Auton L Conservatori$', u'Organisme Autònom Conservatori de Música', payee)
        payee = re.sub(ur'^Organisme Autonom Conservatori de Música$', u'Organisme Autònom Conservatori de Música', payee)
        payee = re.sub(r'^Smax Sl \(Serv\.Medioamb\.Xilxes\)$', 'Servicios Medioambientales Xilxes S.L.', payee)
        payee = re.sub(r'Infraestruc Sau-', 'Infraestructuras S.A.U. - ', payee)
        payee = re.sub(r'Felisa\(Decojar\)', 'Felisa (Decojar)', payee)
        payee = re.sub(r'Comerc\.Ultimo', 'Comercial Ultimo', payee)
        payee = re.sub(r'^Objetivo Const\.Proyect\.S\.L\.$', 'Objetivo de Construcciones y Proyectos S.L.', payee)
        payee = re.sub(r'^Nominas en Formalizacion$', u'Nóminas en formalización', payee)
        payee = re.sub(r'Col\.Legi', 'Col.legi', payee)
        payee = re.sub(r'Col\.Lectiu', 'Col.lectiu', payee)
        payee = re.sub(r'^Ions\.A\.$', 'IONSA', payee)
        payee = re.sub(r'^UTE EIFFAGE INFra\.ESTRUC SAU-EIFFASE ENERGIA S\.L\.U\.$', 'UTE Eiffage Infraestructuras S.A.U. - Eiffase Energia S.L.U.', payee)
        payee = re.sub(r'Construc\.Machancoses', 'Construcciones Machancoses', payee)
        payee = re.sub(r' Frances ', u' Francés ', payee)
        payee = re.sub(r'^Aparicio Colomer Jose Antonio$', u'Aparicio Colomer José Antonio (Notari)', payee)
        payee = re.sub(r'^Aparicio Colomer Jose Antonio \(Notari\)$', u'Aparicio Colomer José Antonio (Notari)', payee)
        payee = re.sub(r'^Cajamar Caja Rural Sociedad Cooperativa de Credito$', u'Cajamar Caja Rural Sociedad Cooperativa de Crédito', payee)
        payee = re.sub(ur'^Cajamar Cajas Rurales Sociedad Cooperativa de Crèdito$', u'Cajamar Caja Rural Sociedad Cooperativa de Crédito', payee)
        payee = re.sub(r'^Cajamar Cajas Rurales Sociedad Cooperativa de Credito$', u'Cajamar Caja Rural Sociedad Cooperativa de Crédito', payee)
        payee = re.sub(r'^Covernat Sociedad Limitad$', 'Covernat Sociedad Limitada', payee)
        payee = re.sub(r'^Enti\.Metropolitana T\.Res\.$', 'Entitat Metropolitana de Tractament de Residus', payee)
        payee = re.sub(r'^Entidad Metropolitana para el Tratamiento de Residuos$', 'Entitat Metropolitana de Tractament de Residus', payee)
        payee = re.sub(r'^Entitat Metropolitana Tractament de Residus$', 'Entitat Metropolitana de Tractament de Residus', payee)
        payee = re.sub(r'^Jaime Mackintosh$', 'Mackintosh Gimeno Jaime', payee)
        payee = re.sub(r'^Jaime Machintosh$', 'Mackintosh Gimeno Jaime', payee)
        payee = re.sub(r'^Parroquia Ntra Sra de Los Angeles$', u'Parroquia Ntra Sra dels Àngels', payee)
        payee = re.sub(r'^Parroquia Ntra Sra Dels Angels$', u'Parroquia Ntra Sra dels Àngels', payee)
        payee = re.sub(r'^Parroquia Ntra\.Sra\.Dels Angels$', u'Parroquia Ntra Sra dels Àngels', payee)
        payee = re.sub(r'^Riera Brocal Carmen$', 'Riera Brocal Carmen (Papereria)', payee)
        payee = re.sub(r'^Correos y Telegrafos$', u'Correos y Telégrafos', payee)
        payee = re.sub(ur'^Aiu Ue-2 L\'Alteró$', u'AIU UE-2 L\'Alteró', payee)

        anonymized = (True if payee == 'Anonimizado' else False)

        description = self._spanish_titlecase(line[10].strip()[:300].decode('utf-8','ignore').encode('utf-8'))

        amount = self._read_english_number(line[7])

        return {
            'area': policy,
            'programme': None,
            'fc_code': None,  # We don't try (yet) to have foreign keys to existing records
            'ec_code': None,
            'date': date,
            'payee': payee,
            'anonymized': anonymized,
            'description': description,
            'amount': amount
        }
