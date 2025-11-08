import csv
import os

nombre_archivo = "paises.csv" # Nombre del archivo CSV para gestionar los datos

# Validaciones

def es_entero_positivo(valor_str):
    """Verifica si una cadena puede ser un entero positivo (> 0)
 y en caso afirmativo retorna el valor como entero; si no, retorna False para ser evaluado en la llamada."""
       
    if not valor_str.isdigit():
        return False
    
    valor = int(valor_str)
    
    if valor <= 0:
        return False
        
    return valor


def validar_entero(dato):
    """Solicita al usuario y valida un entero positivo."""

    while True:
        valor_str = input(f"Ingrese un Entero Positivo para {dato}").strip()
        
        if not valor_str:
            print(" Este campo no puede estar vacío.")
            continue
            
        valor = es_entero_positivo(valor_str)
        
        if valor is False:
            print(" Debe ingresar un número entero positivo.")
            continue
            
        return valor
    

def validar_entero_desde_archivo(valor_str):
    """Función auxiliar para validar las cantidades leídas en el archivo."""
    valor = es_entero_positivo(valor_str)

    if valor is False:
            return None
    else:        
        return valor
    

def mostrar_paises(paises):
    """Función para imprimir una lista de países con formato."""
    if not paises:
        print("La lista de países a mostrar está vacía.")
        return
            
    print("-" * 75)
    print(f"{'Nombre':<20}{'Población':<18}{'Superficie (km²)':<20}{'Continente'}")
    print("-" * 75)
    for p in paises:
        # Formato de números con separador de miles
        poblacion_str = f"{p['poblacion']:,}".replace(",", ".")
        superficie_str = f"{p['superficie']:,}".replace(",", ".")
                
        print(f"{p['nombre']:<20}{poblacion_str:<18}{superficie_str:<20}{p['continente']}")
    print("-" * 75)



# Generador de la lista_paises desde el archivo.

def cargar_datos_csv(nombre_archivo):
    
    """Carga datos de países. Si el archivo no existe, lo crea con el encabezado."""
    lista_paises = []
    registros_ignorados = 0
    claves_encabezado = ['nombre', 'poblacion', 'superficie', 'continente']

    # Si no existe el archivo genera uno con los nombres de encabezado de la lista claves_encabezado.

    if not os.path.exists(nombre_archivo):
        print(f" El archivo '{nombre_archivo}' no fue encontrado. Se genera uno vacío con encabezado.")
        
        with open(nombre_archivo, mode='w', encoding='utf-8', newline='') as archivo:
            escritor_csv = csv.writer(archivo)
            escritor_csv.writerow(claves_encabezado)
        print(" Archivo creado exitosamente. Continuando la ejecución con lista vacía.")
        return []

    # Si existe el archivo realiza la carga
    
    with open(nombre_archivo, 'r', encoding='utf-8') as archivo:
        lector_csv = csv.DictReader(archivo)
        
        for fila in lector_csv:
            falta_clave = False
            for k in claves_encabezado:
                if k not in fila:
                    falta_clave = True
                    break  
                # si encuentra una clave que falta actualiza el contador de registros ignorados y salta de fila
            
            if falta_clave:
                registros_ignorados += 1
                continue
                
            nombre = fila.get("nombre", "").strip().title()
            continente = fila.get("continente", "").strip().title() 
            poblacion = validar_entero_desde_archivo(fila.get("poblacion", "")) 
            superficie = validar_entero_desde_archivo(fila.get("superficie", ""))
            
            if (poblacion is not None and superficie is not None and 
                nombre and continente): # Si se validaron correctamente las cantidades de población y superficie y existen nombre y continente
                                        # se genera el diccionario con el país y se agrega a la lista lista_paises. Si no, se actuliza el contador de ignorados.
                
                pais = {
                    "nombre": nombre,
                    "poblacion": poblacion,
                    "superficie": superficie,
                    "continente": continente
                }
                lista_paises.append(pais)
            else:
                registros_ignorados += 1 
                    
        print(f"\n Carga finalizada. {len(lista_paises)} países cargados correctamente.") # se informa la cantidad de países cargados a la lista_paises
        if registros_ignorados > 0:
            print(f"Advertencia: {registros_ignorados} registros ignorados (formato/datos incompletos).") # y se informan los registros ignorados si los hay.
            
    return lista_paises


