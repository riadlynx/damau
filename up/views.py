
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
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from .models import *
# Create your views here.

def signup(request):
    if request.method == "POST":
        form = SignUp(request.POST)
        if form.is_valid():
            user = User.objects.create_user(form.cleaned_data['username'], form.cleaned_data['email'], form.cleaned_data['password'])
            user.first_name = form.cleaned_data['firstname']
            user.last_name = form.cleaned_data['lastname']
            user.save()
            profile = Profile.objects.create(user=user,occupation=form.cleaned_data['occup'],tel = form.cleaned_data['phone'],company = form.cleaned_data['company'])
            login(request, user)
            return redirect('index')
    else:
        form = SignUp()

    context = {'form':form}

    template = loader.get_template('registration/signup.html')
    return HttpResponse(template.render(context, request))

@login_required
def index(request):
    profile = Profile.objects.get(user=request.user)
    todos = todo.objects.filter(prof=profile).order_by('date')
    if request.method == "POST":
        if 'todo' in request.POST:
            form = AddTodo(request.POST)
            if form.is_valid():
                model = todo()
                model.todo = form.cleaned_data['name']
                model.date = form.cleaned_data['date']
                model.prof = profile
                model.save()
                return redirect('index')
        elif 'barrage' in request.POST:
            form = AddBarrage(request.POST)
            if form.is_valid():
                model = Barrage()
                model.name = form.cleaned_data['name']
                model.BV = form.cleaned_data['BV']
                model.P = form.cleaned_data['P']
                model.O = form.cleaned_data['O']
                model.T = form.cleaned_data['T']
                model.RN = form.cleaned_data['RN']
                model.PHE = form.cleaned_data['PHE']
                model.prof = profile
                model.save()
                return redirect('barrages')
    else:
        form = AddTodo()
        form1= AddBarrage()

    context = {'profile':profile,'todos':todos,'form':form,'form1':form1}

    template = loader.get_template('up/index.html')
    return HttpResponse(template.render(context, request))
@login_required
def todod(request,todoid):
    todo.objects.get(id=todoid).delete()
    return redirect('index')
@login_required
def barrages(request):
    profile = Profile.objects.get(user=request.user)
    if request.method == "POST":
        form = AddBarrage(request.POST)
        if form.is_valid():
            model = Barrage()
            model.name = form.cleaned_data['name']
            model.BV = form.cleaned_data['BV']
            model.P = form.cleaned_data['P']
            model.O = form.cleaned_data['O']
            model.T = form.cleaned_data['T']
            model.RN = form.cleaned_data['RN']
            model.PHE = form.cleaned_data['PHE']
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
        form = Addinst(request.POST)
        if form.is_valid():
            model = Instrument()
            model.name = form.cleaned_data['name']
            model.bar = barrage
            model.save()
            return redirect('barrage',barrageid=barrage.id)
    else:
        form = Addinst()
    instruments = Instrument.objects.filter(bar=barrage.id)
    context={'instruments':instruments , 'barrage':barrage,'form':form,'profile':profile}
    template = loader.get_template('up/inst.html')
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
        start_ = np.datetime64(start)
        end = request.GET.get('end')
        end_= np.datetime64(end)
        ggg = exreg(fich.fich.path, start, end)
        ccc = exreg1(ggg[0], ggg[1])
        coe = ccc[0].coef_
        con = ccc[0].intercept_
        sco = ccc[1]*100
        sco="%.2f" % sco
        delta = (ggg[4][ggg[3]]-ggg[4][ggg[2]]).astype('int')/365
        delta = round (delta,2)
        coe1=coe[0][0]*delta*365
        coe1="%.2f" % coe1
        print(coe,con)

    else:
        tt = 'non supported'
    form = datereg()

    if fich.inst.bar.prof != profile:
        render(request,"You don't have access to this document.")
    y1 = pd.read_excel(fich.fich.path, parse_cols=[1])
    y2 = pd.read_excel(fich.fich.path, parse_cols=[2])
    x = pd.read_excel(fich.fich.path, parse_cols=[0])


    fig, ax2 = pit.subplots(figsize=(14, 6))
    ax1 = ax2.twinx()



    T1=[]
    T2=[]
    if showderive == 'true':

