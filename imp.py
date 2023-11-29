import os




path =  "H:/CUSTODIA/7 Escrituração de Ativos/8 - Administradores/Maps/Escriturador/Informes/ComprovantesPF/36113876000191-ADM/2022/ourinvest/renomeados"
files = os.listdir(path)

for item in files:
    os.rename(  os.path.join(path , item) , os.path.join(path , item.replace("IRRF 2023" , "IRRF 2022" ) ))