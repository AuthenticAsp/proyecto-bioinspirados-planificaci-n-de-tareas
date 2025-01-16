import random
import numpy as np
import warnings
import matplotlib.pyplot as plt
from tabulate import tabulate
warnings.filterwarnings("ignore")

def generarPlanificacion():
    """s
    Genera una planificación de trabajos asignando aleatoriamente las operaciones a las máquinas disponibles.

    Returns:
        list: Una lista de tuplas que representa la planificación generada. Cada tupla contiene el nombre del trabajo y una lista de asignaciones 
        de máquinas para cada operación del trabajo.
    """
    planificacion = []
    for trabajo, operaciones in trabajos.items():
        asignacionMaquinas = [random.choice(range(len(tiemposOperaciones[operacion]))) for operacion in operaciones]
        planificacion.append((trabajo, asignacionMaquinas))
    return planificacion

def evaluarPlanificacion(planificacion):
    tiemposMaquinas = [0] * 4 
    tiemposFinTrabajos = {trabajo: 0 for trabajo in trabajos.keys()} 
    tiemposTrabajos = [] 
    for trabajo, asignacionMaquinas in planificacion:
        tiempoInicioTrabajo = tiemposFinTrabajos[trabajo]
        for i, operacion in enumerate(trabajos[trabajo]):
            maquina = asignacionMaquinas[i]
            tiempoInicio = max(tiempoInicioTrabajo, tiemposMaquinas[maquina])
            tiempoFin = tiempoInicio + tiemposOperaciones[operacion][maquina]
            tiemposTrabajos.append((trabajo, operacion, maquina, tiempoInicio, tiempoFin))
            tiempoInicioTrabajo = tiempoFin
            tiemposMaquinas[maquina] = tiempoFin
        tiemposFinTrabajos[trabajo] = tiempoInicioTrabajo
    return max(tiemposMaquinas), tiemposTrabajos

def torneo(poblacion):
    """
    Selecciona individuos de la población mediante el método del torneo.
    Returns:
        list: Lista de los individuos con los tiempos más bajos.
    """
    mezcla = poblacion[:]
    random.shuffle(mezcla)
    seleccion = [(mezcla[i], mezcla[i+1]) for i in range(0, len(mezcla), 2)]
    ganadores = [min(pareja, key=lambda indv: evaluarPlanificacion(indv)[0]) for pareja in seleccion]
    return ganadores

def cruce(ganadores, tasaCruce):
    """
    Args:
        ganadores (list): Lista con todos los padres.
        tasaCruce (float): Porcentaje de cruza.

    Returns:
        list: Una lista que contiene todos los hijos generados.
    """
    offspring = []
    for padre1 in ganadores:
        if random.random() < tasaCruce:
            padre2 = random.choice(ganadores)
            punto = random.randint(1, len(padre1)-2)
            hijo1 = padre1[:punto] + padre2[punto:]
            hijo2 = padre2[:punto] + padre1[punto:]
            offspring.append(hijo1)
            offspring.append(hijo2)
    return offspring

def mutacion(offspring, tasaMutacion):
    """
    Args:
        offspring (list): Una lista con los hijos generados.

    Returns:
        None
    """
    for planificacion in offspring:
        if random.random() < tasaMutacion:
            trabajo, asignacionMaquinas = random.choice(planificacion)
            indice = random.randint(0, len(asignacionMaquinas)-1)
            asignacionMaquinas[indice] = random.choice(range(len(tiemposOperaciones[trabajos[trabajo][indice]])))

def graficar(mejores, peores):
    plt.figure(figsize=(13,5))
    plt.plot(range(len(mejores)), mejores, color='blue', label='Mejor')
    plt.plot(range(len(peores)), peores, color='green', label='Peor')
    plt.title('Gráfica de convergencia')
    plt.xlabel('Iteraciones')
    plt.ylabel('Fitness')
    plt.legend()
    plt.show()