def guardar_datos_csv(nombre_archivo, lista_paises):
    """Guarda la lista completa de países en el archivo CSV, sobrescribiendo el contenido."""

    claves_encabezado = ['nombre', 'poblacion', 'superficie', 'continente']
    
    with open(nombre_archivo, 'w', encoding='utf-8', newline='') as archivo:
        escritor_csv = csv.DictWriter(archivo, fieldnames=claves_encabezado)
        
        escritor_csv.writeheader()
        escritor_csv.writerows(lista_paises)
    
    print(f"\n Datos guardados exitosamente en '{nombre_archivo}'.")



def agregar_pais(lista_paises, nombre_archivo):
    """Solicita datos de un nuevo país, valida y lo agrega, y luego guarda en el archivo."""
    print("\n AGREGAR NUEVO PAIS ")
        
    while True:
        nombre = input(" Nombre del País: ").strip().title()
        if not nombre:
            print("** El nombre del país no puede estar vacío. **")
            continue
        
        existe = False
        for pais in lista_paises:
            if pais['nombre'] == nombre:
                existe = True
                break
        
        if existe: 
            print(f"** El país '{nombre}' ya existe en la lista. **")
            continue
        break
            
    poblacion = validar_entero(" Población: ")
    superficie = validar_entero(" Superficie (km²): ")
    
    while True:
        continente = input(" Continente: ").strip().title()
        if not continente:
            print("** El continente no puede estar vacío. **")
            continue
        break
        
    nuevo_pais = {
        "nombre": nombre,
        "poblacion": poblacion,
        "superficie": superficie,
        "continente": continente
    }
        
    lista_paises.append(nuevo_pais)
    print(f"\n País '{nombre}' agregado correctamente.")
    
    guardar_datos_csv(nombre_archivo, lista_paises)



def actualizar_datos(lista_paises, nombre_archivo):
    """Actualiza Población y Superficie de un país existente y luego guarda la modificación en el archivo."""
    if not lista_paises:
        print("** No hay datos para actualizar. **")
        return
    print("\n ACTUALIZAR DATOS ")
    nombre_buscado = input(" Ingrese el nombre EXACTO del país: ").strip().title()
        
    indice_pais = -1 # si este valor no cambia significa que no se encontro el nombre de pais en la lista.

    for i, pais in enumerate(lista_paises):
        if pais["nombre"].upper() == nombre_buscado.upper():
            indice_pais = i # se encontró el nombre de país en la lista.
            break 
                
    if indice_pais == -1:
        print(f"** El país '{nombre_buscado}' no fue encontrado. **")
        return
            
    print(f"\n País encontrado: **{nombre_buscado}**.")
    
    cambio_realizado = False  # se fija este valor por defecto, si se actualizan población o superficie se cambia a True
        
    # Actualizar Población
    nueva_poblacion_str = input("Nueva Población (Enter para mantener): ").strip()
   
    if nueva_poblacion_str:
        nueva_poblacion = validar_entero_desde_archivo(nueva_poblacion_str)
        
        if nueva_poblacion:
            lista_paises[indice_pais]['poblacion'] = nueva_poblacion
            print(" Población actualizada.")
            cambio_realizado = True
        else:
            print(" Valor de población no válido. Se mantuvo el valor anterior.")
            
    # Actualizar Superficie
    nueva_superficie_str = input(" Nueva Superficie (km²) (Enter para mantener): ").strip()
    
    if nueva_superficie_str:
        nueva_superficie = validar_entero_desde_archivo(nueva_superficie_str)
        
        if nueva_superficie:
            lista_paises[indice_pais]['superficie'] = nueva_superficie
            print(" Superficie actualizada.")
            cambio_realizado = True
        else:
            print(" Valor de superficie no válido. Se mantuvo el valor anterior.")
            
    print(f"\n **Actualización de datos para {nombre_buscado} completada.**")

    if cambio_realizado: 
        guardar_datos_csv(nombre_archivo, lista_paises)
    else:
        print(" No se detectaron cambios válidos para guardar.")



def buscar_pais(lista_paises):
    """Busca países por nombre (coincidencia parcial o exacta)."""
    if not lista_paises:
        print("** La lista de países está vacía. **")
        return []
    nombre_buscado = input(" Ingrese el nombre (o parte del nombre) del país a buscar: ").strip().lower()
        
    if not nombre_buscado:
        print(" ** La cadena a buscar no puede estar vacía. **")
        return []
            
    resultados = []
        
    for pais in lista_paises:
        if nombre_buscado in pais["nombre"].lower():
            resultados.append(pais)
            
    if resultados:
        print(f"\n Se encontraron {len(resultados)} país(es) que coinciden:")
        mostrar_paises(resultados)
    else:
        print(f"\n Búsqueda sin resultados para '{nombre_buscado.title()}'.")
        
    return resultados


