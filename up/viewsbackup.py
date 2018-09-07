
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader
from sklearn import linear_model
import numpy as np
from datetime import date, datetime, timedelta
import math
import pandas as pd
from .forms import *
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as pit,mpld3


from django.contrib.auth.decorators import login_required
from .models import *
# Create your views here.
@login_required
def barrages(request):
    profile = Profile.objects.get(user=request.user)
    if request.method == "POST":
        form = AddBarrage(request.POST)
        if form.is_valid():
            model = Barrage()
            model.name = form.cleaned_data['name']
            model.prof = profile
            model.save()
            return redirect('barrages')
    else:
        form = AddBarrage()
    barrages = Barrage.objects.filter(prof=profile)
    context = {'barrages':barrages,'profile':profile,'form':form}
    template = loader.get_template('up/barrages.html')
    return HttpResponse(template.render(context, request))
@login_required
def barrage(request, barrageid):
    profile = Profile.objects.get(user=request.user)
    barrage = Barrage.objects.get(pk=barrageid)
    if barrage.prof != profile:
        return render(request," had l barrage mashi nta3k ")
    if request.method == "POST":
        form = AddBarrage(request.POST)
        if form.is_valid():
            model = Instrument()
            model.name = form.cleaned_data['name']
            model.bar = barrage
            model.save()
            return redirect('barrage',barrageid=barrage.id)
    else:
        form = AddBarrage()
    instruments = Instrument.objects.filter(bar=barrage.id)
    context={'instruments':instruments , 'barrage':barrage,'form':form,'profile':profile}
    template = loader.get_template('html/dashboard.0.html')
    return HttpResponse(template.render(context, request))
@login_required
def fich(request, instrumentid):
    profile = Profile.objects.get(user=request.user)
    inst = Instrument.objects.get(pk=instrumentid)
    if inst.bar.prof != profile:
        return render(request,"you don't have access to this document")
    if request.method == "POST":
        form = AddFile(request.POST, request.FILES)
        if form.is_valid():
            model = Fileup()
            model.fich = form.cleaned_data['fich']
            model.inst = inst
            model.save()
            return redirect('appareils',instrumentid=inst.id)
    else:
        form = AddFile()
    fichs = Fileup.objects.filter(inst=inst)
    context={'fichs':fichs,'instrument':inst,'form':form,'profile':profile}
    template = loader.get_template('up/fichlist.html')
    return HttpResponse(template.render(context, request))
@login_required
def fichdelete(request,fileid):
    fich = Fileup.objects.get(id = fileid)
    fich.fich.delete()
    fich.delete()
    return redirect('appareils', instrumentid=fich.inst.id)
@login_required
def graph(request, fileid):
    profile = Profile.objects.get(user=request.user)
    fich = Fileup.objects.get(id = fileid)
    ext = fich.fich.path.split(".")[1]
    showderive = request.GET.get('showhst')
    if ext == 'xlsx' or ext == 'xls':
        start = request.GET.get('start')
        end = request.GET.get('end')
        ggg = exreg(fich.fich.path, start, end)
        ccc = exreg1(ggg[0], ggg[1])
        coe = ccc[0].coef_
        con = ccc[0].intercept_
        sco = ccc[1]
        print("coeffs",coe)
        print("const ",con)
        print("R²",sco)


    else:
        tt = 'non supported'
    form = datereg()

    if fich.inst.bar.prof != profile:
        render(request,"You don't have access to this document.")
    y1 = pd.read_excel(fich.fich.path, parse_cols=[1])
    y2 = pd.read_excel(fich.fich.path, parse_cols=[2])
    x = pd.read_excel(fich.fich.path, parse_cols=[0])






    fig, ax1 = pit.subplots(figsize=(14, 6))




    T1=[]
    T2=[]
    if showderive == 'true':
        for i in ggg[5]:
            T1.append(i * coe[0][0] + con[0])
        ax1.plot(x,T1,color='g',label="Extrapolation de la dérive")
        for i in ggg[4]:
            T2.append(i * coe[0][0] + con[0])
        ax1.plot(x[ggg[2]:ggg[3] + 2], T2, color='r', label="Dérive sur la période")

        print("gggggggggggg", type(ggg[4]))

    ax1.plot(x, y1,color='b',label='Mesures Brutes')
    ax1.set_xlabel('temps')
    ax1.set_ylabel('Mesures Brutes (mm)', color='b')
    ax1.legend(loc='upper left', bbox_to_anchor=(0,1))

    ax2 = ax1.twinx()
    ax2.plot(x, y2,color='xkcd:sky blue',label="Niveau d'eau")
    ax2.set_ylabel("Niveau d'eau (m)", color='xkcd:sky blue')
    ax2.tick_params( color='xkcd:sky blue')
    ax2.legend(loc='upper right')

    ax2.patch.set_alpha(0.0)
    ax1.patch.set_alpha(0.0)
    pit.title(fich.inst)
    graphkhawi = mpld3.fig_to_html(fig)

    context = {'file': fich,'graph':graphkhawi,'form': form,  'start': start, 'end': end,'coe': coe,'con':con,'sco':sco}
    template = loader.get_template('up/fich.html')
    return HttpResponse(template.render(context, request))
