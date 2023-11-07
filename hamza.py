with open("C:/Users/Théo/Documents/Python Scripts/hamza.txt","r") as f:
    lines=f.readlines()
    #on tue la ligne 0
    lines[0]=""
    #on va tuer la ligne 1 et la ligne 4 de chaque carré de la matrice
    nombre_lignes=len(lines)
    nombre_cases_matrice=int(nombre_lignes/4)
    #on remplace les lignes de décorration
    for k in range(nombre_cases_matrice):
        lines[k*4+1]=""
        lines[k*4+4]=""
    #on prépare la suppression des lignes inutiles
    nombre_lignes_a_supprimer=lines.count('')
    print(nombre_lignes_a_supprimer)
    
    #suppression des lignes non-utiles
    for k in range(int(nombre_lignes_a_supprimer)):
        lines.remove('')

    lines_splittées=[]
    #séparation des lignes pour élimination des caractères non-pertinents
    for k in lines:
        lines_splittées.append(k.split())

    #on va retirer les ":" et les "|"    
    #pour ça, on va d'abord les compter
    nombre_char_a_suppr=lines_splittées[0].count('|')
    nombre_char_a_suppr2=lines_splittées[0].count(':')

    #pour chaque ligne
    for j in range(16):
        #on dégage les "|"
        for k in range(int(nombre_char_a_suppr)):
            lines_splittées[j].remove('|')
        #on dégage les ":""
        for i in range(int(nombre_char_a_suppr2)):
            lines_splittées[j].remove(':')

    #on va préparer les cases de la liste
    sorted_array=[[]for k in range(64)]
    #pour faire passer aux lignes suivantes de la matrice
    numero_ligne=0
    for k,l in enumerate(lines_splittées):
        numero_colonne=0
        for j in range(int(len(l)/2)):
            #on récupère les deux infos
            sorted_array[numero_ligne*8+numero_colonne].append(l[2*j])
            sorted_array[numero_ligne*8+numero_colonne].append(l[2*j+1])
            numero_colonne+=1
        #on n'incrémente le compteur de ligne de la matrice qu'une ligne sur deux
        numero_ligne+=k%2

    print(sorted_array)