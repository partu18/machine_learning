from tree_aa_alumnos import *
import pylab

# Armamos dataset tennis 
X=np.array([["Sol","Calor","Alta","Debil"],
["Sol","Calor","Alta","Fuerte"],
["Nublado","Calor","Alta","Debil"],
["Lluvia","Templado","Alta","Debil"],
["Lluvia","Frio","Normal","Debil"],
["Lluvia","Frio","Normal","Fuerte"],
["Nublado","Frio","Normal","Fuerte"]])

y=np.array('No No Si Si Si No Si'.split())
attrs_names=np.array('Cielo Temperatura Humedad Viento'.split())


# Creo un DecisionTree
dt= DecisionTree(information_gain)

# Entrenamos
dt.fit(X,y,attrs_names)

# Pruebo una prediccion arbitraria
# prediccion_ejemplo= dt.predict(np.array([["Lluvia","Frio","Normal","Fuerte"]]))
# prediccion_ejemplo= dt.predict(np.array([["Lluvia","Calor","Normal","Fuerte"]]))
# print 'Predigo',prediccion_ejemplo

xTest = np.array([["Sol","Templado","Alta","Debil"],
["Sol","Frio","Normal","Debil"],
["Lluvia","Templado","Normal","Debil"],
["Sol","Templado","Normal","Fuerte"],
["Nublado","Templado","Alta","Fuerte"],
["Nublado","Calor","Normal","Debil"],
["Lluvia","Templado","Alta","Fuerte"]])

result = np.array('No Si Si Si Si Si No'.split())

corrects = 0
for ind in xrange(len(xTest)):
	row = xTest[ind]
	prediction = dt.predict(np.array([row]))
	if prediction[0] == result[ind]:
		corrects += 1
	print corrects

print "Le pegue a este porcentaje que te voy a decir ahora: {}".format(float(corrects)/len(result))

# Ploteo el arbol para mirarlo
fig= dt.plot_graph()
pylab.show()

