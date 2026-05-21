from scipy import stats
import numpy as np
import matplotlib.pyplot as plt


# Generamos datos de Prueba
x = np.linspace(0, 50, 100)
y = 3*x + 10*np.random.rand(len(x))+5

# Hacemos una regresión lineal
slope, intercept, r_value, p_value, std_err = stats.linregress(x,y)
# slope : es la pendiente
# std_err : es el error en la pendiente
# intecrept: es la ordenada al origen


plt.figure(2)
plt.clf()
plt.plot(x, y, 'o', label='Medición')
plt.plot(x, slope*x + intercept, label='Ajuste')
plt.legend()