@login_required
def rapports(request):
    profile = Profile.objects.get(user=request.user)
    rapports = Rapport.objects.filter(prof=profile)
    context = {'rapports':rapports, 'profile':profile}
    template = loader.get_template('up/rapports.html')
    return HttpResponse(template.render(context, request))
@login_required
def rapport(request,rapportid):
    profile = Profile.objects.get(user=request.user)
    rapport = Rapport.objects.get(id = rapportid)
    context = {'rapport':rapport, 'profile':profile}
    template = loader.get_template('up/rapport.html')
    return HttpResponse(template.render(context, request))

def exreg(file,start,end):
    df = pd.read_excel(file)

    # Y
    Y = (df.iloc[0:, 1:2])
    Y = Y.values

    # recherche de la première année
    year = (df.iloc[0:1, 0:1])  # format dataframe
    year = year.values  # dataframe à vecteur  numpy
    first = str(year[0][0]).split("-")[0]
    first = np.datetime64(first + '-01-01')

    # wl et max wl et min wl
    vals = df.iloc[0:, 2:3].values
    wl = []
    for i in vals:
        wl.append(i[0])

    maxwl = max(wl)
    minwl = min(wl)
    deltamaxmin = maxwl - minwl

    # T
    tt = []
    tp = df.iloc[0:, 0:1].values  # values pour traiter comme matrice numpy
    for i in tp:  # changement de format string à datetime
        tt.append(i[0])
    closest = 0
    if start == None:
        start = tt[0]
    else:
        start = np.datetime64(start)
    if end == None:
        end = tt[-1]
    else:
        end = np.datetime64(end)
    ic = (tt[0]-start).astype('timedelta64[D]').astype('int')
    ic = abs(ic)

    for i in range(len(tt)-1):
        timede = abs((tt[i]-start).astype('timedelta64[D]').astype('int'))
        if timede<ic:
            ic=timede
            closest = i

    closest1 = 0
    ic1 = (tt[0]-end).astype('timedelta64[D]').astype('int')
    ic1 = abs(ic1)
    for i in range(len(tt)-1):
        timede = abs((tt[i] - end).astype('timedelta64[D]').astype('int'))
        if timede<ic1:
            ic1=timede
            closest1 = i



    #tous et limité pour trouver les coeffi de regresion

    Y = Y[closest:closest1+2]
    wl = wl[closest:closest1+2]
    T = []  # remplissage vecteur T
    for i in tt:
        T.append((i - tt[0]).astype('timedelta64[D]').astype('int'))

    Tnl=T       #vect non limité
    T=T[closest:closest1+2]
    tt = tt[closest:closest1+2]

    # vecteur s
    s = []
    for i in tt:
        s.append(2 * math.pi * (i - first).astype('timedelta64[D]').astype('int') / 365.25)
    # #print(s)

    # Z
    Z = []
    for i in wl:
        Z.append((maxwl - i) / deltamaxmin)
    # Z2
    Z2 = []
    for i in Z:
        Z2.append(i * i)
    # Z3
    Z3 = []
    for i in Z:
        Z3.append(i * i * i)

    # Z4
    Z4 = []
    for i in Z2:
        Z4.append(i * i)

    # cos
    cos = []
    for i in s:
        cos.append(math.cos(i))

    # sin
    sin = []
    for i in s:
        sin.append(math.sin(i))

    # cos2
    cos2 = []
    for i in s:
        cos2.append(math.cos(2 * i))

    # sin2
    sin2 = []
    for i in s:
        sin2.append(math.sin(2 * i))

    # matrice X limité pour regression
    X = []
    for i in range(0, len(Z)):
        X.append([T[i], Z[i], Z2[i], Z3[i], Z4[i], cos[i], sin[i], cos2[i], sin2[i]])
    X = np.asarray(X)



    return X,Y,closest,closest1,T,Tnl

def exreg1(X,Y):

    regr = linear_model.LinearRegression()
    regr.fit(X, Y)


    Score= regr.score(X, Y)
    regr.coef_
    regr.intercept_

    return regr,Score

