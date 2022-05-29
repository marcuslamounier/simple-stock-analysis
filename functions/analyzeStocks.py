from pandas import DataFrame


indicators = [
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

def summarizeInformation (df: DataFrame, groupBy = 'Setor'):
  indicators.append(groupBy)
  df_aux = df[indicators].groupby(groupBy).agg(['mean', 'std'])
  indicators.pop()
  return df_aux