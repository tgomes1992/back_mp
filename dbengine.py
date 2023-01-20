from sqlalchemy import create_engine
import pymongo
from MAPS_MODULE.extracoes import MapsEscriturador
from datetime import datetime , timedelta
from BackupModule.ExtracaoMovimentacao import ExtracaoMovimentacao




myclient = pymongo.MongoClient("mongodb://localhost:27017/")



data = datetime(2020,1,1)

escriturador = ExtracaoMovimentacao(data, myclient)

escriturador.extrair_eventos_por_depositaria()






# start_date = datetime(2020,1,1)

# enddate = datetime.today()


# while start_date < enddate:
#     start_date = start_date+ timedelta(days=1)
#     data = start_date.strftime("%Y-%m-%d")
#     incluir_movimentos(5010150 , data)
#     print (data)


