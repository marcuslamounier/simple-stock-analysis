from functions.read_csv import read_csv

sectors = read_csv('inputs/sectors.csv')

def menu_stocks():
  option = -1
  while option < 1 or option > len(sectors) - 1:
    option = int(input("\nDigite o código do setor (0 para ver lista): "))

    if (option == 0):
      for i in range (1, len(sectors)):
        if (sectors[i][1] != ''):
          print(sectors[i][0], '-', sectors[i][1])
    elif (option < 1 or option > len(sectors) - 1):
      print('Digite uma opção válida. Há apenas', len(sectors) - 1,'registrados.')
    else:
      return [option, sectors[option][1]]