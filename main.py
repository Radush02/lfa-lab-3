def lambda_inchid(stari, nfa):
    st=[]
    for x in stari:
        st.append(x)
    l_inchidere = set(stari)
    while st:
        curr=st.pop()
        if 'l' in nfa[curr]:
            for urm in nfa[curr]['l']: #pt fiecare stare in care avem s-(l)->t
                if urm not in l_inchidere: #daca starea nu e in l_i adaugam si pune pe stiva
                    l_inchidere.add(urm)
                    st.append(urm)
    return list(l_inchidere)

def nfa_to_dfa(nfa,st_init,alfabet):
    dfa = {}
    l_inchid_init = sorted(lambda_inchid([st_init], nfa)) #initializez m. starilor din afd cu l_i(st_init)
    d_stari = [l_inchid_init] # m stari afd
    tranz = set() #m. tranzitiilor
    while d_stari: # cat timp avem o stare x nemarcata
        prelucram_stare = d_stari.pop(0) #marcam
        if tuple(prelucram_stare) in tranz:
            continue
        tranz.add(tuple(prelucram_stare))
        dfa[tuple(prelucram_stare)] = {}
        for lit in alfabet:
            next = set() # mult starilor pt care exista o tranz de la lit la o stare s din x
            for nfa_state in prelucram_stare:
                next.update(nfa.get(nfa_state, {}).get(lit, []))
            lambda_mutare = sorted(lambda_inchid(next, nfa))
            if tuple(lambda_mutare) not in tranz:
                d_stari.append(lambda_mutare) #adaug tranzitia daca ca nu e
            dfa[tuple(prelucram_stare)][lit] = tuple(lambda_mutare)  #pt ca l_i nu e in afd
    return dfa

def main():
    f=open("date.in",'r')
    stare_l_inchid_initiala=f.readline().strip().split()[0]
    stari=f.readline().strip().split()
    stari_finale=f.readline().strip().split()
    tranzitii={x:{} for x in stari}
    alfabet=set()
    for x in f.readlines():
        x=x.strip().split()
        try:
            tranzitii[x[0]][x[1]]+=x[2]
        except:
            tranzitii[x[0]][x[1]]=x[2]
    for x in tranzitii:
        for w in tranzitii[x]:
            if(w!='l'):
                alfabet.add(w)
            rez = list('q'+substr for substr in tranzitii[x][w].split('q') if substr)
            tranzitii[x][w]=rez
    print(tranzitii)
    dfa=nfa_to_dfa(tranzitii,stare_l_inchid_initiala,alfabet)

    print("stare | lit | st urm")
    for stare in dfa:
        if stare != ():
            for lit in dfa[stare]:
                starea_urm = dfa[stare][lit]
                print(f"{stare} {lit} {starea_urm}\n")

    print(f"stari finale: {stari_finale}")
if __name__=="__main__":
    main()