# -*- coding: utf-8 -*-
"""
Created on Sun Jun 21 12:34:29 2015

@author: miha
"""

from geopy.geocoders import Nominatim
import numpy as np
import copy

# funkcija, ki doloci geografsko sirino in dolzino dolocenega mesta
def lokacija_mesta(mesto):
    geolocator = Nominatim()    
    loc = geolocator.geocode(mesto)    
    x = loc.latitude
    y = loc.longitude
    return (x,y)
    
    
    

# PRIMOV ALGORITEM
def najcenejse_vpeto_drevo(G):
    # funkcija vzame kot parameter matriko sosednosti (poln, utezen, neusmerjen graf)
    G = copy.deepcopy(G) # skopiramo graf (tehnicni python razlog)
    st_vozlisc = G.shape[0] # st vozlisc je kar dolzina matrike
    drevo_povezave = []
     
    # zacnemo z vozliscem 0:                                                                                         
    obiskana_vozlisca = [0]                                                                                    
    st_obiskanih = 1
    # izlocimo diagonalne "povezave", jim priredimo neskoncno vrednost
    diag_indices = np.arange(st_vozlisc)
    G[diag_indices, diag_indices] = np.inf
     
    while st_obiskanih != st_vozlisc: # obiskati moramo vsa vozlisca
        # pogledamo najcenejso povezavo iz obiskanih vozlisc
        nova_povezava = np.argmin(G[obiskana_vozlisca], axis=None)
        # moramo se deliti s stevilom vozlisc, da vemo iz katerega vozlisca gre povezava
        # zato ker np.argmin vrze ven le mesto v "matricnem seznamu", ne pa mesta v matriki
        nova_povezava = divmod(nova_povezava, st_vozlisc)
        nova_povezava = [obiskana_vozlisca[nova_povezava[0]], nova_povezava[1]]

        # dodamo povezavo v najcenejse drevo
        drevo_povezave.append(nova_povezava) 
        # oznacimo vozlisce kot obiskano 
        obiskana_vozlisca.append(nova_povezava[1])
        
        # oznacimo novo povezavo kot ze obdelano, ji priredimo vrednost inf      
        # oz. vsem vozliscem, ki imajo povezavo do tega vozlisca, da se izognemo ciklom
        G[obiskana_vozlisca, nova_povezava[1]] = np.inf
        G[nova_povezava[1], obiskana_vozlisca] = np.inf # "obratno" povezavo tudi                                                 
        st_obiskanih += 1
        
    return np.vstack(drevo_povezave) # vrnemo seznam povezav v našem drevesu
    
    
    
    
    
# DFS algoritem (iterativni)
# inputi so graf v dict obliki, zacetno vozlisce u, slovar orderjev,
# seznam mest in pa slovar razdalj
def dfs(graf, u, orders, mesta, dist):
    obiskani = [False for i in range(len(mesta))] #nastavimo vsa mesta kot neobiskana
    stack = [u] # seznam "aktivnih" vozlisc
    obiskani[u] = True # nastavimo zacetno vozlisce na obiskano
    # seznam prispevkov posameznih mest k izgradnji omrezja
    prispevki = [0 for i in range(len(mesta))]
    # poddrevo, sluzi za racunanje prispevkov
    poddreve = copy.deepcopy(orders)
    c = 1 # counter, ki šteje orderje
    preorder = [] # seznam mest po času prvega obiska
    postorder = [] # seznam mest po času zadnjega obiska
    preorder.append([c,u]) # zacetno vozlisce obiscemo najprej
    orders[mesta[u]].append(c) # napišemo še preorder vrednost
    poddreve[mesta[u]].append(u) # damo u v poddrevo
    # (v bistvu ni relevantno, ker u nima nobene vhodne povezave za placati)
 
    naslednjiStackElem = False # logical, ki meri ali gremo naprej v globino ali ne
    while len(stack) > 0: # dokler je stack neprazen izvajamo algoritem
        s = stack[-1] # gledamo zadnje dodano vozlisce
 
        naslednjiStackElem = False # recemo, da moramo se pregledati v globino
                                        # iz trenutnega vozlisca
        for v in graf[s]: # za vse povezave iz vozlisca s
            if naslednjiStackElem: # ce ne gledamo v globino gremo na naslednji while
                break
            if not obiskani[v]: # če v še ni bil obiskan
                stack.append(v) # ga damo na vrh (konec) stacka
                obiskani[v] = True # oznacimo kot obiskanega
                c += 1 # nastavimo order za eno naprej
                preorder.append([c,v]) # vpišemo preorder (ker smo vozlišče ravno obiskali)
                orders[mesta[v]].append(c)
                for k in stack: # za vse v stacku dodamo noter vozlišče v
                                # da bomo upoštevali, da se cena vseh prejšnjih povezav
                                # do centra porazdeli tudi med vozlišče v
                    poddreve[mesta[k]].append(v)
 
                # prvic ko pridemo do vozlisca
                # ga takoj procesiramo v naslednji while iteraciji (globina)
                 # pogledamo njegove sosede etc, vse kar je v for zanki
                 # to je bistvo DFS algoritma
                naslednjiStackElem = True
                continue
                # tukaj gremo na naslednjo while iteracijo (if pogoj na začetku for zanke)
 
        if not naslednjiStackElem: # pomeni, da smo prišli zadnjič do vozlišča s
            c += 1            
            postorder.append([c,s]) # nastavimo post-order
            orders[mesta[s]].append(c)
            
            # to je tehnično, zaradi spodnjega računanja prispevkov
            # ker drugače bi bil indeks k izven seznama (for zanka)
            if len(stack) < 2: 
                prispevki[s] += 0
            else:
                for k in poddreve[mesta[s]]:                    
                    prispevki[k] += dist[stack[-1]][stack[-2]] / len(poddreve[mesta[s]])
            stack.pop() # damo ven zadnje vozlisce iz stacka
            # outputi so seznam vozlisc urejen po preorderjih, seznam postorderjev,
                # prispevki posameznih vozlisc k izgradnji in poddrevo vsakega vozlisca do centra
    return preorder, postorder, orders, prispevki, poddreve