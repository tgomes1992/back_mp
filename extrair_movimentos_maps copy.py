from BackupModule.ExtracaoMovimentacao import ExtracaoMovimentacao
from pymongo import MongoClient
from datetime import datetime ,  timedelta
import pandas as pd
from MAPS_MODULE.extracoes import MapsCentaurus


myclient = MongoClient("mongodb://Thiago.Conceicao:PZV%7BTaKR1j8n@OTAPLICRJ04/")



def atualizar_investidor():

    atualizacao_investidor = MapsCentaurus("thiago.conceicao","tAman2021**")
    df = atualizacao_investidor.get_investidor()
    base = df.to_dict("records")
    mydb = myclient["backup_maps"]
    mydb['investidores'].delete_many({})
    mydb['investidores'].insert_many(base)  



def get_investidores(nome):
    mydb = myclient["backup_maps"]
    investidor = mydb['investidores'].find_one({"Investidor": nome})
    try:
        return investidor['cpf_cnpj_jcot']
    except:
        return nome



'''extrai todas as movimentações escriturais'''
# movimentos.movimentos_escriturador()

def gerar_planilha_importacao(papelcota , cd_fundo ,  data , path):

    col = myclient['movimentos_abertos2']['JIVE_BOSSANOVA_HIGH_YIELD_ADVISORY_FIC_FIM_CP'].find({"data": data})
    df = pd.DataFrame.from_dict(col)
    df['cotista'] = df['investidor'].apply(get_investidores)
    df['fundo'] = cd_fundo
    df['valor'] = df['Valor Bruto'].apply(abs)
    df['liquidacao'] = "LI"
    df['qtdcotas'] = df['Quantidade'].apply(abs)
    df['tipo'] = df["Tipo Operação"]
    df['data'] = df['data'].apply(lambda x: datetime.strptime(x , "%d/%m/%Y").strftime("%Y-%m-%d"))    
    # filtro = df['Tipo Operação'] != "COME-COTAS"
    df[[ 'data' ,  'tipo'  ,  'cotista' , "fundo"  , 'liquidacao'  , 'valor' , 'qtdcotas' ]].to_excel(f'{path}/{data.replace("/","")}.xlsx' , index=False)


with open('fundos_backup.txt','r') as arquivo:
    for item in arquivo:
        fundo =  item.replace("\n","")        
        print (fundo)
        data_inicial = datetime(2022,5,30)
        movimentos = ExtracaoMovimentacao(data_inicial, myclient)
        movimentos.movimentos_fundos_abertos(fundo)
      






data_inicial = datetime(2022,5,30)
data_final = datetime.today()
atualizar_investidor()

while data_inicial < data_final:
    try:
        print (data_inicial)
        gerar_planilha_importacao("JIVE BOSSANOVA HIGH YIELD ADVISORY FIC FIM CP" ,  '30991' , data_inicial.strftime("%d/%m/%Y") , "JIVE")
        data_inicial = data_inicial + timedelta(days=1)
    except Exception as e :
        data_inicial = data_inicial + timedelta(days=1)
        continue


