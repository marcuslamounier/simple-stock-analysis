import pandas as pd
import requests

headers = {
    'User-Agent':
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    ' (KHTML, like Gecko) Chrome/100.0.4896.88 Safari/537.36'
}
base_url = 'https://fundamentus.com.br'

def get_stock_list(sector_id = ''):
  url = base_url+'/resultado.php?setor='+str(sector_id)
  response = requests.get(url, headers=headers)
  content = pd.read_html(response.content)
  return content[0]['Papel']


def get_stock_columns(stock_id): 
  url = base_url+'/detalhes.php?papel='+str(stock_id)
  response = requests.get(url, headers=headers)
  content = pd.read_html(response.content)
  columns = []

  # AQUI ESTÁ PRONTO ATÉ A PARTE 1
  for table_index in range(0, 2):
    part = content[table_index]
    for column_index in range(0, len(part.columns), 2):
      column_names = list(part[column_index])
      column_names = [str(c).replace('?', '') for c in column_names]
      columns.extend(column_names)

        
  # AQUI ESTÁ PRONTO ATÉ A PARTE 3
  for table_index in range(2, 4):
    part = content[table_index]
    for column_index in range(0, len(part.columns), 2):
      column_names = part[column_index].dropna()
      if column_names[0] == 'Oscilações':
        postfix = ' (%)'
      else:
        postfix = ''
      column_names = list(column_names.drop([0]))
      column_names = [str(c).replace('?', '')+postfix for c in column_names]
      columns.extend(column_names)

  # AQUI ESTÁ PRONTO ATÉ A PARTE 4
  for table_index in range(4, 5):
    part = content[table_index]
    for column_index in range(0, len(part.columns), 2):
      column_names = part[column_index].dropna()
      if column_names[1] == 'Últimos 12 meses':
        postfix = ' (12m)'
      else:
        postfix = ' (3m)'
      column_names = list(column_names.drop([0, 1]))
      column_names = [str(c).replace('?', '')+postfix for c in column_names]
      columns.extend(column_names)
      
  return columns

def get_stock_information(stock_id):
  url = base_url+'/detalhes.php?papel='+str(stock_id)
  response = requests.get(url, headers=headers)
  content = pd.read_html(response.content)
  data = []

  # AQUI ESTÁ PRONTO ATÉ A PARTE 1
  for table_index in range(0, 2):
    part = content[table_index]
    for column_index in range(1, len(part.columns), 2):
      data.extend(list(part[column_index]))

  for table_index in range(2, 4):
    part = content[table_index]
    for column_index in range(1, len(part.columns), 2):
      data.extend(list(part[column_index].dropna().drop([0])))

  for table_index in range(4, 5):
    part = content[table_index]
    for column_index in range(1, len(part.columns), 2):
      data.extend(list(part[column_index].drop([0, 1])))
      
  return data

def clean_float_columns(df, list_columns, decimalPlaces = 0):
  for col in list_columns:
    df.loc[df[col] == '-', [col]] = [0]
  df[list_columns] = df[list_columns].fillna(0)
  df[list_columns] = df[list_columns].applymap(lambda x: str(x).replace('%', ''))
  if decimalPlaces == 1:
    df[list_columns] = df[list_columns].applymap(lambda x: str(x) + '0')
  df[list_columns] = df[list_columns].applymap(lambda x: str(x).replace('.', '').replace(',', ''))
  df[list_columns] = df[list_columns].astype('float')
  if decimalPlaces > 0:
    df[list_columns] = df[list_columns]/(pow(10, max(2, decimalPlaces)))

def clean_float_fundamentus_dataframe(df):
  clean_float_columns(df, list(df.iloc[:, [5]].columns), decimalPlaces = 2)
  clean_float_columns(df, list(df.iloc[:, 7:9].columns), decimalPlaces = 2)
  clean_float_columns(df, list(df.iloc[:, 9:12].columns))
  clean_float_columns(df, list(df.iloc[:, [13]].columns))
  clean_float_columns(df, list(df.iloc[:, 14:31].columns), decimalPlaces = 2)
  clean_float_columns(df, list(df.iloc[:, [31]].columns), decimalPlaces = 1)
  clean_float_columns(df, list(df.iloc[:, 32:34].columns), decimalPlaces = 2)
  clean_float_columns(df, list(df.iloc[:, [34]].columns), decimalPlaces = 1)
  clean_float_columns(df, list(df.iloc[:, 35:37].columns), decimalPlaces = 2)
  clean_float_columns(df, list(df.iloc[:, 37:43].columns), decimalPlaces = 1)
  clean_float_columns(df, list(df.iloc[:, 43:46].columns), decimalPlaces = 2)
  clean_float_columns(df, list(df.iloc[:, 46:].columns))


def createDataframe (stock_list):
  df_columns = get_stock_columns(stock_list[0])
  df = pd.DataFrame(columns=df_columns)

  for stock in stock_list:
    print(stock)
    try:
      df_data = get_stock_information(stock)
      df = pd.concat([df, pd.DataFrame(columns=df_columns, data=[df_data])], ignore_index=True)
    except:
      print('Could not get information about', stock)
    # df_data = get_stock_information(stock)
    # df_aux = 
    # print (len(df_aux.columns), '-', len(df_columns), len(df_aux.columns) == len(df_columns))
    # if (len(df_aux.columns) == len(df_columns)):
    #   df = pd.concat([df, pd.DataFrame(columns=df_columns, data=[df_data])], ignore_index=True)

  clean_float_fundamentus_dataframe(df)

  return df