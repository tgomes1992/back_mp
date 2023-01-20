import email
from MAPS_MODULE.extracoes import Maps, MapsCentaurus , MapsEscriturador
from sqlalchemy import create_engine
from datetime import date, datetime , timedelta
import pandas as pd
from dbengine import engine_fundo



engine_teste = create_engine("mysql+pymysql://root:tAman1993**@localhost/batimentos_o2_maps")

engine_besa = create_engine("sqlite:///besa.db")


# ativos_maps = pd.read_sql("ativos_maps", con=engine_teste)


# ativos_maps.to_csv("teste.csv")

# print (ativos_maps)



class Login():

    def __init__(self,path):
        self.path =  path
        
    def get_login(self):
        df = pd.read_excel(self.path)
        return {
            'login': df.user[0] , 
            'password':  df.password[0]
        }



class ExtratorMaps():

    
    path = "//Scototrj01/h/CUSTODIA/7 Escrituração de Ativos/1 - Controle das Operações/Batimentos/data_files"

    login  = Login(f'{path}/login.xlsx').get_login()
    cent = MapsCentaurus(login['login'],login['password'])
    pd.options.display.float_format = '{:.2f}'.format


    def __init__(self,data):
        self.data = data        

    def extrair_cotas_posicao(self,papel_cota):
        data_inicial = date(2021,12,31)
        df = self.cent.posicao_movimentacoes(self.data,papel_cota)
        print (df)
        df.to_sql("posicao",con=engine_fundo,index=False,if_exists='append')


    def movimento_fundo(self,papel_cota):
        df = self.cent.extrair_movimentacoes_fundo(papel_cota,"01/01/2000",self.data)
        df.to_sql("movimento",con=engine_fundo,if_exists="append")

    def extrair_posicao_consolidada(self,papelcota):
        df = self.cent.get_posicao_consolidada(papelcota,self.data)
        df.to_sql("posicaoconsolidada",con=engine_fundo,if_exists="append")

    def renovar_dados_papel_cota(self):
        try:
            engine_fundo.execute(f'drop table if exists posicaoconsolidada ')
            engine_fundo.execute(f"drop table if exists  posicao ")
            engine_fundo.execute(f'drop table if exists movimento')
        except Exception as e:
            print(e)
            pass

    def main(self,papelcota):
        print (f"Extração Papel cota {papelcota} iniciada")
        self.renovar_dados_papel_cota()
        print ("delete realizado")
        self.extrair_cotas_posicao(papelcota)
        # self.movimento_fundo(papelcota)
        # self.extrair_posicao_consolidada(papelcota)
        print (f"Extração Papel cota {papelcota} finalizada")

    def quantidade_movimentacoes(self,papel_cota):
        df = self.cent.extrair_movimentacoes_fundo(papel_cota,"01/01/2000","31/12/2022")
        resultado = {
            "papel_cota":  [papel_cota] , 
            "quantidade_movimentacoes" :  [df.count()['Tipo Operação']]
        }
        return resultado



escriturador = MapsEscriturador("pamela.leal",'Fevereiro2023')


datainicial = datetime(2017,1,1)
datafim =  datetime(2022,10,26)
while datainicial != datafim:
    print (datainicial)
    df = escriturador.movimentos(5012351,datainicial.strftime("%Y-%m-%d"))
    if not df.empty:
        df.to_sql("movimentacoes",con=engine_besa, if_exists="append",index=False)
    datainicial = datainicial + timedelta(days=1)





