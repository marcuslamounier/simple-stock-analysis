import pandas as pd
from datetime import date
import os
from functions.analyzeStocks import summarizeInformation

from functions.menu_sectors import menu_sectors
from functions.get_stocks import *
from functions.menu_strategies import menu_strategies
from functions.read_csv import read_csv

method = menu_strategies()
if (method == 'Sector Analysis'):
  option = menu_sectors()
  if option[1] == '':
    print('No information about this sector in the API.')
  else:
    stock_list = get_stock_list(option[0])
else:
  stock_list = get_stock_list()

if len(stock_list) > 0:
  df = createDataframe(stock_list)

  media_subsetor = summarizeInformation(df, 'Subsetor')
  media_setor = summarizeInformation(df, 'Setor')

  print ('Generating file...')
  t = date.today().strftime("%Y-%m-%d")

  filename = 'outputs/'+method.replace(' ','_').lower()
  if (method == 'Sector Analysis'):
    filename += ('_'+str(option[1]).replace(',', '').replace(' ', '_'))
  filename += ('_'+t+'.xlsx')

  if os.path.exists(filename):
    os.remove(filename)

  with pd.ExcelWriter(filename) as writer:
    if (method != 'Sector Analysis'):
      sector_agg =summarizeInformation(df, 'Setor')
      sector_agg.to_excel(writer, sheet_name='SECTOR', encoding='utf8')

    subsector_agg =summarizeInformation(df, 'Subsetor')
    subsector_agg.to_excel(writer, sheet_name='SUBSECTOR', encoding='utf8')

    df.to_excel(writer, sheet_name='data', encoding='utf8')

  print ('Done.')

else:
  print('Your research have not returned any information.')






# option = menu_sectors()
# if option[1] == '':
#   print('Não há informação sobre este setor na API.')
# else:
#   stock_list = get_stock_list(option[0])
#   df_columns = get_stock_columns(stock_list[0])

#   df = pd.DataFrame(columns=df_columns)

#   for stock in stock_list:
#     df_data = get_stock_information(stock)
#     df = pd.concat([df, pd.DataFrame(columns = df_columns, data = [df_data])], ignore_index=True)
    
#   clean_float_columns(df, list(df.iloc[:, [5]].columns), decimalPlaces = 2)
#   clean_float_columns(df, list(df.iloc[:, 7:9].columns), decimalPlaces = 2)
#   clean_float_columns(df, list(df.iloc[:, 9:12].columns))
#   clean_float_columns(df, list(df.iloc[:, [13]].columns))
#   clean_float_columns(df, list(df.iloc[:, 14:31].columns), decimalPlaces = 2)
#   clean_float_columns(df, list(df.iloc[:, [31]].columns), decimalPlaces = 1)
#   clean_float_columns(df, list(df.iloc[:, 32:34].columns), decimalPlaces = 2)
#   clean_float_columns(df, list(df.iloc[:, [34]].columns), decimalPlaces = 1)
#   clean_float_columns(df, list(df.iloc[:, 35:37].columns), decimalPlaces = 2)
#   clean_float_columns(df, list(df.iloc[:, 37:43].columns), decimalPlaces = 1)
#   clean_float_columns(df, list(df.iloc[:, 43:46].columns), decimalPlaces = 2)
#   clean_float_columns(df, list(df.iloc[:, 46:].columns))

  # indicators = [
  #   'Subsetor',
  #   'Vol $ méd (2m)',
  #   'Dia (%)',
  #   'Mês (%)',
  #   '30 dias (%)',
  #   '12 meses (%)',
  #   '2022 (%)',
  #   '2021 (%)',
  #   '2020 (%)',
  #   '2019 (%)',
  #   '2018 (%)',
  #   '2017 (%)',
  #   'P/L',
  #   'P/VP',
  #   'P/EBIT',
  #   'PSR',
  #   'Div. Yield',
  #   'EV / EBITDA',
  #   'EV / EBIT',
  #   'Cres. Rec (5a)',
  #   'Marg. Bruta',
  #   'Marg. EBIT',
  #   'Marg. Líquida',
  #   'EBIT / Ativo',
  #   'ROIC',
  #   'ROE',
  #   'Liquidez Corr',
  #   'Div Br/ Patrim',
  #   'Giro Ativos'
  # ]
  # df_aux = df[indicators]


  # media_setor = df_aux[indicators].groupby('Subsetor').agg(['mean','std'])

  # print ('Gerando arquivo...')

  # t = date.today().strftime("%Y-%m-%d")
  # filename = 'outputs/stocks_alanysis_sector_'+str(option[1]).replace(',', '')+'_'+t+'.xlsx'

  # if os.path.exists(filename):
  #     os.remove(filename)

  # with pd.ExcelWriter(filename) as writer:
  #     media_setor.to_excel(writer, sheet_name='GENERAL', encoding='utf8')
  #     df.to_excel(writer, sheet_name=option[1], encoding='utf8')

  # print ('Finalizado.')