# -*- coding: utf-8 -*-
"""
Created on Tue Jun 14 09:43:56 2022

@author: efrui
"""

import pandas as pd 
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import requests
import json

## Extracción de datos
response_API = requests.get('https://analytics.deacero.com/api/teenus/get-data/c744a2a4-ab89-5432-b5e6-9f320162e160')
data = response_API.json()
hotel = pd.DataFrame(data)

#%%
## Limpieza de Datos

hotel.describe(include='all')

hotel.head(10)

print(hotel.dtypes)

hotel['stays_in_weekend_nights'] = hotel['stays_in_weekend_nights'].astype(int)
hotel['stays_in_week_nights'] = hotel['stays_in_week_nights'].astype(int)
hotel['adults'] = hotel['adults'].astype(int)
hotel['babies'] = hotel['babies'].astype(int)
hotel['adr'] = hotel['adr'].astype(float)
hotel['previous_cancellations'] = hotel['previous_cancellations'].astype(int)
hotel['previous_bookings_not_canceled'] = hotel['previous_bookings_not_canceled'].astype(int)
hotel['days_in_waiting_list']= hotel['days_in_waiting_list'].astype(int)
hotel['lead_time'] = hotel['lead_time'].astype(int)
hotel['required_car_parking_spaces'] = hotel['required_car_parking_spaces'].astype(int)
hotel['total_of_special_requests'] = hotel['total_of_special_requests'].astype(int)


print(hotel.dtypes)

#%%
#Caso especial de los niños cuyo valor era 'NA'
index = hotel['children'].replace('NA','0')

hotel['children'] = index.astype(int)
print(hotel.dtypes)

#Caso especial para agente y compañía, sin embargo, ellos son strings por lo que no es necesario deshacerse de los null's
hotel['company'] = hotel['company'].astype(str)
hotel['agent'] = hotel['agent'].astype(str)


#%%
# Trabajar con los valores nulos.

missing_data = hotel.isnull()
for column in missing_data.columns.values.tolist():
    print(column)
    print(missing_data[column].value_counts())
    print('')

#No faltan datos, no hay nada que hacer entonces.
    
#%%
# ¿De dónde vienen los huéspedes?

countries = pd.DataFrame(hotel['country'].value_counts())
countries.rename(columns = {'country':'N_of_clients'}, inplace=True)
countries["c"] = countries.index
print('Dado que hay 195 países reconocidos por la ONU y tenemos que las personas vienen de 178 países diferentes, podemos decir que los huéspedes vienen de casi todo el mundo. \n')
coun = countries.iloc[[0,1,2,3,4,5,6,7]]
p = countries[countries['N_of_clients'] < 2500]['N_of_clients'].sum()
coun.loc[8] = [p , "OTHERS"]


print("Particularmente, en la siguiente gráfica se puede apreciar, por países, aquellos que representan una mayor cantidad de huéspedes \n")
print("los cuales son: Portugal, Inglaterra, Francia, España y Alemania")
    
fig = plt.figure(figsize =(7, 7))
plt.pie(coun['N_of_clients'], labels=coun['c'], colors = sns.color_palette('coolwarm'), autopct='%.0f%%')
plt.savefig('pie_plot.png') 
plt.show()


#%%
   #¿Cuánto pagan en promedio las personas por habitación por noche?
   
   #Contando todas
print("Si contamos todas, el promedio por habitación reservada es: " + str(hotel['adr'].mean()) + "\n")
   
#Segmentando por hotel
hotel_city = hotel[hotel['hotel'] == 'City Hotel']
hotel_resort = hotel[hotel['hotel'] == 'Resort Hotel']
   
#Primero hay que filtrar a las que sí reservaron
print("Si contamos todas, el promedio por noche en el hotel City es " + str(hotel_city['adr'].mean()) + "\n")
print("Si contamos todas, el promedio por noche en el hotel Resort es " + str(hotel_resort['adr'].mean()) + "\n")
   
   
# De una vez podemos contestar la pregunta de cuántas reservaciones fueron canceladas
print("El número de reservaciones canceladas en total es: " + str(hotel[hotel['is_canceled'] == '1'].shape[0]) + "\n")
   
