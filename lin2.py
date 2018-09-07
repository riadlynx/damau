import numpy as np
import pandas as pd
from sklearn import linear_model
from datetime import date, datetime, timedelta
import math



#il faut preparer son excel sous format excel de la facon suivante : datetime | mesure | water level(Crp)

df = pd.read_excel("ttt.xlsx")

#Y
Y=(df.iloc[0:,1:2])
Y = Y.values

#recherche de la première année
year=(df.iloc[0:1,0:1]) #format dataframe
year = year.values          #dataframe à vecteur  numpy
first = str(year[0][0]).split("-")[0]
first = np.datetime64(first+'-01-01')
print("hhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhh",first,type(first))
#wl et max wl et min wl
vals = df.iloc[0:,2:3].values
wl = []
for i in vals:
    wl.append(i[0])

maxwl= max(wl)
minwl= min(wl)
deltamaxmin=maxwl-minwl

#T
tt = []
tp = df.iloc[0:,0:1].values  #values pour traiter comme matrice numpy
for i in tp:     #changement de format string à datetime
    tt.append(i[0])
T = []              #remplissage vecteur T
for i in tt:
    T.append((i-tt[0]).astype('timedelta64[D]').astype('float64'))

print(type(T[0]))

#vecteur s

s = []
for i in tt:
    s.append(2*math.pi*(i-first).astype('timedelta64[D]').astype('float64')/365.25)
#print(s)


#Z
Z=[]
for i in wl:
    Z.append((maxwl-i)/deltamaxmin)
#Z2
Z2=[]
for i in Z:
    Z2.append(i*i)
#Z3
Z3=[]
for i in Z:
    Z3.append(i*i*i)

#Z4
Z4=[]
for i in Z2:
    Z4.append(i*i)

#cos
cos=[]
for i in s:
    cos.append(math.cos(i))

#sin
sin=[]
for i in s:
    sin.append(math.sin(i))

#cos2
cos2=[]
for i in s:
    cos2.append(math.cos(2*i))

#sin2
sin2=[]
for i in s:
    sin2.append(math.sin(2*i))


#matrice X
X = []
for i in range(0,len(Y)):
    X.append([T[i],Z[i],Z2[i],Z3[i],Z4[i],cos[i],sin[i],cos2[i],sin2[i]])
X = np.asarray(X)

regr = linear_model.LinearRegression()
regr.fit(X,Y)
regr.score(X, Y)

regr.coef_
print(regr.coef_)
print(regr.intercept_)
print(regr.score(X, Y))
