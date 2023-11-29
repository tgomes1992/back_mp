from BackupModule.ExtracaoMovimentacao import ExtracaoMovimentacao
from pymongo import MongoClient
from datetime import datetime ,  timedelta
import pandas as pd
from MAPS_MODULE.extracoes import MapsCentaurus


myclient = MongoClient("mongodb://Thiago.Conceicao:PZV%7BTaKR1j8n@OTAPLICRJ04/")



def atualizar_investidor():

    atualizacao_investidor = MapsCentaurus("thiago.conceicao","tAman2025**")
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

    col = myclient['movimentos_abertos2'][papelcota.replace(" ","_")].find({"data": data})
    df = pd.DataFrame.from_dict(col)
    # print(df)
    df['cotista'] = df['investidor'].apply(get_investidores)
    df['fundo'] = cd_fundo
    df['valor'] = df['Valor Bruto'].apply(abs)
    df['liquidacao'] = "LI"
    df['qtdcotas'] = df['Quantidade'].apply(abs)
    df['tipo'] = df["Tipo Operação"]
    df['data'] = df['data'].apply(lambda x: datetime.strptime(x , "%d/%m/%Y").strftime("%Y-%m-%d"))    

    # filtro = df['Tipo Operação'] != "COME-COTAS"
    df[[ 'data' ,  'tipo'  ,  'cotista' , "fundo"  , 'liquidacao'  , 'valor' , 'qtdcotas' ]].to_excel(f'{path}/{data.replace("/","")}.xlsx' , index=False)



    return df[[ 'data' ,  'tipo'  ,  'cotista' , "fundo"  , 'liquidacao'  , 'valor' , 'qtdcotas' ]].to_dict("records")


with open('fundos_backup.txt','r') as arquivo:
    for item in arquivo:
        fundo =  item.replace("\n","")        
        print (fundo)
        data_inicial = datetime(2023,3,1)
        movimentos = ExtracaoMovimentacao(data_inicial, myclient)
        movimentos.movimentos_fundos_abertos(fundo)
      



data_inicial = datetime(2023,3,1)

data_final = datetime(2023,7,12)

atualizar_investidor()

item = []
while data_inicial <= data_final:
    try:
        # print (data_inicial)
        dados = gerar_planilha_importacao("OT SOBERANO" ,  '1944' , data_inicial.strftime("%d/%m/%Y") , "OT SOBERANO")
        for d in dados:

            item.append(d)
        data_inicial = data_inicial + timedelta(days=1)

    except Exception as e :
        data_inicial = data_inicial + timedelta(days=1)
        print (e)
        continue


df = pd.DataFrame.from_dict(item)

df.to_excel("importar_jcot.xlsx")