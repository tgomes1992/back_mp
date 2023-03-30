import requests
import json 
from JCOTSERVICE import RelPosicaoFundoCotistaService ,  ListFundosService
import pandas as pd
from MAPS_MODULE.extracoes import MapsCentaurus
from datetime import datetime




posicaojcot = RelPosicaoFundoCotistaService("thiago","Senh@123")
dias_fundos = ListFundosService("thiago","Senh@123").listfundosrequest()
centaurus =  MapsCentaurus("thiago.conceicao" , "tAman2021**")

def buscar_data_posicao(codigo_fundo):
    try:
        return dias_fundos[dias_fundos['codigo']==codigo_fundo].dataPosicao.values[0]
    except:
        return "erro"

depara = "http://otaplicrj04:5004/get_ativos_cadastrados"
base = requests.get(depara)
df_de_para = pd.DataFrame.from_dict(base.json())
df_de_para["dataPosicao"] = df_de_para['jcot'].apply(buscar_data_posicao)
df_de_para.columns = ['centaurus', 'id_amplis', 'codigo' ,  'o2', 'pegasus' , 'dataposicao']
pre_df_com_jcot = []

for item in df_de_para.iterrows():
    try:
        base  = item[1].to_dict()
        posicao = posicaojcot.get_posicao_consolidada(base)
        posicao_maps =  centaurus.get_posicao_consolidada(base["centaurus"] , datetime.strptime( base['dataposicao'] , "%Y-%m-%d").strftime("%d/%m/%Y"))
        base['qtd_jcot'] = posicao['qtCotas']
        base['qtd_maps'] =  posicao_maps['Quantidade']
        base['principalJcot'] =  posicao['vlAplicacao']
        base['principalMaps'] = posicao_maps['Principal']
        base['plJcot'] = posicao['vlCorrigido']
        base['plMaps'] = posicao_maps['Saldo Bruto']
        print (base)
        pre_df_com_jcot.append(base)    
    except Exception as e:
        print (e)
        continue

batimento = pd.DataFrame.from_dict(pre_df_com_jcot)








