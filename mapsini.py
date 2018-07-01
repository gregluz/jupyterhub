import googlemaps
import csv
import pandas as pd
import numpy as np
#ideia para usar com mais chaves
#gmaps2 = []
#a=str(input("Entre com uma chave ou 0 para sair"))
#while(a!="0"):
#    gmaps2.append(googlemaps.Client(key = a))
#    a = str(input("Entre com uma chave ou 0 para sair"))
gmaps = googlemaps.Client(key="AIzaSyD7grRXJmd_kf4V70PFYjrGlY2QtRjkcno")
gmaps4 = googlemaps.Client(key="AIzaSyDoBNsz1KDdzPOVZhtjEqN4hafhqv-cWo0")
gmaps2 = googlemaps.Client(key= "AIzaSyDLIhAqVhWWOMUEnI5_JjDhWtYsZkw1-vs")
gmaps3 = googlemaps.Client(key= "AIzaSyA3C9z1IX3Mxh88zzq9f730O2vJsJP-V60")
#if gmaps == gmaps2[0]:
#    print("OK")
#geocode_result = gmaps.geocode('1600 Amphitheatre Parkway, Mountain View, CA')
#test = gmaps.distance_matrix(['Brasília,DF','São Paulo,SP','Copacabana, RJ','Ipanema,RJ'],['Rio de Janeiro','Leblon,RJ','Lagoa,RJ','Ipanema,RJ'],mode="driving")
#a resposta de gmaps.distance_matrix será um dicionario com primeiro elemento origem, segundo destinos e terceiro os elementos de resposta de fato
#lista = test['rows']
lista =[]
#abrindo o tal do csv
with open('bairrosrio.csv',newline='') as csvfile:
    bairros = csv.reader(csvfile,delimiter=',')
    for bairro in bairros:

        #print(','.join(bairro))
        lista.append(bairro)

print(lista)
epty =[]
for elemento in lista:
    epty.append(elemento[0])
print(epty)
df = pd.read_csv("bairrosrio.csv")

# match = [s for s in epty if 'Paque' in s] achar substring

#adiciona Rio de janeiro para search na api
for i in range(len(epty)):
    epty[i]+=',Rio de Janeiro'

#ideia:dividir a tabela origemXdestino em blocos de 7x23 e entao percorrer 23 grupos de 7 linhas  e 7 grupos de 23 colunas
#matriz final tera dimensao origemxdestino
distancia = np.zeros((len(epty),len(epty)),dtype=int)
tempo = np.zeros((len(epty),len(epty)),dtype=int)
for i in range(8,23,1):
    for j in range(7):
        testando1 = gmaps.distance_matrix(epty[7*i:7*i+4],epty[23*j:23*j+23],mode='driving')#mudar modo para transit para pegar dados de transporte público
        testando2 = gmaps.distance_matrix(epty[7*i+4:7*i+7],epty[23*j:23*j+23],mode='driving')
        for k in range(4):
            for l in range(23):
               if(testando1['rows'][k]['elements'][l]['status']=='OK'):
                    distancia[7*i+k,23*j+l] = testando1['rows'][k]['elements'][l]['distance']['value']
                    tempo[7*i + k, 23*j + l] = testando1['rows'][k]['elements'][l]['duration']['value']
               else:
                   distancia[7 * i + k, 23 * j + l]=0
                   tempo[7 * i + k, 23 * j + l]=0
               #elif(testando1['rows'][k]['elements'][l]['status']=='ZERO_RESULTS'):

        for k in range(3):
            for l in range(23):
                if (testando2['rows'][k]['elements'][l]['status'] == 'OK'):
                    distancia[7*i+4+k,23*j+l] = testando2['rows'][k]['elements'][l]['distance']['value']
                    tempo[7*i + 4 + k, 23*j + l] = testando2['rows'][k]['elements'][l]['duration']['value']
                else:
                    distancia[7 * i + 4 + k, 23 * j + l]=0
                    tempo[7 * i + 4 + k, 23 * j + l]=0




#teste = gmaps.distance_matrix(epty[0:9],epty[0],mode='driving')
dist = pd.DataFrame(data = distancia,index = np.array(epty),columns= np.array(epty))
temp = pd.DataFrame(data = tempo,index = np.array(epty),columns= np.array(epty))
dist.to_csv('./distanciamatrix.csv',sep=",")
temp.to_csv('./tempomatrix.csv',sep=",")