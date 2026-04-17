import time
import functools

def timer(func):
    @functools.wraps(func)
    def wrapper(*args):
        inicio = time.perf_counter()
        print(f"Este es el valor del time inicio {inicio}"  )
        resultado = func(*args)
        fin = time.perf_counter()
        tiempo = fin - inicio
        print(f"Tiempo de ejecución de {func.__name__}: {tiempo:.6f} segundos")
        return resultado
    return wrapper

def memorize(func):
    cache = {}

    @functools.wraps(func)
    def wrapper(*args):
        # convertir args a algo hasheable porque las listas no lo son 
        key = str(args)

        if key not in cache:
            print(f"     [Calculado] {func.__name__} con input {args}")
            cache[key] = func(*args)
        else:
            print(f".    [Cache hit] {func.__name__} con input {args}")
        return cache[key]
    
    wrapper.cache = cache
    wrapper.clear_cache = lambda: cache.clear()

    return wrapper


def _flatten_ejercicio1(listOfLists):
    resultado = []
    for lista in listOfLists:
        if isinstance(lista, list):
            resultado += _flatten_ejercicio1(lista)
        else:
            resultado.append(lista)

    return resultado


@timer
@memorize
def flatten_ejercicio1(listOfLists):
    return _flatten_ejercicio1(listOfLists)


