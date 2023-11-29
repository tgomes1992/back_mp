from BackupModule import *
from datetime import datetime ,  timedelta
import pymongo




class ExtracaoMovimentacao():
    escriturador = MapsEscriturador("marcella.rodrigues@oliveiratrust.com.br","#Mdetrano16")
    centaurus = MapsCentaurus("thiago.conceicao",'tAman2025**')

    def __init__(self, data , mongo_conection   ):
        '''a data , precisa ser a data inicial no formato datetime'''
        self.data = data
        self.mongo_conection  = mongo_conection
        self.db = "movimentos_abertos2" 
        self.today = datetime.today()
        # self.today = datetime(2022,8,22)


    def movimentos_escriturador(self):
        '''extrai os movimentos do escriturador da maps'''
        while self.data < self.today:
            movimentos = self.escriturador.movimentos_escriturais(self.data)
            print (self.data)
            self.mongo_conection[self.db]["movimentos_escriturador"].insert_many(movimentos)
            self.data = self.data + timedelta(days=1)

    def movimentos_centaurus(self , papel_cota):       
        while self.data < self.today:            
            print (f"Extração {papel_cota} {self.data.strftime('%Y-%m-%d')}  ")
            movimentos_centaurus = self.centaurus.extrair_movimentacoes_fundo(papel_cota ,  self.data.strftime("%d/%m/%Y"))
            print (movimentos_centaurus)
            self.mongo_conection[self.db]["movimentos_centaurus"].delete_many({"mnemonico":  papel_cota ,  "data": self.data.strftime("%d/%m/%Y") })
            self.mongo_conection[self.db]["movimentos_centaurus"].insert_many(movimentos_centaurus)
            self.data = self.data + timedelta(days=1)


    def movimentos_fundos_abertos(self , papel_cota):       
        while self.data <= self.today:
            try:      
                print (f"Extração {papel_cota} {self.data.strftime('%Y-%m-%d')}  ")
                movimentos_centaurus = self.centaurus.extrair_movimentacoes_fundo(papel_cota ,  self.data.strftime("%d/%m/%Y"))
                self.mongo_conection[self.db][papel_cota.replace(" ","_")].delete_many({"mnemonico":  papel_cota ,  "data": self.data.strftime("%d/%m/%Y") })
                self.mongo_conection[self.db][papel_cota.replace(" ","_")].insert_many(movimentos_centaurus)
                self.data = self.data + timedelta(days=1)
            except Exception as e:
                self.data = self.data + timedelta(days=1)
                print (e)
                continue



    def extracao_eventos_escriturador(self , depositaria):
        while self.data < self.today:
            eventos_escriturador = self.escriturador.consulta_eventos(self.data , depositaria)
            self.mongo_conection[self.db]['eventos_maps'].insert_many(eventos_escriturador)
            print (self.data)
            self.data = self.data + timedelta(days=1)


    def extrair_eventos_por_depositaria(self):
        depositarias = [1,2,3]
        data_base = self.data
        for depositaria in depositarias:
            self.extracao_eventos_escriturador(depositaria)
            self.data = data_base


