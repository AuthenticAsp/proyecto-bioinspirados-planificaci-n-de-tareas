# Planificación de Tareas mediante el uso de Algoritmos Bioinspirados

[![Video de presentación](https://img.youtube.com/vi/NVlVY9CKNRs/0.jpg)](https://www.youtube.com/watch?v=NVlVY9CKNRs)

## Descripción

En este programa se aborda el problema de la planificación de tareas [<b>Job Scheduling Problem</b>] buscando minimizar lo más posible el tiempo de convergencia hacia soluciones subóptimas para el problema.
Se hace uso del algoritmo genético en el cual se cruza, muta y se seleccionan los individuos de manera elitista por medio de la selección por torneo; se verificó la efectividad del algoritmo propuesto por medio
de pruebas que garantizan la viabilidad y la validez estadística de los resultados.

## Integrantes

- **Cruz García Daniel** 
- **López López Rebeca** 
- **Pérez Nuñez Miguel Alejandro** 

## Tecnologías Utilizadas

- Lenguaje de programación: Python

## Instalación y Uso

Para instalar y ejecutar este proyecto en una máquina local, se siguen estos pasos:

1. Se clona el repositorio:
   ```bash
   git clone https://github.com/AuthenticAsp/proyecto-bioinspirados-planificaci-n-de-tareas

2. El lenguaje utilizado es python, este proyecto utiliza varias bibliotecas externas. Para instalar todas las dependencias necesarias, se ejecuta el siguiente comando:
   ```bash
   pip install numpy matplotlib tabulate
   
3. Una vez que se tengan las dependencias instaladas, se puede ejecutar el código y para cambiar los trabajos se necesitan modificar las siguientes líneas para cambiar los tiempos de operaciones o los trabajos asignados a las máquinas:
   ```python
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
