# -*- coding: UTF-8 -*-
from budget_app.loaders import SimpleBudgetLoader


expenses_mapping = {
    'default': {'ic_code': None, 'fc_code': 1, 'full_ec_code': 2, 'description': 4, 'forecast_amount': 7, 'actual_amount': 10},
    '2017': {'ic_code': None, 'fc_code': 1, 'full_ec_code': 2, 'description': 4, 'forecast_amount': 8, 'actual_amount': 11},
    '2018': {'ic_code': None, 'fc_code': 2, 'full_ec_code': 4, 'description': 6, 'forecast_amount': 9, 'actual_amount': 12},
}

income_mapping = {
    'default': {'full_ec_code': 1, 'description': 3, 'forecast_amount': 4, 'actual_amount': 7},
}

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
    '3230': '3261',     # Escola Permanent d'Adults
    '3240': '3262',     # Becas estudios
    '3241': '3263',     # Becas comedor
    '3242': '3264',     # Gabinete psicopedagógico
    '3243': '3265',     # OOAA Conservatorio Música
    '3350': '3330',     # Escuela de teatro
    '3351': '3331',     # Representaciones teatrales
    '4310': '4312',     # Mercados, abastos y lonjas
}

# Programme codes have changed also in 2010. We are forced to amend budget data prior to 2010
# in order to mantain the code-programme mapping constant, although the mapping goes from
# pre-2010 to pre-2015.
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

# Income economic codes have changed in 2010. We are forced to amend budget data prior
# to 2010 in order to mantain the code-programme mapping constant.
income_economic_mapping_2010 = {
    '11201': '11300',   # De naturalesa urbana
    '11300': '11500',   # Vehicles tracció mecànica
    '11400': '11600',   # Incr. valor terrenys urb.
    '28200': '29000',   # Sobre construcc. i obres
    '31000': '32500',   # Taxa exped docum. aminis.
    '31001': '32900',   # Taxa llic. obert. establi
    '31002': '30900',   # Taxa servei cementeri
    '31004': '32600',   # Taxa serv.retir.vehicles
    '31005': '31300',   # Taxa utiliz.polispostiu
    '31007': '32900',   # Taxa util.locals serv.pub
    '31101': '30200',   # Taxa servei recoll. fem
    '31102': '33400',   # Taxa oc.sub.sol vol obres
    '31103': '33900',   # Taxa ocup. mercat i feste
    '31104': '33500',   # Taxa ocup taules-cadires
    '31105': '33901',   # Taxa ocup. fira S.Sebasti
    '31106': '33200',   # Taxa electr. gas i telefo
    '31200': '32100',   # Taxa llicencies urbanisti
    '31201': '30100',   # Taxa servei clavegueram
    '31202': '33100',   # Taxa entrada vehi. vorere
    '32000': '31301',   # Tasa util.inst. piscina
    '34001': '34200',   # P.P.Act.Cult.i esp.EPA
    '34002': '34203',   # P.P.Ac.Cult. Esc.Matinera
    '34003': '34201',   # P.P.Ac.Cult.Escola Estiu
    '34004': '34202',   # P.P.Ac.Cult. Camp. Estiu
    '34005': '34400',   # P.P.Ac.Educ. i Esp.Teatre
    '34200': '30000',   # Taxa servei subm. d'aigua
    '36000': '35000',   # Contribucions especials
    '38000': '38900',   # De pressupostos tancats
    '38101': '38901',   # Reintegrament Estat i S.S
    '38803': '38903',   # Reinteg.prom.vivendes VPO
    '39101': '39120',   # Multes i sancions
    '39201': '39200',   # Recarrecs prorrog. i cons
    '39902': '39610',   # Quotes urbanistiques
    '39905': '39909',   # Imprevistos
    '39908': '32200',   # Taxa Cedules Habitabilit.
    '39909': '33800',   # Canon C.T.N.E.
    '42001': '42090',   # Subvencions de l'Estat
    '42300': '42100',   # Aportacions  I.N.E.M.
    '45500': '45080',   # Subvencions Generalitat
    '46200': '46100',   # Subvencions Diputacio
    '52100': '52000',   # Int. Diposits ent. Bancar
    '55000': '54100',   # Concesions administrativ.
    '55001': '55100',   # Cessio ninxols
    '75500': '75080',   # Subven. Generalitat Vcna.
    '76101': '76100',   # Aportacio Diputacio PPOS
    '87001': '87010',   # Aplic. financ. supl. cred
    '87002': '87010',   # Aplic.financ. incorp.cred
    '91701': '91300',   # Prestecs entitats financ.
}


class BudgetCsvMapper:
    def __init__(self, year, is_expense):
        column_mapping = income_mapping

        if is_expense:
            column_mapping = expenses_mapping

        mapping = column_mapping.get(str(year))

        if not mapping:
            mapping = column_mapping.get('default')

        self.ic_code = mapping.get('ic_code')
        self.fc_code = mapping.get('fc_code')
        self.full_ec_code = mapping.get('full_ec_code')
        self.description = mapping.get('description')
        self.forecast_amount = mapping.get('forecast_amount')
        self.actual_amount = mapping.get('actual_amount')


class SillaBudgetLoader(SimpleBudgetLoader):
    # make year data available in the class and call super
    def load(self, entity, year, path, status):
        self.year = year
        SimpleBudgetLoader.load(self, entity, year, path, status)

    def parse_item(self, filename, line):
        # Ignore invalid lines in input data
        if line[0] == '':
            return None

        # Type of data
        is_expense = (filename.find('gastos.csv') != -1)
        is_actual = (filename.find('/ejecucion_') != -1)

        # Mapper
        mapper = BudgetCsvMapper(self.year, is_expense)

        # Institutional code
        # All expenses go to the root node
        ic_code = '000'

        # Economic code
        # We got 3- or 5- digit economic codes as input, so we need to add trailing zeroes
        full_ec_code = line[mapper.full_ec_code].strip()
        full_ec_code = full_ec_code.ljust(5, '0')

        # Description
        description = line[mapper.description].strip()
        description = self._spanish_titlecase(description)

        # Parse amount
        amount = line[mapper.actual_amount if is_actual else mapper.forecast_amount]
        amount = self._parse_amount(amount)

        # Expenses
        if is_expense:
            # Functional code
            fc_code = line[mapper.fc_code].strip()

            # For years before 2010 and 2015 we check whether we need to amend the programme
            # codes, but the amends made for years before 2010 must be amended again for 2015
            # programme codes
            if int(self.year) < 2010:
                fc_code = programme_mapping_2010.get(fc_code, fc_code)
            if int(self.year) < 2015:
                fc_code = programme_mapping.get(fc_code, fc_code)

        # Income
        else:
            # Functional code
            # We don't have a functional code in income
            fc_code = None

            # For years before 2010 we check whether we need to amend the economic codes
            if int(self.year) < 2010:
                full_ec_code = income_economic_mapping_2010.get(full_ec_code, full_ec_code)

        # Concepts are the firts three digits from the economic codes
        ec_code = full_ec_code[:3]

        # Item numbers are the last two digits from the economic codes (fourth and fifth digits)
        item_number = full_ec_code[-2:]

        return {
            'is_expense': is_expense,
            'is_actual': is_actual,
            'fc_code': fc_code,
            'ec_code': ec_code,
            'ic_code': ic_code,
            'item_number': item_number,
            'description': description,
            'amount': amount
        }