def graficarCronograma(tiemposTrabajos):
    """
    Genera un gráfico de barras horizontal que muestra el cronograma de ejecución de los trabajos en diferentes máquinas.

    Args:
        tiemposTrabajos (list): Una lista de tuplas que contienen información sobre cada trabajo, operación, máquina, inicio y fin.

    Returns:
        None
    """
    # Determinar el número de máquinas en base al primer elemento de tiemposOperaciones
    numero_maquinas = len(next(iter(tiemposOperaciones.values())))
    etiquetas_maquinas = [f'M{i}' for i in range(numero_maquinas)]

    # Obtener una lista de colores
    colores = plt.cm.get_cmap('tab20', len(trabajos))

    fig, ax = plt.subplots(figsize=(10, 6))

    for trabajo, operacion, maquina, inicio, fin in tiemposTrabajos:
        color = colores(list(trabajos.keys()).index(trabajo))
        ax.barh(maquina, fin - inicio, left=inicio, color=color, edgecolor='black', label=trabajo)

    ax.set_xlabel('Tiempo')
    ax.set_ylabel('Máquina')
    ax.set_yticks(range(numero_maquinas))
    ax.set_yticklabels(etiquetas_maquinas)

    # Manejo de leyendas
    handles, labels = ax.get_legend_handles_labels()
    porEtiqueta = dict(zip(labels, handles))
    ax.legend(porEtiqueta.values(), porEtiqueta.keys())

    plt.title('Cronograma de ejecución de los trabajos')
    plt.show()
    
def algoritmoGenetico(tamPoblacion, generaciones, tasaMutacion, tasaCruce):
    """
    Implementa el algoritmo genético para la planificación de tareas secuencial.
    
    Args:
        tamPoblacion (int): El tamaño de la población de individuos.
        generaciones (int): El número de generaciones a evolucionar.
        tasaMutacion (float): La probabilidad de mutación de un individuo.
        tasaCruce (float): La probabilidad de cruce entre dos individuos.
    
    Returns:
        tuple: Una tupla que contiene la mejor planificación encontrada, el puntaje de la mejor planificación y los tiempos de los trabajos.
    """
    poblacion = [generarPlanificacion() for _ in range(tamPoblacion)]
    #---------------Datos para gráfica de convergencia------------#
    bestAptitude = []
    worstAptitude = []    
    
    #---------------Algoritmo Genético-----------------#
    for _ in range(generaciones):
        #------------Seleccion por torneo----------------#
        ganadores = torneo(poblacion)
        
        #------------Cruza----------------#
        offspring = cruce(ganadores, tasaCruce)
        
        #------------Mutación de los hijos----------------#
        mutacion(offspring, tasaMutacion)
        
        #------------Seleccion de la nueva generación (n mejores)----------------#
        todos = poblacion + offspring
        todos.sort(key = lambda indv: evaluarPlanificacion(indv)[0])
        poblacion = todos[:tamPoblacion]
        #------------Seleccion de la nueva generación (n mejores)----------------#
        
        #-------------Datos para gráfica de convergencia------------#
        mejor = poblacion[0]
        peor = poblacion[-1]
        mejorPuntaje, tiemposTrabajos = evaluarPlanificacion(mejor)
        bestAptitude.append(mejorPuntaje)
        worstAptitude.append(evaluarPlanificacion(peor)[0])

    #-------------Gráficas------------#
    graficar(bestAptitude, worstAptitude)
    graficarCronograma(tiemposTrabajos)
    #-------------Gráficas------------#
    
    #----------------------------Crear la tabla de reporte-----------------------------#
    tablaReporte = []
    for trabajo, operacion, maquina, inicio, fin in tiemposTrabajos:
        tiempo = fin - inicio
        tablaReporte.append([f'M{maquina}', f'{trabajo}/{operacion}', inicio, fin, tiempo])
    print(tabulate(tablaReporte, headers=['Máquina', 'Trabajos/Operaciones', 'Tiempo Inicial', 'Tiempo Final', 'Tiempo Total'], tablefmt='grid'))
    #----------------------------Crear la tabla de reporte------------------------------#
    
    #-------------Imprimir datos en consola------------#
    promedio = sum(bestAptitude)/ len(bestAptitude)
    standar = np.std(bestAptitude, ddof=1)
    print("Mejor planificación:", mejor)
    print("Makespan:", mejorPuntaje)
    print(f'Promedio chingon: {promedio}')
    print(f'Desviacion: {standar}')
    #-------------Imprimir datos en consola------------#

tiemposOperaciones = {
    'O1': [3.5, 6.7, 2.5, 8.2],
    'O2': [5.5, 4.2, 7.6, 9.0],
    'O3': [6.1, 7.3, 5.5, 6.7],
    'O4': [4.8, 5.3, 3.8, 4.7],
    'O5': [3.8, 3.4, 4.2, 3.6]
}

trabajos = {
    'j1': ['O2', 'O4', 'O5'],
    'j2': ['O1', 'O3', 'O5'],
    'j3': ['O1', 'O2', 'O3', 'O4', 'O5'],
    'j4': ['O4', 'O5', 'O1', 'O3'],
    'j5': ['O2', 'O4', 'O1'],
    'j6': ['O1', 'O2', 'O4', 'O5']
}

random.seed(123)
algoritmoGenetico(100, 200, 0.15, 0.8)