# Filtros

def ordenar_lista(lista): # Función auxiliar para filtrar
    """Ordena una lista  de elementos (cadenas/números)."""
    n = len(lista)

    for i in range(1, n):
        valor_actual = lista[i]
        j = i - 1
        # Mueve los elementos de lista[0..i-1] que son mayores que valor_actual
        # una posición adelante de su posición actual
        while j >= 0 and lista[j] > valor_actual:
            lista[j + 1] = lista[j]
            j -= 1
        lista[j + 1] = valor_actual

    return lista


def filtrar_por_continente(lista_paises):
    """Filtra la lista de países por el continente especificado."""
    continentes_set = set()
    for pais in lista_paises:
        continentes_set.add(pais['continente']) # se usa un set para obtener luego una lista de nombres únicos.
    

    continentes_disponibles = list(continentes_set)
    ordenar_lista(continentes_disponibles) # Uso de la función auxiliar
    

    print(f"Continentes disponibles: {', '.join(continentes_disponibles)}") # muestra por pantalla una lista de los continentes posibles.
    continente_buscado = input(" Ingrese el Continente a filtrar ( Debe conincidir con alguno de los Continentes disponibles ): ").strip().title()
        
    if not continente_buscado:
        print(" El nombre del continente no puede estar vacío.")
        return
        
    resultados_filtro = []
    for pais in lista_paises:
        if pais["continente"] == continente_buscado:
            resultados_filtro.append(pais)
    
    if resultados_filtro:
        print(f"\n Se encontraron {len(resultados_filtro)} país(es) en '{continente_buscado}':")
        mostrar_paises(resultados_filtro)      
    else:
        print(f"\n** Búsqueda sin resultados. No se encontraron países en el continente '{continente_buscado}'. **")



def filtrar_por_rango_poblacion(lista_paises):
    """Filtra la lista de países por un rango de población."""
    print(" FILTRAR POR RANGO DE POBLACION ")
    min_poblacion = validar_entero(" Población Mínima: ")
    
    while True:
        max_poblacion = validar_entero(" Población Máxima: ")
        if max_poblacion < min_poblacion:
            print(" El valor MAXIMO no puede ser menor que el MINIMO.")
        else:
            break
                
    resultados_filtro = []
    for pais in lista_paises:
        if min_poblacion <= pais["poblacion"] <= max_poblacion:
            resultados_filtro.append(pais)
    
    if resultados_filtro:
        print(f"\n Se encontraron {len(resultados_filtro)} país(es) en el rango:")
        mostrar_paises(resultados_filtro)      
    else:
        print("\n** Búsqueda sin resultados para el rango de población especificado. **")

def filtrar_por_rango_superficie(lista_paises):
    """Filtra la lista de países por un rango de superficie."""
    print(" FILTRAR POR RANGO DE SUPERFICIE ")
    min_superficie = validar_entero(" Superficie Mínima (km²): ")
    
    while True:
        max_superficie = validar_entero(" Superficie Máxima (km²): ")
        if max_superficie < min_superficie:
            print(" El valor Máximo no puede ser menor que el Mínimo.")
        else:
            break
                
    resultados_filtro = []
    for pais in lista_paises:
        if min_superficie <= pais["superficie"] <= max_superficie:
            resultados_filtro.append(pais)
    
    if resultados_filtro:
        print(f"\n Se encontraron {len(resultados_filtro)} país(es) en el rango:")
        mostrar_paises(resultados_filtro)      
    else:
        print("\n** Búsqueda sin resultados para el rango de superficie especificado. **")


def menu_filtros(lista_paises):
    """Submenú para manejar las opciones de filtrado, usando match/case."""
    if not lista_paises: 
        print("** La lista de países está vacía. No se puede filtrar. **")
        return
        
    while True:
        print("\n SUBMENU DE FILTROS ")
        print("1. Filtrar por Continente")
        print("2. Filtrar por Rango de Población")
        print("3. Filtrar por Rango de Superficie")
        print("4. Volver al Menú Principal")
        opcion = input(" Seleccione una opción: ").strip()
                
        match opcion:
            case '1':
                filtrar_por_continente(lista_paises)
            case '2':
                filtrar_por_rango_poblacion(lista_paises)
            case '3':
                filtrar_por_rango_superficie(lista_paises)
            case '4':
                break
            case _:
                print(" Opción inválida. Intente nuevamente")


# Ordenamientos