#Dérive
        for i in ggg[5]:
            T1.append(i * coe[0][0] + con[0])
        for i in ggg[4]:
            T2.append(i * coe[0][0] + con[0])
#Mesures Corrigé

        # vecteur s
        s_ = []
        for i in ggg[7]:
            s_.append(2 * math.pi * (i - ggg[8]).astype('timedelta64[D]').astype('int') / 365.25)
        # #print(s)

        # Z
        Z_ = []
        for i in ggg[6]:
            Z_.append((ggg[10] - i) / ggg[12])
        # Z2
        Z2_ = []
        for i in Z_:
            Z2_.append(i * i)
        # Z3
        Z3_ = []
        for i in Z_:
            Z3_.append(i * i * i)

        # Z4
        Z4_ = []
        for i in Z2_:
            Z4_.append(i * i)

        # cos
        cos_ = []
        for i in s_:
            cos_.append(math.cos(i))

        # sin
        sin_ = []
        for i in s_:
            sin_.append(math.sin(i))

        # cos2
        cos2_ = []
        for i in s_:
            cos2_.append(math.cos(2 * i))

        # sin2
        sin2_ = []
        for i in s_:
            sin2_.append(math.sin(2 * i))

        MC = []
        for i in range(len(Z_)):
            MC.append(ggg[9][i] - Z_[i] * coe[0][1] - Z2_[i] * coe[0][2] - Z3_[i] * coe[0][3] - Z4_[i] * coe[0][4] - cos_[i] *coe[0][5] - sin_[i] * coe[0][6] - cos2_[i] * coe[0][7] - sin2_[i] * coe[0][8])


        #ploting derive w mc
        ax1.plot(x, T1, color='lime', label="Extrapolation de la dérive (mm)", linewidth=2, )
        ax1.plot(x[ggg[2]:ggg[3] + 2], T2, color='g', label="Dérive sur la période (mm)", linewidth=4)
        ax1.plot(x, MC, color='darkred', label="Mesures Corrigées (mm)",marker='o',linestyle='' )
        titre = "Analyse HST , Dérive"
        pit.title(titre)
# max et min
        mean = 0
        for i in ggg[9]:
            mean += i
        mean= mean/len(ggg[9])

        mean1 = 0
        for i in ggg[9]:
            mean1 += abs(i-mean)
        mean1= mean1/len(ggg[9])
        mx=[]
        mn=[]
        np.asarray(mx)
        for i in T1:
            mx.append(i + mean1)
            mn.append(i-mean1)
        ax1.plot(x, mx, color='y', label="Max (mm)", linewidth=2, )
        ax1.plot(x, mn, color='y', label="Min (mm)", linewidth=2, )

    # plotting
    ax1.plot(x, y1, color='b', label='Mesures Brutes (mm)')
    ax1.set_xlabel('temps')
    ax1.legend(loc='upper right', bbox_to_anchor=(1, 1))

    ax2.plot(x, y2, color='xkcd:sky blue', label="Niveau d'eau (m)")
    ax2.legend(loc='upper left', bbox_to_anchor=(0, 1))
    #ax1.set_ylabel("<--- soulèvement,vers l'amont || tassement,vers l'aval --->", size='20')
    ax2.patch.set_alpha(0.0)
    ax1.patch.set_alpha(0.0)


    pit.axis()
    graphkhawi = mpld3.fig_to_html(fig)

    context = {'file': fich,'graph':graphkhawi,'form': form,  'start': start, 'end': end,'coe': coe,'con':con,'sco':sco , 'delta':delta,'coe1':coe1}
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
    print(type(Y[0][0]))
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
    Ynl=Y
    wlnl=wl
    ttnl=tt
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
    for i in ttnl:
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
    for i in range( len(Z)):
        X.append([T[i], Z[i], Z2[i], Z3[i], Z4[i], cos[i], sin[i], cos2[i], sin2[i]])
    X = np.asarray(X)





    return X,Y,closest,closest1,T,Tnl,wlnl,ttnl,first,Ynl,maxwl,minwl,deltamaxmin

def exreg1(X,Y):

    regr = linear_model.LinearRegression()
    regr.fit(X, Y)


    Score= regr.score(X, Y)
    regr.coef_
    regr.intercept_



    return regr,Score


