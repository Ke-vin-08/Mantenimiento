"""
Kevin David Ortega Q.
Sebastian Vélez Marulanda.
Inginería eléctrica UTP.
Análisis de confiabilidad en un SEP.
Enunciado :
Un sistema de transmisión está compuesto por 5 líneas (L1 a L5) con tasa de fallos en las líneas L1
y L3 de 0.003 fallas/año y en las demás de 0.001 fallas/año. ¿En cuál de los tres barrajes sería
conveniente ubicar el generador G1 para llevar energía a la línea de distribución LP1 con mayor
confiabilidad?
"""
from typing import List, Union, Any

import matplotlib.pyplot as plt
import numpy as np
import math as mt
import pandas as pd

# Tasa de fallos.

L1 = 0.003  # Fallas/año
L3 = 0.003  # Fallas/año
L2 = 0.001  # Fallas/año
L4 = 0.001  # Fallas/año
L5 = 0.001  # Fallas/año


# Para el sistema 1, original.
# Método de descomposición
def sisO():
    Rdes = (1 - (1 - RL1) * (1 - RL4)) * (1 - (RL2) * (1 - RL3)) * RL5 + (1 - (1 - RL1 * RL2) * (1 - RL4 * RL3)) * (
                1 - RL5)
    return Rdes


def conf_serie(R1, R2):
    return R1 * R2


def conf_paralelo(R1, R2):
    return 1 - (1 - R1) * (1 - R2)


# ******************************************
def sis1():
    equi1 = conf_serie(RL1, RL4)
    equi2 = conf_paralelo(equi1, RL5)
    equi3 = conf_serie(equi2, RL2)
    Rsp1 = conf_paralelo(equi3, RL3)
    return Rsp1


def sis2():
    equi12 = conf_serie(RL1, RL4)
    equi22 = conf_paralelo(equi12, RL5)
    equi33 = conf_serie(equi22, RL3)
    Rsp2 = conf_paralelo(equi33, RL2)
    return Rsp2


# La idea es graficar, por lo que puede ser necesario organizar en tomar valore añadiendo en listas
# Es decir podemos inicializar una lista vacía para el sistema 1

# Confiabilidad del sistema 1
Cdes = []
Crsp1 = []
Crsp2 = []
for t in range(0, 1000, 5):
    RL1 = mt.exp(-L1 * t)
    RL2 = mt.exp(-L2 * t)
    RL3 = mt.exp(-L3 * t)
    RL4 = mt.exp(-L4 * t)
    RL5 = mt.exp(-L5 * t)
    Cdes.append(sisO())
    Crsp1.append(sis1())
    Crsp2.append(sis2())
X = 'Confiabilidad del sistema original'
Y = 'Confiabiliadad del sistema con el generador en 2'
Z = 'Confiabiliadad del sistema con el generador en 3'

#df = pd.DataFrame(Cdes, Crsp1, columns= 'A B')
#columna_a = matriz['A'] # accedemos a la columna A
#columna_b = matriz['B'] # accedemos a la columna A
#columna_c = matriz['C'] # accedemos a la columa C
#print(df)
#print(f"{Cdes} {Crsp1} {Crsp2}".format(sisO(),sis1(),sis2()))
#print("Confiabiliad del sistema ubicando G en 2", '\n'.join(map(str, Crsp1)))
#print("Confiabiliad del sistema ubicando G en 3",'\n'.join(map(str, Crsp2)))
from tabulate import tabulate
CS0 = np.array([[Cdes ],
    [Crsp1],
       [Crsp2]]).T


print('Confiabilidad del sistema en instantes de tiempo',CS0)
# Plotes

x = np.linspace(0, 1000, 200).astype(int)
plt.plot(x, Cdes)
plt.plot(x, Crsp1)
plt.plot(x, Crsp2)
plt.legend(["N1", "N2", "N3"])
plt.title("Confiabilidad vs tiempo")
plt.xlabel("Tiempo")
plt.ylabel("Confiabilidad del sistema")
plt.grid()
plt.savefig("Confiabilidadvstiempoc.pdf")
plt.show()

# Análisis de porcentajes.

plt.hist(Cdes, bins=15, edgecolor='black')
plt.hist(Crsp1,bins=15, edgecolor='black')
plt.hist(Crsp2,bins=15, edgecolor='black')
plt.legend(["N1", "N2", "N3"])
plt.title('Histograma de confiabilidad')
plt.xlabel("Confiabilidad")
plt.ylabel("Iteraciones")
plt.savefig("Histogramac.pdf")
plt.show()
