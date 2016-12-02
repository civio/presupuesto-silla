# -*- coding: UTF-8 -*-
from budget_app.models import *
from budget_app.loaders import SimpleBudgetLoader
from decimal import *
import csv
import os
import re

class SillaBudgetLoader(SimpleBudgetLoader):

    def parse_item(self, filename, line):
        # Programme codes have changed in 2015, due to new laws. Since the application expects a code-programme
        # mapping to be constant over time, we are forced to amend budget data prior to 2015.
        # See https://github.com/dcabo/presupuestos-aragon/wiki/La-clasificaci%C3%B3n-funcional-en-las-Entidades-Locales
        programme_mapping = {
            # old programme: new programme
            '1550': '1532',     # Vías públicas
            '1551': '1531',     # Obras
            '1620': '1630',     # Limpieza viaria
            '1720': '1721',     # Protección y mejora medio ambiente
            '2300': '2310',     # Asistencia social
            '2320': '2315',     # Departamento de la mujer
            '2321': '2316',     # Centro de día para menores
            '2322': '2318',     # Educador de Calle
            '2323': '2313',     # Prevención drogodependencias
            '2324': '2314',     # Entidades no lucrativas
            '2330': '2312',     # Asistencia domiciliaria
            '2331': '2319',     # Ayuda a la dependencia
            '3131': '3111',     # Salud Pública
            '3132': '3112',     # Desinfeccion y desratización
            '3133': '3113',     # iudades sanas
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
            '3130': '3110',     # Medicamentos y prod sanitarios
        }

        # Some dirty lines in input data
        if line[0]=='':
            return None

        is_expense = (filename.find('gastos.csv')!=-1)
        is_actual = (filename.find('/ejecucion_')!=-1)
        if is_expense:
            # We got 3- or 4- digit functional codes as input, so add a trailing zero
            fc_code = line[1].ljust(4, '0')
            # We got 3- or 5- digit economic codes as input, so add a trailing zero
            ec_code = line[2].ljust(5, '0')

            # For years before 2015 we check whether we need to amend the programme code
            year = re.search('municipio/(\d+)/', filename).group(1)
            if int(year) < 2015:
                fc_code = programme_mapping.get(fc_code, fc_code)

            return {
                'is_expense': True,
                'is_actual': is_actual,
                'fc_code': fc_code,
                'ec_code': ec_code[:-2],        # First three digits (everything but last two)
                'ic_code': '000',
                'item_number': ec_code[-2:],    # Last two digits
                'description': line[4],
                'amount': self._parse_amount(line[10 if is_actual else 7])
            }

        else:
            return {
                'is_expense': False,
                'is_actual': is_actual,
                'ec_code': line[1][:-2],        # First three digits
                'ic_code': '000',               # All income goes to the root node
                'item_number': line[1][-2:],    # Fourth and fifth digit; careful, there's trailing dirt
                'description': line[3],
                'amount': self._parse_amount(line[7 if is_actual else 4])
            }
