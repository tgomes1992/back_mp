from .CotService import COTSERVICE
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import pandas as pd


class ListFundosService(COTSERVICE):


    url = "https://oliveiratrust.totvs.amplis.com.br:443/jcotserver/services/FundosService"


    def listFundosRequestBody(self):
        xml_request = f'''<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:tot="http://totvs.cot.webservices">
   <soapenv:Header>
        {self.header_login()}
   </soapenv:Header>
   <soapenv:Body>
      <tot:ListFundosRequest>
         <tot:fundo>
            <tot:login>{self.user}</tot:login>
         </tot:fundo>
      </tot:ListFundosRequest>
   </soapenv:Body>
</soapenv:Envelope>'''
        return xml_request


    def formatar_resposta(self,xmlresponse):
         # buscar_status  = RelPosicaoFundoCotistaService(self.user , self.password)
         base_formatacao = {
            'ns2:razaoSocial':  [] , 
            'ns2:cnpj': [] ,   
            'ns2:codigo':  [] , 
            'ns2:custodiante':  []  ,
            'ns2:gestorPrincipal': [] , 
            'ns2:administrador': []  , 
            'ns2:empresa':  [] , 
            'ns2:tipoFundo': [] , 
            'ns2:dataPosicao': []  ,
            # "status": []
         }
         response = BeautifulSoup(xmlresponse,'xml')
         fundos = response.find_all("ns2:fundo")
         for i in fundos:
            formata_data = datetime.strptime(i.find('ns2:dataPosicao').text[0:10],'%Y-%m-%d')
            base_formatacao['ns2:razaoSocial'].append(i.find('ns2:razaoSocial').text)
            base_formatacao['ns2:cnpj'].append(i.find('ns2:cnpj').text)
            base_formatacao['ns2:codigo'].append(i.find('ns2:codigo').text) 
            base_formatacao['ns2:custodiante'].append(i.find('ns2:custodiante').text)
            base_formatacao['ns2:gestorPrincipal'].append(i.find('ns2:gestorPrincipal').text)
            base_formatacao['ns2:administrador'].append(i.find('ns2:administrador').text)
            base_formatacao['ns2:empresa'].append(i.find('ns2:empresa').text)
            base_formatacao['ns2:tipoFundo'].append(i.find('ns2:tipoFundo').text )
            base_formatacao['ns2:dataPosicao'].append(i.find('ns2:dataPosicao').text[0:10])
            # base_formatacao['status'].append(buscar_status.get_status({'codigo': i.find('ns2:codigo').text  , 'dataposicao': i.find('ns2:dataPosicao').text[0:10]  }))
            # base_formatacao['status'].append('fechado')
         df = pd.DataFrame.from_dict(base_formatacao)
         df.columns = ["razaoSocial",'cnpj','codigo','custodiante','gestorPrincipal',"administrador",'empresa',"tipoFundo","dataPosicao" ]
         return df 


    def listfundosrequest(self):
      r = requests.post(self.url,self.listFundosRequestBody())
      df = self.formatar_resposta(r.content)
      return df
 
