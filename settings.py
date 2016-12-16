# -*- coding: UTF-8 -*-

from django.conf.urls import patterns, url

MAIN_ENTITY_LEVEL = 'municipio'
MAIN_ENTITY_NAME = 'Silla'

BUDGET_LOADER = 'SillaBudgetLoader'
PAYMENTS_LOADER = 'SillaPaymentsLoader'

FEATURED_PROGRAMMES = ['1320', '1532', '1621', '1700', '2310', '3340', '3421']

OVERVIEW_INCOME_NODES = [
                          {
                            'nodes': [['11', '113']],
                            'label.ca': 'Impost sobre béns immobles de naturalesa urbana',
                            'label.es': 'Impuesto sobre bienes inmuebles de naturaleza urbana',
                            'link_id': '11'
                          },
                          {
                            'nodes': [['11', '115']],
                            'label.ca': 'Impost sobre vehicles de tracció mecànica',
                            'label.es': 'Impuesto sobre vehículos de tracción mecánica',
                            'link_id': '11'
                          },
                          '13', '42',
                        ]

OVERVIEW_EXPENSE_NODES = ['01', '13', '15', '16', '23', '32', '33', '34', '92']

# How aggresive should the Sankey diagram reorder the nodes. Default: 0.79 (Optional)
# Note: 0.5 usually leaves nodes ordered as defined. 0.95 sorts by size (decreasing).
# OVERVIEW_RELAX_FACTOR = 0.95

# Show Payments section in menu & home options. Default: False.
SHOW_PAYMENTS           = True

# Show Tax Receipt section in menu & home options. Default: False.
SHOW_TAX_RECEIPT        = True

# Show Counties & Towns links in Policies section in menu & home options. Default: False.
# SHOW_COUNTIES_AND_TOWNS = True

# Show an extra tab with institutional breakdown. Default: True.
SHOW_INSTITUTIONAL_TAB  = False

# Show an extra tab with funding breakdown (only applicable to some budgets). Default: False.
# SHOW_FUNDING_TAB = True

# Adjust inflation in amounts in Overview page. Default: True
ADJUST_INFLATION_IN_OVERVIEW = False

# Show Subtotals panel in Overview. Default: False
# SHOW_OVERVIEW_SUBTOTALS = True

# Calculate budget indicators (True), or show/hide the ones hardcoded in HTML (False). Default: True.
# CALCULATE_BUDGET_INDICATORS = False

# Show an extra column with actual revenues/expenses. Default: True.
# Warning: the execution data still gets shown in the summary chart and in downloads.
# SHOW_ACTUAL = False

# Include financial income/expenditures in overview and global policy breakdowns. Default: False.
# INCLUDE_FINANCIAL_CHAPTERS_IN_BREAKDOWNS = True

# Search in entity names. Default: True.
SEARCH_ENTITIES = False

# Supported languages. Default: ('es', 'Castellano')
LANGUAGES = (
  ('ca', 'Valenci&agrave;'),
  ('es', 'Castellano'),
)

# Facebook Aplication ID used in social_sharing temaplate. Default: ''
# In order to get the ID create an app in https://developers.facebook.com/
FACEBOOK_ID             = '1070950059697559'

# Google Analytics ID. Default: ''
# In order to get the ID create a Google Analytics Acount in https://analytics.google.com/analytics/web/
ANALYTICS_ID            = 'UA-28946840-24'

# Setup Data Source Budget link
DATA_SOURCE_BUDGET      = 'http://www.silla.es/serveis-municipals/serveis-economics/pressupost-municipal'

# Setup Data Source Population link
DATA_SOURCE_POPULATION  = 'http://www.ine.es/dynt3/inebase/index.htm?padre=517'

# Setup Data Source Inflation link
DATA_SOURCE_INFLATION   = 'http://www.ine.es/jaxiT3/Tabla.htm?t=10019&L=0'

# Setup Main Entity Web Url
MAIN_ENTITY_WEB_URL     = 'http://www.silla.es/'

# Setup Main Entity Legal Url (if empty we hide the link)
MAIN_ENTITY_LEGAL_URL   = 'http://www.silla.es/avis-legal'

# External URL for Cookies Policy (if empty we use out template page/cookies.html)
COOKIES_URL             = ''

# Allow overriding of default treemap color scheme
# COLOR_SCALE = [ '#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2', '#e7969c', '#bcbd22', '#17becf' ]
