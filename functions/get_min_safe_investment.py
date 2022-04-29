selic = 0.1175
best_liquid_rate = 1.05
income_tax_rate = 0.225

def get_min_safe_investment():
  print('Taxa básica (SELIC):', selic * 100, '%')
  print('CDI puro:', selic * 100 - 0.1, '%')
  print('Alíquota de IR:', income_tax_rate * 100, '%')

  benchmark_year = (best_liquid_rate * (selic - 0.001)) * (1 - income_tax_rate)

  print('Melhor oferta com baixa liquidez:', best_liquid_rate * 100, '%', 'do CDI =', round(benchmark_year * 100, 5), '%', 'a.a.')

  return round(((1 + benchmark_year) ** (1/12)) - 1, 7)