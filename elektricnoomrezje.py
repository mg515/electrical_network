# -*- coding: utf-8 -*-
"""
Created on Mon May 04 19:53:12 2015
"""

# nalozimo vse pakete, katerih funkcije bomo uporabljali
import pandas as pd
import os 
from geopy.distance import vincenty
import numpy as np
import copy
from funkcije import *


os.chdir("/home/miha/Documents/shortest_path_games/") # nastavimo working directory

# preberemo seznam najvecjih slovenskih mest
mesta = pd.read_pickle("mesta_series")

# izracun lokacij in razdalj med mesti

#lokacije_mest = [] # seznam geo dolzin in sirin nasih mest
#for i in mesta:
#    lokacije_mest.append(lokacija_mesta(i))


#n = len(mesta)
#razdalje_mat = np.zeros((n, n))
#for i in range(len(mesta)):
#    for j in range(len(mesta)):
#        if i==j:
#            razdalje_mat[i][j] = 0
#        else:
#            loc1 = lokacije_mest[i]
#            loc2 = lokacije_mest[j]
            # v i,j-to mesto v matriki dodamo zracno razdaljo
            # med i-tim in j-tim mestom
#            dist = vincenty(loc1, loc2).km
#            razdalje_mat[i][j] = dist

# shranimo v datoteko
#razdalje = pd.DataFrame(razdalje_mat, index=mesta, columns=mesta)
#razdalje.to_pickle("razdalje")

# nalozimo naso matriko razdalj
razdalje = pd.read_pickle("razdalje")
razdalje_mat = pd.DataFrame.as_matrix(razdalje)


razdalje_mat = razdalje_mat[0:10, 0:10] # testni primer zgolj na 10 mestih
seznam = najcenejse_vpeto_drevo(razdalje_mat)

# spodnji razdelek sluzi za pisanje najcenejsega drevesa v matricno obliko
# hkrati zaokrozimo razdaljo na 3 decimalke
mesta = mesta[0:10]
n = len(mesta)
mst = np.zeros((n, n))
for i in seznam:
    mst[i[0]][i[1]] = round(razdalje_mat[i[0]][i[1]], 3)
    mst[i[1]][i[0]] = round(razdalje_mat[i[0]][i[1]], 3)


# zapisemo nas MST tudi v dictionary data type
gdict = dict()
raz = copy.deepcopy(mst)
mesta = mesta[0:10]
for i in range(len(mesta)):
    kat = [j for j in range(len(mesta)) if raz[i][j] > 0]
    gdict[i] = set(kat)


# (zaenkrat) prazen slovar pre-order in post-order vrednosti
orders = dict()
for i in range(len(mesta)):
    orders[mesta[i]] = []


pre, po, orders, prispevki, poddreve = dfs(gdict, 0, orders, mesta, raz)


# printamo prispevke
for i in range(len(prispevki)):
    print mesta[i]
    print prispevki[i]


# dodamo še prispevke glede na velikost kraja
# večji kot je kraj, dražji je "transformator", ki ga mesto potrebuje
# za nemoteno oskrbovanje z elektriko
prebs = np.genfromtxt('prebivalci.csv')
prebs = prebs/1000
prebs = np.ndarray.tolist(prebs)
prispevki = prispevki + prebs


####
# generiranje naključnega grafa

def randomgraf(n):
    G = np.random.randint(n, size=(n,n))
    for i in range(1,n):
        for j in range(i):
            G[i][j] = G[j][i]
    return G


n = 10000
rg = np.random.random_integers(1,1000,size=(n,n))
rg_sym = (rg + rg.T)/2

# matrike 10000 * 10000 ogromne, en element porabi 24 bytov, sys.getsizeof(x)
# torej cela matrika 2.4 gigabyte
# 100k * 100k bi porabila 240 gigabytov