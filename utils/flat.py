def flatten_ejercicio1(listOfLists):
    resultado = []
    for lista in listOfLists:
        if isinstance(lista, list):
            resultado += flatten_ejercicio1(lista)
        else:
            resultado.append(lista)

    return resultado