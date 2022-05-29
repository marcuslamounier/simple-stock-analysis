strategies = [
  'Sector Analysis',
  'Cash Yield (not working yet)',
  'Earning Yield (not working yet)',
  'IDIV (not working yet)'
]

def menu_strategies():
  option = -1
  while option < 1 or option > len(strategies):
    for i in range (0, len(strategies)):
      print(i + 1, '-', strategies[i])
    option = int(input("\nDigite o método que gostaria de utilizar: "))
    if (option < 1 or option > len(strategies)):
      print('Digite uma opção válida. Há apenas', len(strategies),'métodos disponíveis.')
    else:
      return strategies[option - 1]