#Además podemos contestar el mes con el mayor número de cancelaciones en total
   
hotel_cancel = hotel[hotel['is_canceled'] == '1']
hotel_cancel_month = hotel_cancel[['arrival_date_year','arrival_date_month']].value_counts()


print(hotel_cancel_month.head(5))
print("Se nota que los meses con mayores cancelaciones son Mayo 2017, Octubre 2016 y Abril 2017")

#%%
   #Variación de la noche a lo largo del año.
   #Primero agrupamos por mes, a todos.
hotel_city = hotel_city.sort_values(by = ['arrival_date_year', 'arrival_date_week_number'])
hotel_resort = hotel_resort.sort_values(by = ['arrival_date_year', 'arrival_date_week_number'])        

hotel_2015 = hotel_city[hotel_city['arrival_date_year'] == 2015]
hotel_2015_c = pd.DataFrame(hotel_2015.groupby(['arrival_date_week_number'])['adr'].mean())
hotel_2015_c['week'] = hotel_2015_c.index
hotel_2015_c['year'] = 2015

hotel_2016 = hotel_city[hotel_city['arrival_date_year'] == 2016]
hotel_2016_c = pd.DataFrame(hotel_2016.groupby(['arrival_date_week_number'])['adr'].mean())
hotel_2016_c['week'] = hotel_2016_c.index
hotel_2016_c['year'] = 2016

hotel_2017 = hotel_city[hotel_city['arrival_date_year'] == 2017]
hotel_2017_c = pd.DataFrame(hotel_2017.groupby(['arrival_date_week_number'])['adr'].mean())
hotel_2017_c['week'] = hotel_2017_c.index
hotel_2017_c['year'] = 2017

hotel_2015 = hotel_resort[hotel_resort['arrival_date_year'] == 2015]
hotel_2015_r = pd.DataFrame(hotel_2015.groupby(['arrival_date_week_number'])['adr'].mean())
hotel_2015_r['week'] = hotel_2015_r.index
hotel_2015_r['year'] = 2015

hotel_2016 = hotel_resort[hotel_resort['arrival_date_year'] == 2016]
hotel_2016_r = pd.DataFrame(hotel_2016.groupby(['arrival_date_week_number'])['adr'].mean())
hotel_2016_r['week'] = hotel_2016_r.index
hotel_2016_r['year'] = 2016

hotel_2017 = hotel_resort[hotel_resort['arrival_date_year'] == 2017]
hotel_2017_r = pd.DataFrame(hotel_2017.groupby(['arrival_date_week_number'])['adr'].mean())
hotel_2017_r['week'] = hotel_2017_r.index
hotel_2017_r['year'] = 2017

hotel_c =pd.concat([hotel_2015_c, hotel_2016_c,hotel_2017_c],    # Combine vertically
                          ignore_index = True,
                          sort = False)

hotel_r =pd.concat([hotel_2015_r, hotel_2016_r,hotel_2017_r],    # Combine vertically
                          ignore_index = True,
                          sort = False)

#Plots
print("En las siguientes gráficas se muestra la variación del adr promedio por semana, segmentado por hotel y año")


f1 = sns.relplot(
    data=hotel_c,
    x="week", y="adr", col = "year", color = "blue")
plt.savefig('f1.png', orientation="landscape")


f2 = sns.relplot(
    data=hotel_r,
    x="week", y="adr", col = "year", color = "red")
plt.savefig('f2.png', orientation="landscape")


print("\n Se ve una tendencia de pico entre las semanas 30 y 40, lo cual es de esperarse por ser las vacaciones de verano en el hotel Resort, pero no se ve el mismo comportamiento en el hotel City" )
#%%
  # Meses más ocupados
  

Months_2015 = pd.DataFrame(hotel[(hotel["is_canceled"] == '0') & (hotel["arrival_date_year"] == 2015)]['arrival_date_month'].value_counts())
Months_2015['m-year'] = Months_2015.index + " 2015"

Months_2016 = pd.DataFrame(hotel[(hotel["is_canceled"] == '0') & (hotel["arrival_date_year"] == 2016)]['arrival_date_month'].value_counts())
Months_2016['m-year'] = Months_2016.index + " 2016"
    
