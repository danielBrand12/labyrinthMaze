#LABORATORIO #2 DE LÓGICA Y REPRESENTACIÓN II
#ELABORADO POR KEVIN CORREA REYES Y DANIEL BRAND TABORDA

import random                                                                       # HACEMOS USO DE LA LIBERÍA RANDOM PARA PODER GENERAR MOVIMIENTOS ALEATORIOS


laberinto = list()                                                                  # LISTA EN LA QUE VAMOS A GUARDAR EL LABERINTO EN FORMA DE STRING
lista_recorridos = list()                                                           # LISTA DONDE SE VAN A GUARDAR TODOS LOS RECORRIDOS DE INICIO A FIN QUE SE ENCUENTREN EN LABERINTO
lista_menor_recorridos = list()                                                     # LISTA DONDE SE VAN A GUARDAR LOS RECORRIDOS MÁS CORTOS

with open('laberinto', 'r') as file:                                                # ABRIMOS EL ARCHIVO DONDE SE GUARDA EL LABERINTO
    laberinto = [[letter[0] for letter in line.split(" ")] for line in file]        # LINEA DONDE SE GUARDA UNO POR UNO LOS ELEMENTOS DEL LABERINTO, EN CASO DE TENER LA MATRIZ SEPARADA POR "," CAMBIAR EL SPLIT

def encontrar_inicio():                                                             # MÉTODO QUE ENCUENTRA EL INICIO DEL LABERINTO MARCADO CON "i"
    for i in range(len(laberinto)):
        for j in range(len(laberinto[i])):
            if laberinto[i][j] is 'i':
                return i, j

def encontrar_final():                                                              # MÉTODO QUE SIRVE PARA ENCONTRAR EL FINAL DEL LABERINTO
    for i in range(len(laberinto)):
        for j in range(len(laberinto[i])):
            if laberinto[i][j] is 'f':
                return i, j

def contar_ceros():                                                                 # MÉTODO QUE CUENTA LA CANTIDAD DE CEROS QUE SE ENCUENTRAN EN EL LABERINTO
    cont = 0                                                                        # CON EL FIN DE DESIGNARLE UN FINAL AL MÉTODO PRINCIPAL
    for i in range(len(laberinto)):
        for j in range(len(laberinto[i])):
            if laberinto[i][j] is '0':
                cont = cont + 1
    return cont

