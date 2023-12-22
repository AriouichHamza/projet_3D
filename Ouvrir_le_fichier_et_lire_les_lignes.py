#Ouvrir le fichier et lire les lignes
with open('teraterm2.txt', 'r') as file:
    lines = file.readlines()

# Initialiser des listes pour stocker les données
data = []

# Indicateur pour déterminer si nous sommes à l'intérieur d'un tableau
inside_table = False

# Parcourir les lignes
for line in lines:
    if '-----------------' in line:
        # Lorsque nous trouvons une ligne de séparation, cela signifie que nous entrons ou sortons d'un tableau
        inside_table = not inside_table
    elif inside_table and '|' in line:
        # Si nous sommes à l'intérieur d'un tableau et que la ligne contient des barres verticales, alors nous extrayons les données
        values = line.strip().split('|')
        data.append(values)

# Créer un DataFrame à partir des données
df = pd.DataFrame(data)

# Afficher le DataFrame
print(df.iloc[0:])