Months_2017 = pd.DataFrame(hotel[(hotel["is_canceled"] == '0') & (hotel["arrival_date_year"] == 2017)]['arrival_date_month'].value_counts())
Months_2017['m-year'] = Months_2017.index + " 2017"

Months = pd.concat([Months_2015,Months_2016,Months_2017], ignore_index = False)
Months.rename(columns = {'arrival_date_month':'No_of_oc'}, inplace=True)
Months.sort_values(by=['No_of_oc'])  

sns.barplot(x=Months[Months['No_of_oc']> 3300]['m-year'], y=Months[Months['No_of_oc']> 3300]['No_of_oc'], palette="magma",data=Months)
plt.xlabel("Month-Year")
plt.ylabel("Number of occupations")
plt.xticks(rotation=30)
plt.savefig('bar_plot.png') 

print("""Los meses más ocupados son Octubre-2016, Mayo-2016 y Mayo-2017, el primero por haber sido en ese tiempo la primer ronda de la Copa del Mundo, en la cual Portugal tuvo dos partidos como local. Mayo de ambos años debido a que hay muchas festividades, las más notoria es "Las peregrinaciones a Fátima"\n """)
    
    
#%%
    #¿Cuánto tiempo se queda la gente en los hoteles (noche)?
    #Primero, sumaremos el numero de noches en total, en una nueva columna

hotel_yes = hotel[hotel['is_canceled'] == '0']
hotel_yes['total_n'] = hotel_yes[["stays_in_week_nights", "stays_in_weekend_nights"]].sum(axis=1, skipna=True)


#Calculamos el máximo y el mínimo
M = hotel_yes['total_n'].max()
m = hotel_yes['total_n'].min()

print("Los huespédes se alojan desde " + str(m) + " noches hasta " + str(M) + " noches")    
    
#%%
#Reservas por segmento de mercado

print("Las reservas por segmento de mercado son: ")
print(hotel['market_segment'].value_counts())

#%%    
    #Correlacion
    
print("Para el año 2015 \n")

corr2015 = hotel_2015.drop(columns = ["arrival_date_year"]).corr ()
plt.figure(figsize=(8,8))
ax = sns.heatmap(corr2015, annot=True, linecolor='white',linewidths=.3, fmt='.2f', cbar=True, cmap=(sns.color_palette("Blues")))
    
print("Para el año 2016 \n")

corr2016 = hotel_2016.drop(columns = ["arrival_date_year"]).corr ()
plt.figure(figsize=(8,8))
ax = sns.heatmap(corr2016, annot=True, linecolor='white',linewidths=.3, fmt='.2f', cbar=True, cmap=(sns.color_palette("Reds")))
    
print("Para el año 2017 \n")

corr2017 = hotel_2017.drop(columns = ["arrival_date_year"]).corr ()
plt.figure(figsize=(8,8))
ax = sns.heatmap(corr2017, annot=True, linecolor='white',linewidths=.3, fmt='.2f', cbar=True, cmap=(sns.color_palette("Greens")))
    
    
    
#%%

#Segmentación de las canelaciones por merket_segment
h = pd.DataFrame(hotel_cancel['market_segment'].value_counts())
h.rename(columns = {'market_segment':'cancelations'}, inplace = True)
h['market_segment'] = h.index
    

fig = plt.figure(figsize =(7,10))
sns.catplot(data=h, kind="bar", x="market_segment", y="cancelations", palette = 'dark')
plt.xlabel("Market_segment")
plt.ylabel("Number of cancelations")
plt.xticks(rotation=45)
plt.savefig('hist_plot.png')    
    
#%%

#Aquí nos fijamos en cuántas veces nos han cancelado, nuevos clientes o clientes repetidos


print(hotel_cancel['previous_bookings_not_canceled'].value_counts())
print("En estas tablas vemos que los no estamos logrando captar bien a los clientes nuevos")

fig = plt.figure(figsize =(7,10))
g = sns.FacetGrid(hotel_cancel, col="is_repeated_guest", height=4, aspect=1)
g.map(sns.histplot, "previous_bookings_not_canceled", color="turquoise")

  
    
    
    
    