def ordenar_paises(lista_paises, clave, opcion_orden):
    """ Ordena y muestra la lista de países  , recibiendo como parámetros : 
    la lista , la clave del campo a ordenar y si es ascendente o descendente (valor por defecto)"""

    n = len(lista_paises)  
    resultados_ordenados = lista_paises  # Se crea una copia para ordenar y no modificar la lista original
    
    for i in range(1, n):
        pais_actual = resultados_ordenados[i]
        valor_actual = pais_actual[clave] # se obtiene el valor de la clave solicitada en el llamado de la función ( población o superficie )
        j = i - 1
        
        # Mueve los países de resultados_ordenados que son mayores (o menores si es descendente) 
        # una posición adelante de su posición actual
        while j >= 0:
            valor_comparacion = resultados_ordenados[j][clave]
            
            debe_moverse = False
            
            if opcion_orden == 'd': # Descendente
                if valor_comparacion < valor_actual: 
                    debe_moverse = True
            else: # Ascendente
                if valor_comparacion > valor_actual: 
                    debe_moverse = True

            if debe_moverse:
                resultados_ordenados[j + 1] = resultados_ordenados[j]
                j -= 1
            else:
                break

        resultados_ordenados[j + 1] = pais_actual

    if opcion_orden == 'd':
        orden_str = "Descendente (Z-A / Mayor a Menor)" 
    else:
        orden_str = "Ascendente (A-Z / Menor a Mayor)"

    print(f"\n Países ordenados por '{clave.title()}' en orden '{orden_str}':")
    mostrar_paises(resultados_ordenados)


def opción_ordenamiento():
    """función para validad el orden ascendente o descendente."""
    while True: 
        opcion_orden = input(" ¿Orden Ascendente (A) o Descendente (D)?: ").strip().lower()              
        if opcion_orden == 'a' or opcion_orden == 'd':
            return opcion_orden
        else:
            print("** Opción de orden inválida. Use 'A' o 'D'. **")
            continue


def menu_ordenamiento(lista_paises):
    """Submenú para manejar las opciones de ordenamiento, usando match/case."""
    if not lista_paises: 
        print(" La lista de países está vacía. No se puede ordenar.")
        return
        
    while True:
        print("\n SUBMENU DE ORDENAMIENTO ")
        print("1. Nombre (A-Z / Z-A)")
        print("2. Población")
        print("3. Superficie")
        print("4. Volver al Menú Principal")
                
        opcion_criterio = input(" Ingrese una opción: ").strip()
        
        match opcion_criterio:
            case '1':
                opcion_orden = opción_ordenamiento()
                ordenar_paises(lista_paises, 'nombre', opcion_orden )
            case '2':
                opcion_orden = opción_ordenamiento()
                ordenar_paises(lista_paises, 'poblacion', opcion_orden )
            case '3':
                opcion_orden = opción_ordenamiento()
                ordenar_paises(lista_paises, 'superficie', opcion_orden )
            case '4':
                break
            case _:
                print("** Opción de criterio para Ordenamiento inválida. **")


# Estadísticas

def obtener_extremos_poblacion(lista_paises):
    """Identifica y muestra el país con la mayor y la menor población."""
    if not lista_paises: 
        print(" La lista de países está vacía. No se pueden calcular extremos.")
        return
        
    print("\n ESTADISTICAS: POBLACION MAX y MIN ")
    
    # Se inicializan ambos con el primer elemento de la lista
    pais_max_pob = lista_paises[0]
    pais_min_pob = lista_paises[0]
    
    # Se itera desde el segundo elemento
    for pais in lista_paises[1:]:
        if pais['poblacion'] > pais_max_pob['poblacion']:
            pais_max_pob = pais
        if pais['poblacion'] < pais_min_pob['poblacion']:
            pais_min_pob = pais
    
    # Formateo
    pob_max_str = f"{pais_max_pob['poblacion']:,}".replace(",", ".")
    pob_min_str = f"{pais_min_pob['poblacion']:,}".replace(",", ".")
        
    print(f" País con Mayor Población:  {pais_max_pob['nombre']} ({pob_max_str} hab.)")
    print(f" País con Menor Población:  {pais_min_pob['nombre']} ({pob_min_str} hab.)")


def calcular_promedio(lista_paises, clave):
    """Calcula el promedio de una clave numérica."""
    if not lista_paises:
        return None
        
    suma_total = 0
    for pais in lista_paises:
        suma_total += pais[clave]
    
    return suma_total / len(lista_paises)


