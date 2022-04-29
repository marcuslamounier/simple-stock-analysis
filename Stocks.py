import pandas as pd
from datetime import date
import os

from functions.menu_stocks import menu_stocks
from functions.get_stocks import *
from functions.read_csv import read_csv

option = menu_stocks()
if option[1] == '':
  print('Não há informação sobre este setor na API.')
else:
  stock_list = get_stock_list(option[0])
  df_columns = get_stock_columns(stock_list[0])

  df = pd.DataFrame(columns=df_columns)

  for stock in stock_list:
    df_data = get_stock_information(stock)
    df = pd.concat([df, pd.DataFrame(columns=df_columns, data=[df_data])])

  clean_float_columns(df, list(df.iloc[:, [5]].columns), decimal = True)
  clean_float_columns(df, list(df.iloc[:, 7:9].columns), decimal = True)
  clean_float_columns(df, list(df.iloc[:, 9:12].columns))
  clean_float_columns(df, list(df.iloc[:, [13]].columns))
  clean_float_columns(df, list(df.iloc[:, 14:46].columns), decimal = True)
  clean_float_columns(df, list(df.iloc[:, 46:].columns))

  indicators = [
    'Subsetor',
    'Vol $ méd (2m)',
    'Dia (%)',
    'Mês (%)',
    '30 dias (%)',
    '12 meses (%)',
    '2022 (%)',
    '2021 (%)',
    '2020 (%)',
    '2019 (%)',
    '2018 (%)',
    '2017 (%)',
    'P/L',
    'P/VP',
    'P/EBIT',
    'PSR',
    'Div. Yield',
    'EV / EBITDA',
    'EV / EBIT',
    'Cres. Rec (5a)',
    'Marg. Bruta',
    'Marg. EBIT',
    'Marg. Líquida',
    'EBIT / Ativo',
    'ROIC',
    'ROE',
    'Liquidez Corr',
    'Div Br/ Patrim',
    'Giro Ativos'
  ]
  df_aux = df[indicators]
  media_setor = df_aux[indicators].groupby('Subsetor').agg(['mean','std'])

  print ('Gerando arquivo...')

  t = date.today().strftime("%Y-%m-%d")
  filename = 'outputs/stocks_alanysis_sector_'+str(option[1]).replace(',', '')+'_'+t+'.xlsx'

  if os.path.exists(filename):
      os.remove(filename)

  with pd.ExcelWriter(filename) as writer:
      media_setor.to_excel(writer, sheet_name='GENERAL', encoding='utf8')
      df.to_excel(writer, sheet_name=option[1], encoding='utf8')

  print ('Finalizado.')