def encontrar_salidas():
    pila = list()                                                                   # LISTA QUE VAMOS A USAR EN FORMA DE PILA PARA GUARDAR LOS DATOS DEL LABERINTO
    marca = laberinto                                                               # MATRIZ AUXILIAR CON LA QUE VAMOS A REALIZAR LAS COMPARACIONES DEL CAMINO
    movimiento = [(-1, 0), #ARRIBA                                                  # ARREGLO DE TUPLAS PARA EJECUTAR LOS MOVIMIENTOS DE LA PILA DENTRO DE LA MATRIZ (ARRIBA, DERECHA, IZQ, ABAJO)
                  (0, 1),  #DERECHA
                  (1, 0),  #ABAJO
                  (0, -1)] #IZQUIERDA
    pila.append(encontrar_inicio())                                                 # APILAMOS EL INICIO DEL LABERINTO
    cont_final = 0                                                                  # CONTADOR QUE SE UTILIZA PARA REVISAR SI NO SE ENCUENTRA NINGÚN CAMINO EN CIERTO NÚMERO DE RECORRIDOS
    final = 0
    while True:                                                                     # CICLO PRINCIPAL QUE SE EJECUTA HASTA QUE SE CUMPLA ALGUNA DE LAS CONDICIONES DE PARADA DESIGNADAS
        mov_aux = random.choice(movimiento)                                         # VARIABLE QUE USAMOS PARA ELEGIR UNA TUPLA RANDOM DE MOVIMIENTO Y OPERAR CON ESTE
        sig_row = pila[-1][0] + mov_aux[0]                                          # AL ÚLTIMO VALOR DE LA PILA ([-1]) EN LA POSICIÓN DE LA FILA ([0]) LE VAMOS A SUMAR EL VALOR DE FILA DEL MOV_AUX
        sig_col = pila[-1][1] + mov_aux[1]                                          # AL ÚLTIMO VALOR DE LA PILA ([-1]) EN LA POSICIÓN DE LA COLUMNA ([1]) LE VAMOS A SUMAR EL VALOR DE COLUMNA DEL MOV_AUX
        cont_final = cont_final + 1                                                 # AUMENTAMOS EL CONTADOR FINAL EN 1 QUE ES EL RECORRIDO QUE ESTÁ HACIENDO
        if cont_final == 5000:
            print("No hay salida del laberinto")
            break
        if laberinto[sig_row][sig_col] == '1':                                      # SI MOV_AUX CONDUCE A UN '1' VUELVE AL INICIO DEL WHILE
            continue
        elif laberinto[sig_row][sig_col] == '0' and marca[sig_row][sig_col] == '0':
            pila.append((sig_row, sig_col))
            marca[sig_row][sig_col] = '1'                                           # MARCA UNA POSICIÓN POR LA CUAL YA HEMOS PASADO
            cont = 0
            for mov in movimiento:                                                  # FOR EN EL CUAL REALIZAMOS LOS MOVIMIENTOS EN SENTIDO DEXTRÓGIRO
                sig_row1 = pila[-1][0] + mov[0]                                     # CON LA FINALIDAD DE REVISAR SI LA POSICIÓN EN LA QUE ESTAMOS ESTÁ RODEADA O NO DE '1'
                sig_col1 = pila[-1][1] + mov[1]
                if laberinto[sig_row1][sig_col1] == '1':
                    cont = cont + 1                                                 # SI CONT=4 SIGNIFICA QUE EN TODOS LOS SENTIDOS HAY UN '1' Y NO SE PUEDE MOVER
            if cont == 4:
                for i in range(len(pila) - 1):                                      # PROCEDEMOS A DESAPILAR HASTA EL PRIMER ELEMENTO DE LA PILA Y A DEVOLVER A MARCA A SU ESTADO INICIAL
                    i = pila.pop()
                    marca[i[0]][i[1]] = '0'
        if laberinto[sig_row][sig_col] == 'f':                                      # SI EN LOS PROCEDIMIENTOS ANTERIORES LLEGAMOS AL FINAL REESTABLECEMOS EL CONTADOR FINAL
            cont_final = 0
            final = final + 1                                                       # LE AUMENTAMOS 1 A FINAL CON EL FIN DE REVISAR SI HAY MÁS CAMINOS POSIBLES
            pila.append((sig_row, sig_col))
            if str(pila) not in lista_recorridos:                                   # SI EL RECORRIDO ENCONTRADO NO ESTÁ EN LA LISTA DE RECORRIDOS LO AGREGA A LA LISTA DE RECORRIDOS Y REESTABLECE EL VALOR DE FINAL
                lista_recorridos.append(str(pila))
                final = 0
            pila.pop()
        if final == contar_ceros()*8:                                               # SI SE HACE CIERTO NÚMERO DE RECORRIDOS SIN ENCONTRAR UN NUEVO CAMINO RETORNA LOS ENCONTRADOS HASTA EL MOMENTO
            break                                                                   # QUE POR EL ALTO VALOR DEL PUNTO DE PARADA ASEGURA POR PROBABILIDAD QUE SE ENCUENTREN TODOS LOS CAMINOS

def contar_comas_lista():                                                           # MÉTODO PARA CONTAR LAS ',' QUE CONTIENE CADA UNO DE LOS CAMINOS DE LA LSITA DE RECORRIDOS Y RETORNAR EL NÚMERO MENOR
    lista2 = list()
    for i in lista_recorridos:
        contador = str(i).count(",")
        lista2.append(contador)
    return min(lista2)

def contar_comas(cadena):                                                          # CUENTA EL NÚMERO DE ',' QUE HAY EN UNA CADENA INGRESADA
    return str(cadena).count(",")


encontrar_salidas()                                                                # LLAMADO AL MÉTODO PRINCIPAL
if lista_recorridos:                                                               # SI LA LISTA DE RECORRIDOS NO ESTÁ VACÍA PROCEDEMOS A MOSTRAR EL MENÚ DE OPCIONES
    for i in lista_recorridos:
        if contar_comas(i) == contar_comas_lista():
            lista_menor_recorridos.append(i)
    while True:
        print("Elija opcion")
        print("""
        1. Ver todas las opciones.
        2. Ver el o los caminos más cortos.
        3. Ver todos los caminos.
        """)
        des = int(input("Elección -> "))
        if des == 1:                                                                # CASO DE VER TODAS LAS OPCIONES Y ELEGIR ENTRE UNA DE ELLAS
            for i in range(len(lista_recorridos)):
                print("Opción ->", i+1)
            des = int(input("Elección -> "))
            print(lista_recorridos[des-1])
        elif des == 2:                                                              # CASO DE VER EL O LOS CAMINOS MÁS CORTOS
            if len(lista_menor_recorridos) == 1:
                print("El camino más corto es:")
                print(lista_menor_recorridos)
            else:
                print("Qué camino desea ver?")
                for i in range(len(lista_menor_recorridos)):
                    print("Opción ->", i + 1)
                des = int(input("Elección -> "))
                print(lista_recorridos[des - 1])
        elif des == 3:                                                              # CASO DE VER TODOS LOS CAMINOS
           for i in lista_recorridos:
               print(i)
        else:
            print("Ingreso incorrecto.")
        print("""
        Para continuar digite 1, de lo contrario 0
        """)
        var = str(input("Elección ->"))
        if var is '0': break
else:
    print("Pruebe con otro laberinto.")






