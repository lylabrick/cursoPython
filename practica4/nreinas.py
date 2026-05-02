def es_valido(estado, fila, col):
    """
    Verifica si colocar una reina en (fila, col) cumple con las restricciones 
    respecto a las reinas ya colocadas.
    """
    for f in range(fila):
        # Misma columna
        if estado[f] == col:
            return False
        # Misma diagonal (la diferencia entre filas es igual a la de columnas)
        if abs(estado[f] - col) == abs(f - fila):
            return False
    return True

def resolver_n_reinas(n, fila=0, estado=None):
    """
    Algoritmo de Backtracking puro para el problema de las N-Reinas.
    estado[i] guarda la columna de la reina en la fila i.
    """
    if estado is None:
        estado = [-1] * n

    # Caso base: Se han colocado todas las reinas exitosamente
    if fila == n:
        return [list(estado)]

    soluciones = []
    
    # Explorar el dominio de la variable actual (columna para la fila actual)
    for col in range(n):
        if es_valido(estado, fila, col):
            # Asignación (Hacer)
            estado[fila] = col
            
            # Llamada recursiva (Explorar)
            resultados = resolver_n_reinas(n, fila + 1, estado)
            soluciones.extend(resultados)
            
            # Backtrack (Deshacer asignación para probar la siguiente columna)
            estado[fila] = -1
            
    return soluciones

def imprimir_tablero(solucion):
    n = len(solucion)
    for col in solucion:
        fila_str = [" . "] * n
        fila_str[col] = " Q "
        print("".join(fila_str))
    print("\n" + "-" * (n * 3))

# Ejemplo de uso para N=4
N = 4
todas_las_soluciones = resolver_n_reinas(N)

print(f"Se encontraron {len(todas_las_soluciones)} soluciones para N={N}:\n")
for sol in todas_las_soluciones:
    imprimir_tablero(sol)