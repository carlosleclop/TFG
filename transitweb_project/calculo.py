

for i in range(0,100000000):
    correr = i%10
    numero = i/10
    cifras_str = str(numero)
    nuevo_numero = int(str(correr) + cifras_str) 
    if nuevo_numero == 2*i:
        print "encontrado: " + str(i)
