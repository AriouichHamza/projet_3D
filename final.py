import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from scipy.interpolate import griddata
import math
import re
from re import X
from scipy.optimize import minimize



def lire():
    with open('hamza.txt', 'r') as file:
        lines = file.read()
        

        
    lines = lines.replace("|", ".")
    lines = lines.replace(":", ".")
    lines = lines.replace("53L5A1", "")

    lines = lines.replace("X", "0")

    lines = re.sub(r'[^0-9.]', '', lines)


    lines = lines.split('.')

    lines = [i for i in lines if i != '']   

    res=[eval(i) for i in lines]

    #print(res)

    n = len(res)//4

    data = np.zeros((n, 4), dtype = int)

    up = []
    down = []

    for i in range(len(res)):
        j = i%32
        if j >= 16:
            
            down.append(res[i])
        else:
            up.append(res[i])

    print(len(up)/64, len(down)/64)
    # assert len(up) == len(down) 
    #print(up)
    #print(down)

    for i in range(len(up)):
        
        if i%2 == 0:
            data[i//2, 0] = up[i]
            data[i//2, 2] = down[i]
        else:
            data[i//2, 1] = up[i]
            data[i//2, 3] = down[i]
        
    #print('resultat',data.reshape(-1,64,4))
    #print("mes resultat",data)
    return data
""""*****************************************************************************************"""
Data=lire()

#def Transformation_Matrice_1x64_A_Une_Matrice_8x8(Data):
n=len(Data)
print(n)
i=0
#Matrix8X8=np.empty((8, 8) , dtype=object)
myList=[]
# Maintenant, matrix_8x8 est une matrice 8x8 dont les éléments sont des matrices 1x4 remplies de zéros

while i < n-8:
    Matrix8X8=np.empty((8, 8) , dtype=object)
    for j in range(8):
        for k in range(8):
            #print(Data[i])
            Matrix8X8[j,k]= (Data[i]) 
            i=i+1  
            
    myList.append(Matrix8X8)
    #print ("*******************ma matrice" ,i/64, "********************\n", myList,"\n","*******************************\n")
    #print("la matrice\n", Matrix8X8)
    #print("la listeest ",int ((i-64)/64)) #,Matrix8X8[0][0][0])             
    #return myList          
#print("myliste est ",(myList))
#print("myliste est \n",(myList))
num_matrice=0
num_line=7
num_colon=7
#print("test",(myList[num_matrice][num_line][num_colon])[0])

print(myList)
"""*****************************************************************************************************"""


def chgt_coord1(mat):
    mat_x = [[0 for _ in range(8)] for _ in range(8)]
    mat_y = [[0 for _ in range(8)] for _ in range(8)]
    mat_z = [[0 for _ in range(8)] for _ in range(8)]

    # Angle de transformation (64 degrés divisé par 8, puis divisé par 2)
    
    angle = 37*(math.pi/180)

    # Décalage en déclinaison
    mat_dec = [-7/2, -5/2, -3/2, -1/2, 1/2, 3/2, 5/2, 7/2]

    for i in range(8):
        for j in range(8):
            # R est la valeur de la distance radiale dans le repère polaire
            R = mat[i][j][0]
            # Calcul des coordonnées cartésiennes
            B = math.sin(math.radians(-mat_dec[j] * angle))
            A = math.cos(math.radians(-mat_dec[j] * angle))
            C = math.sin(math.radians(mat_dec[i] * angle))
            D = math.cos(math.radians(mat_dec[i] * angle))

            mat_x[i][j] = R * A * D
            mat_y[i][j] = R * A * C
            mat_z[i][j] = R * B

    return [mat_x, mat_y, mat_z]

"""*****************************************************************************************************"""
def visualisation_3D(mat_xyz):
    # Créez une figure 3D
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    # Tracez les données en 3D
    ax.scatter(mat_xyz[0], mat_xyz[1], mat_xyz[2], c='r', marker='o')

    # Étiquetez les axes
    ax.set_xlabel('Axe X')
    ax.set_ylabel('Axe Y')
    ax.set_zlabel('Axe Z')

    # Affichez la figure
    plt.show()
"""*****************************************************************************************************"""
def visualisation_3Dprim(mat_xyz):
    # Créez une figure 3D
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    # Déterminez une grille de coordonnées pour le plan
    x = mat_xyz[0]
    y = mat_xyz[1]
    z = mat_xyz[2]

    # Créez une grille de coordonnées pour le plan
    x_grid, y_grid = np.meshgrid(x[0], y[0])

    # Utilisez l'interpolation pour obtenir les valeurs z du plan
    z_plane = griddata((x[0], y[0]), z[0], (x_grid, y_grid), method='cubic')

    # Tracez le plan en utilisant plot_surface
    ax.plot_surface(x_grid, y_grid, z_plane, alpha=0.05, rstride=10, cstride=10, cmap='viridis')

    # Tracez également les points
    ax.scatter(x, y, z, c='r', marker='o')

    # Étiquetez les axes
    ax.set_xlabel('Axe X')
    ax.set_ylabel('Axe Y')
    ax.set_zlabel('Axe Z')

    # Affichez la figure
    plt.show()
 
"""*****************************************************************************************************"""

# Vos données en coordonnées cartésiennes (x, y, z)
data = np.array(chgt_coord1(myList[0]))  # Remplacez ceci par vos propres données

# Modèle de plan : z = ax + by + c
def plane(params, data):
    a, b, c = params
    x, y, z = data
    return a * x + b * y + c

# Fonction d'erreur à minimiser
def error(params, data):
    return np.sum((plane(params, data) - data[0]) ** 2)

# Estimation des coefficients du plan
initial_guess = [0, 0, 0]  # Vous pouvez initialiser les valeurs ici
result = minimize(error, initial_guess, args=(data,), method='BFGS')
a, b, c = result.x

# Création du plan
x_range = np.linspace(np.min(data[0]), np.max(data[0]), 64)
print(len(x_range))
y_range = np.linspace(np.min(data[1]), np.max(data[1]), 64)
z_range=np.linspace(np.min(data[2]), np.max(data[2]), 64)
xx, yy = np.meshgrid(x_range, y_range)
#yy, zz = np.meshgrid(y_range, z_range)
#xx = a * yy + b * zz + c
zz = a * xx + b * yy + c-1000

# Tracé du plan et des points
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.plot_surface(xx, yy, zz, alpha=0.2, rstride=64, cstride=64, cmap='viridis')
ax.scatter(data[0], data[1], data[2], c='r', marker='o')

# Étiquetage des axes
ax.set_xlabel('Axe X')
ax.set_ylabel('Axe Y')
ax.set_zlabel('Axe Z')

plt.show()
"""*****************************************************************************************************"""
data = np.array(chgt_coord1(myList[0]))
# Modèle de plan : z = ax + by + c
def plane(params, data):
    a, b, c = params
    x, y, z = data
    return a * x + b * y + c

# Fonction d'erreur à minimiser
def error(params, data):
    return np.sum((plane(params, data) - data[2]) ** 2)

# Estimation des coefficients du plan
initial_guess = [0, 0, 0]  # Vous pouvez initialiser les valeurs ici
result = minimize(error, initial_guess, args=(data,), method='BFGS')
a, b, c = result.x


# Création du plan
x_range = np.linspace(np.min(data[0]), np.max(data[0]), 64)
y_range = np.linspace(np.min(data[1]), np.max(data[1]), 64)
xx, yy = np.meshgrid(x_range, y_range)
zz  = a * xx + b * yy + c 
print(f"Coefficient a : {a}")
print(f"Coefficient b : {b}")
print(f"Coefficient c : {c}")
# Tracé du plan et des points
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.plot_surface(xx, yy, zz, alpha=0.5, rstride=64, cstride=64, cmap='viridis')
ax.scatter(data[0], data[1], data[2], c='r', marker='o')

# Étiquetage des axes
ax.set_xlabel('Axe X')
ax.set_ylabel('Axe Y')
ax.set_zlabel('Axe Z')

plt.show()



