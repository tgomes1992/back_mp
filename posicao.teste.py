from MAPS_MODULE.extracoes import MapsCentaurus
import pandas as pd

centaurus = MapsCentaurus("thiago.conceicao","tAman1994**")


retorno  = centaurus.posicao_movimentacoes("10/02/2022" ,"JIVE BOSSANOVA HIGH YIELD ADVISORY FIC FIM CP")

base = pd.DataFrame.from_dict(retorno)


base.to_excel("posicao.xlsx")