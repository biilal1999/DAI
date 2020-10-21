def criba(lista, n):

    i = 0
    while(lista[i]*lista[i] <= n):
        for num in lista:
            if num <= lista[i]:
                continue
            elif num % lista[i] == 0:
                lista.remove(num)
            else:
                pass
        i += 1

    print (lista)


