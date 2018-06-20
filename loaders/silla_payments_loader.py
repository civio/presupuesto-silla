# -*- coding: UTF-8 -*-
from budget_app.loaders import PaymentsLoader
from budget_app.models import Budget

from silla_budget_loader import programme_mapping
from silla_budget_loader import programme_mapping_2010

import re


payments_mapping = {
    'default': {'fc_code': 1, 'date': 6, 'payee': 9, 'description': 10, 'amount': 7},
    '2009': {'fc_code': 1, 'date': 7, 'payee': 10, 'description': 11, 'amount': 8},
    '2010': {'fc_code': 1, 'date': 7, 'payee': 10, 'description': 11, 'amount': 8},
    '2011': {'fc_code': 1, 'date': 7, 'payee': 10, 'description': 11, 'amount': 8},
    '2013': {'fc_code': 1, 'date': 5, 'payee': 9, 'description': 10, 'amount': 6},
    '2018': {'fc_code': 1, 'date': 5, 'payee': 8, 'description': 9, 'amount': 6},
}


class PaymentsCsvMapper:
    def __init__(self, year):
        mapping = payments_mapping.get(str(year))

        if not mapping:
            mapping = payments_mapping.get('default')

        self.fc_code = mapping.get('fc_code')
        self.date = mapping.get('date')
        self.payee = mapping.get('payee')
        self.description = mapping.get('description')
        self.amount = mapping.get('amount')


class SillaPaymentsLoader(PaymentsLoader):
    # An artifact of the in2csv conversion of some of the original XLS files is
    # a trailing '.0', which we remove here
    def clean(self, s):
        return s.split('.')[0]

    # Parse an input line into fields
    def parse_item(self, budget, line):
        # Mapper
        mapper = PaymentsCsvMapper(budget.year)

        # Functional code
        # We got 3- or 4- digit functional codes as input, as leading zeroes are missing
        fc_code = line[mapper.fc_code].strip()
        fc_code = self.clean(fc_code)
        fc_code = fc_code.rjust(4, '0')

        # We need to apply the programme mappings here because in some cases the policy in the old and
        # new codes is different.
        if budget.year < 2010:
            fc_code = programme_mapping_2010.get(fc_code, fc_code)
        if budget.year < 2015:
            fc_code = programme_mapping.get(fc_code, fc_code)

        # first two digits of the functional code make the policy id
        policy_id = fc_code[:2]

        # but what we want as area is the policy description
        policy = Budget.objects.get_all_descriptions(budget.entity)['functional'][policy_id]

        # We got an iso date
        date = line[mapper.date].strip()

        # Payee data
        payee = line[mapper.payee].strip()
        default_payee = ('Diversos' if budget.entity_id == 1 else 'Varios')
        anonymized_payee = ('Anonimitzat' if budget.entity_id == 1 else 'Anonimizado')

        # default value
        if payee == "":
            payee = default_payee

        # anoniymized
        elif re.search('Anonimizado', payee):
            payee = anonymized_payee

        else:
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

        # We got some anonymized entries
        anonymized = (True if payee == anonymized_payee else False)

        # Description
        # We got some texts that exceed the maximum field size and that include
        # some unsupported chars.
        description = line[mapper.description].strip()
        description = description[:300].decode('utf-8', 'ignore').encode('utf-8')
        description = self._spanish_titlecase(description)

        # Amount
        amount = line[mapper.amount]
        amount = self._read_english_number(amount)

        return {
            'area': policy,
            'programme': None,
            'fc_code': None,  # We don't try (yet) to have foreign keys to existing records
            'ec_code': None,
            'ic_code': None,
            'date': date,
            'payee': payee,
            'anonymized': anonymized,
            'description': description,
            'amount': amount
        }