def mostrar_promedio_poblacion(lista_paises):
    """Calcula y muestra el promedio de población con coma decimal."""
    if not lista_paises: 
        print(" La lista de países está vacía. No se pueden calcular promedios.")
        return
        
    print("\n ESTADISTICAS: PROMEDIOS ")
        
    promedio_pob = calcular_promedio(lista_paises, 'poblacion')
    if promedio_pob is not None:
        pob_str = f"{promedio_pob:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
        print(f" Promedio de Población: {pob_str} habitantes")
        

def mostrar_promedio_superficie(lista_paises):
    """Calcula y muestra el promedio de superficies con coma decimal."""
    if not lista_paises: 
        print(" La lista de países está vacía. No se pueden calcular promedios.")
        return
        
    print("\n ESTADISTICAS: PROMEDIOS ")

    promedio_sup = calcular_promedio(lista_paises, 'superficie')
    if promedio_sup is not None:
        sup_str = f"{promedio_sup:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
        print(f" Promedio de Superficie: {sup_str} km²")



def contar_por_continente(lista_paises):
    """Cuenta la cantidad de países por cada continente."""
    if not lista_paises: 
        print(" La lista de países está vacía. No se puede contar por continente.")
        return
        
    print("\n ESTADISTICAS: PAISES POR CONTINENTE ")
        
    conteo_continentes = {}
    for pais in lista_paises:
        continente = pais.get("continente")
        if continente: # actualiza el contador de paises por continente, si es el primero asume valor 0 y lo incrementa en 1.
            conteo_continentes[continente] = conteo_continentes.get(continente, 0) + 1
            
    if conteo_continentes:# título del informe.
        print(" Continente | Cant. de países")
        
        # Obtener los nombres de los continentes
        nombres_continentes = []
        for continente in conteo_continentes:
            nombres_continentes.append(continente) # Genera la lista de los continentes existentes.
        

        for continente in nombres_continentes: # itera sobre la lista de continentes toma la cantidad del dicc conteo_continentes
            cantidad = conteo_continentes[continente]
            print(f" {continente}  :  {cantidad} país(es)")
    else:
        print(" No se encontraron datos de continentes.")



def menu_estadisticas(lista_paises):
    """Submenú para manejar las opciones de estadísticas, usando match/case."""
    if not lista_paises: 
        print(" La lista de países está vacía. No se pueden mostrar estadísticas.")
        return
        
    while True:
        print("\n SUBMENU DE ESTADISTICAS ")
        print("1. País con Mayor y Menor Población")
        print("2. Promedio de Población")
        print("3. Promedio de Superficie")
        print("4. Cantidad de Países por Continente")
        print("5. Volver al Menú Principal")
        opcion = input(" Seleccione una opción: ").strip()
        
        match opcion:
            case '1':
                obtener_extremos_poblacion(lista_paises)
            case '2':
                mostrar_promedio_poblacion(lista_paises)
            case '3':
                mostrar_promedio_superficie(lista_paises)
            case '4':
                contar_por_continente(lista_paises)
            case '5':
                break
            case _:
                print(" Opción inválida. Intente nuevamente.")



# Menú Principal

# Carga de datos
print("\nIniciando la carga de datos desde 'paises.csv'...")
lista_paises = cargar_datos_csv(nombre_archivo)
    
# Menú principal
while True:
    print("\n" + "=" * 40)
    print("      Gestión de Datos de Países ")
    print("=" * 40)
    print("1. Agregar un País")
    print("2. Actualizar Población/Superficie")
    print("3. Buscar País por Nombre")
    print("4. Filtrar Países")
    print("5. Ordenar Países")
    print("6. Mostrar Estadísticas")
    print("7. Mostrar Todos los Países")
    print("8. Salir del Sistema")
    print("-" * 40)
            
    opcion = input(" Ingrese su opción: ").strip()
            
    # La lista 'lista_paises' se pasa como argumento

    match opcion:
        case '1':
            agregar_pais(lista_paises, nombre_archivo)
        case '2':
            actualizar_datos(lista_paises, nombre_archivo)
        case '3':
            buscar_pais(lista_paises)
        case '4':
            menu_filtros(lista_paises)
        case '5':
            menu_ordenamiento(lista_paises)
        case '6':
            menu_estadisticas(lista_paises)
        case '7':
            print("\n LISTA COMPLETA DE PAISES ")
            mostrar_paises(lista_paises)
        case '8':
            print("\n Guardando datos y saliendo del sistema...")
            guardar_datos_csv(nombre_archivo, lista_paises)
            print(" Gracias por usar: 'Gestión de Datos de Países'")
            break
        case _:
            print("Opción no válida. Intente nuevamente")