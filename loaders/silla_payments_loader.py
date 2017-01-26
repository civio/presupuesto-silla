# -*- coding: UTF-8 -*-
import datetime

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
            '1110': '9120',     # Órganos de gobierno
            '1111': '9121',     # Grupos Políticos
            '1112': '9120',     # Órganos de gobierno
            '1113': '9122',     # Gabinete de comunicación
            '1114': '9120',     # Órganos de gobierno
            '1210': '9200',     # Servicios Generales
            '1211': '9201',     # Secretaría
            '1212': '9202',     # Oficinas Municipales
            '1213': '9203',     # Edificios Municipales
            '1214': '9204',     # Departamento informática
            '1215': '9203',     # Edificios Municipales
            '1216': '9206',     # Bienes Municipales
            '1217': '9207',     # Juzgado
            '1218': '9292',     # Taller
            '1219': '9209',     # Departamento de Personal
            '1230': '9205',     # Asesoría y defensa letrada
            '1240': '9120',     # Órganos de gobierno
            '2220': '1320',     # Seguridad y orden público
            '2221': '1330',     # Control del tráfico
            '2222': '1331',     # Recogida de vehículos
            '3110': '2200',     # Otras prestaciones económicas a favor de empleados
            '3120': '2210',     # Personal activo
            '3130': '2312',     # Asistencia domiciliaria
            '3131': '2311',     # Acción Social
            '3132': '2310',     # Asistencia Social
            '3133': '2315',     # Departamento de la mujer
            '3135': '3379',     # Centro Tercera Edad
            '3136': '3379',     # Centro Tercera Edad
            '3139': '2316',     # Centro de día para menores
            '3210': '2318',     # Educador de Calle
            '3220': '2410',     # Escuelas Taller
            '3222': '2411',     # Promoción del empleo
            '3223': '4300',     # Promoción Económica
            '3230': '2314',     # Entidades no lucrativas
            '3224': '2412',     # Bolsa de empleo
            '3233': '2313',     # Prevención drogodependencias
            '4110': '3111',     # Salud Pública
            '4120': '3121',     # Servicio Médico
            '4131': '3111',     # Salud Pública
            '4132': '3112',     # Desinfeccion y desratización
            '4134': '3113',     # Ciudades sanas
            '4220': '3231',     # Enseñanza Primaria
            '4221': '3200',     # Ponencia de educación
            '4223': '3261',     # Escuela Permanente de Adultos
            '4226': '3265',     # OOAA Conservatorio Músic
            '4230': '3264',     # Gabinete psicopedagógico
            '4260': '2317',     # Comedor social
            '4310': '9203',     # Edificios Municipales
            '4312': '1521',     # Agencia de la vivienda
            '4314': '1522',     # Plan especial rehabilitación
            '4320': '1510',     # Urbanismo
            '4321': '1510',     # Urbanismo
            '4322': '1510',     # Urbanismo
            '4323': '1532',     # Vías públicas
            '4340': '1650',     # Alumbrado Público
            '4351': '1710',     # Parques y Jardines
            '4352': '1710',     # Parques y Jardines
            '4410': '1610',     # Servicio de Agua Potable
            '4411': '1600',     # Alcantarillado y tratamiento de aguas
            '4413': '1612',     # Fuente del Manano
            '4420': '1630',     # Limpieza viaria
            '4422': '1621',     # Recogida de residuos
            '4424': '1621',     # Recogida de residuos
            '4430': '1640',     # Cementerio Municipal
            '4440': '1532',     # Vías públicas
            '4441': '1531',     # Obras
            '4442': '1531',     # Obras
            '4460': '1700',     # Medio Ambiente
            '4461': '1700',     # Medio Ambiente
            '4470': '4930',     # O.M.I.C.
            '4480': '4312',     # Mercados, abastos y lonjas
            '4510': '3320',     # Bibliotecas y Archivos
            '4511': '3343',     # Campaña animación lectura
            '4512': '3344',     # Proyectos culturales Europeos
            '4513': '3265',     # OOAA Conservatorio Música
            '4514': '3330',     # Escuela de Teatro
            '4515': '3300',     # Animador Cultural
            '4516': '3340',     # Ponencia de Cultura
            '4517': '3341',     # Casa de la Cultura
            '4518': '3370',     # Ponencia de Juventud
            '4519': '3347',     # Promoción de uso Valenciano
            '4520': '3422',     # Piscinas municipales
            '4521': '3421',     # Polideportivo Municipal
            '4522': '3410',     # Ponencia de Deportes
            '4531': '3360',     # Arqueología y protección del patrimonio histórico-artístico
            '4540': '3380',     # Fiestas Populares
            '4610': '3345',     # Bandas de Música
            '4631': '4910',     # Medios de comunicación
            '4640': '3381',     # Junta Local Fallera
            '4641': '3382',     # Comisiones Falleras
            '4650': '2314',     # Entidades no lucrativas
            '4651': '3370',     # Ponencia de Juventud
            '4653': '2314',     # Entidades no lucrativas
            '5110': '1532',     # Vías públicas
            '5111': '1532',     # Vías públicas
            '5112': '1532',     # Vías públicas
            '5310': '4120',     # Plan Ecológico ganadería y agricultura
            '6110': '9310',     # Área Económica
            '6113': '9320',     # Recaudación Tributos
            '6220': '4311',     # Feria San Sebastián
            '6320': '9240',     # Participación ciudadana
            '7110': '4100',     # Consejo Local Agrario
            '7111': '4100',     # Consejo Local Agrario
            '9112': '9420',     # Transferencias a Entidades Locales territoriales
            '9114': '9430',     # Transferencias a otras Entidades Locales
            '9116': '9430',     # Transferencias a otras Entidades Locales
            '9210': '9291',     # Indemnizaciones
        }

        # For years before 2009 and 2015 we check whether we need to amend the programme code
        fc_code = line[1].strip().rjust(4, '0') # We need four digits, including leading zeroes
        year = self.year
        if int(year) < 2010:
            fc_code = programme_mapping_2010.get(fc_code, fc_code)
        elif int(year) < 2015:
            fc_code = programme_mapping.get(fc_code, fc_code)

        policy_id = fc_code[:2] # First two digits of the programme make the policy id
        # But what we want as area is the policy description
        policy = Budget.objects.get_all_descriptions(budget.entity)['functional'][policy_id]

        return {
            'area': policy,
            'programme': None,
            'fc_code': None,  # We don't try (yet) to have foreign keys to existing records
            'ec_code': None,
            'date': line[6].strip(),
            'contract_type': None,
            'payee': self._titlecase(line[9].strip()),
            'anonymized': False,
            'description': self._spanish_titlecase(line[10].strip()[:300].decode('utf-8','ignore').encode('utf-8')),
            'amount': self._read_english_number(line[7])
        }
