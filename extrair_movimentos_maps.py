from BackupModule.ExtracaoMovimentacao import ExtracaoMovimentacao
from pymongo import MongoClient
from datetime import datetime ,  timedelta




myclient = MongoClient("mongodb://Thiago.Conceicao:PZV%7BTaKR1j8n@OTAPLICRJ04/")
# mydb = myclient["backup_maps"]


data_inicial = datetime(2021,1,1)
movimentos = ExtracaoMovimentacao(data_inicial, myclient)
'''extrai todas as movimentações escriturais'''
movimentos.movimentos_escriturador()
