"""
@file power_grapho.py
@brief Herramienta para estimación de potencia dinámica en circuitos digitales VLSI
@details
    Este programa implementa un analizador de potencia dinámica para circuitos digitales
    utilizando un algoritmo basado en teoría de grafos. Procesa netlists en formato Verilog y 
    calcula factores de actividad y consumo de potencia.

@author B.Sc J. Antonio Franchi

@version 1.0

@copyright Copyright (c) 2024
@license MIT License

Dependencias:
- NetworkX para manejo de grafos
- Pandas para procesamiento de datos
- Matplotlib para visualización
- NumPy para cálculos numéricos


Input files:
- netlist.v: Archivo Verilog con la descripción del circuito
- output.csv: Archivo con información de fanout
- library_pins.csv: Archivo con información de capacitancias

Output files:
- resultados_potencia_dinamica.csv: Resultados del análisis de potencia
- resultados_potencia_dinamica_total.txt: Resultados del analisis de potencia dinamica total
"""

# import re
import pandas as pd
# import numpy as np
import networkx as nx

import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

# Importar de los otros modulos para el calculo de probabilidades y factores de actividad
from get_activity_factor import LogicGateActivity 
# Importar las funciones para el manejo de los datos de get_data.py
from get_data import *


def main():
    """
    @brief Funcion principal que ejecuta el cálculo de potencia dinámica.
    """

    """ 
    # Paso 1: Importar y preparar los datos
    """
    # Leer library_pins.csv
    library_pins_df = pd.read_csv('library_pins.csv')

    library_pins_df.columns = [col.strip() for col in library_pins_df.columns]

    # Crear un diccionario para buscar capacitancias por Cell Name/Pin
    cap_dict = library_pins_df.set_index('Cell Name/Pin')['Capacitance'].to_dict()

    # Guarda los valores de las direcciones de los pines de la capacitancias
    dir_dict = library_pins_df.set_index('Cell Name/Pin')['Direction'].to_dict()


    # Leer output.csv 
    netlist_data = read_output_fanout('output.csv')

    # Codigo para Debuggear
    # Imprimir los datos de la estructura de datos: netlist_data
    # print("\n ------ Debuggear: netlist_data  ---------")
    # for entry in netlist_data:
    #     # print(f"Wire_Name: {entry['Wire_Name']}")
    #     # print(f"Source: {entry['Source']}")
    #     # print(f"Sinks: {entry['Sinks']}")
    #     print(f"Wire_Name: {entry['Wire_Name']}, Source: {entry['Source']}, Sinks: {entry['Sinks']}")
    #     print('--------')


    # Parsear el netlist .v para obtener el mapeo de instancias a tipos de celdas
    instance_cell_mapping, instance_cell_base_mapping, instance_pin_mapping = parse_netlist_rtl('pipeline_8b_adder.v')

    # Imprimir para debuggear
    # print("\n ------ Debuggear:  instance_cell_mapping  ---------")
    # print(instance_cell_mapping)

    # Imprimir para debuggear
    # print("\n ------ Debuggear:  instance_pin_mapping  ---------")
    # print(instance_pin_mapping)

    """ 
     # Paso 2: Construir el grafo dirigido DAG (GAD: Grafo aciclico Dirigido)
    """
    # Se construey el Grafo DAG 
    G = nx.DiGraph()

    # Conjunto de elementos secuwancilaes para el grafo: flip flops
    flip_flop_cells = {
    'sky130_fd_sc_hd__dfxtp_2',
    'sky130_fd_sc_hd__dfxtp_1',
    'sky130_fd_sc_hd__dfxtp_4',
    'sky130_fd_sc_hd__dfxtp_'
    }

    # Agregar nodos y aristas basados en netlist_data
    for entry in netlist_data:
        wire_name = entry['Wire_Name']
        source = entry['Source']
        sinks = entry['Sinks']

        # Obtener informacion del source
        if source == 'PI':
            source_instance = None
            source_pin = None
            source_cell_type_full = 'PI'  # Primary Input
            source_cell_type_base = 'PI'
            # source_cell_type = 'PI'  # Primary Input
        else:
            if '/' in source:
                source_instance, source_pin = source.split('/')
            else:
                print(f"Advertencia: Source '{source}' no contiene '/'")
                continue  

            source_cell_type_full = instance_cell_mapping.get(source_instance, None)
            source_cell_type_base = instance_cell_base_mapping.get(source_instance, None)
            
            # source_cell_type = instance_cell_mapping.get(source_instance, None)
            
        # Determinar si el source es un flip-flop
        source_is_ff = source_cell_type_base in flip_flop_cells
        # source_is_ff = source_cell_type in flip_flop_cells

        # Construir Nodo source
        if source_is_ff:
            # Para flip-flop, usar el pin /Q como nodo source
            source_node = f"{source_instance}/Q"
        elif source_cell_type_base == 'PI':
            # Para entradas primarias, usar el wire_name como nodo
            source_node = wire_name
        else:
            # Para celdas combinacionales, usar el nombre de instancia
            source_node = source_instance

        if not G.has_node(source_node):
            G.add_node(source_node, cell_type_full=source_cell_type_full, cell_type_base=source_cell_type_base)
            # G.add_node(source_node, cell_type=source_cell_type)

        # Procesar sinks
        for sink in sinks:
            if sink == '':
                continue
            if '/' not in sink:
                print(f"Advertencia: Sink '{sink}' no contiene '/'")
                continue
            sink_instance, sink_pin = sink.split('/')
            sink_cell_type_full = instance_cell_mapping.get(sink_instance, None)
            sink_cell_type_base = instance_cell_base_mapping.get(sink_instance, None)
            #sink_cell_type = instance_cell_mapping.get(sink_instance, None)

            sink_is_ff = sink_cell_type_base in flip_flop_cells

            # Construir Nodos
            # Construir Nodo sink
            if sink_is_ff:
                # Para flip-flop, usar el pin /D como nodo sink
                sink_node = f"{sink_instance}/D"
            else:
                # Para celdas combinacionales, usar el nombre de instancia
                sink_node = sink_instance

            if not G.has_node(sink_node):
                # G.add_node(sink_node, cell_type=sink_cell_type)
                G.add_node(sink_node, cell_type_full=sink_cell_type_full, cell_type_base=sink_cell_type_base)

            # Construir Aristas
            # Agregar arista desde source_node a sink_node con información del sink_pin
            G.add_edge(source_node, sink_node, wire=wire_name, sink_pin=sink_pin)
        
    # Imprimir info del grafo para debuggear
    print("\n--- Informacion del Grafo ---")
    print(f"Numero de nodos: {G.number_of_nodes()}")
    print(f"Numero de aristas: {G.number_of_edges()}\n")
    
    """ 
    # Paso 2.2 (Opcional): Visualizar el grafo para tenerlo como herramienta de visual
    # Comentarios
    #     Tipos de Layouts para los grafos:
    # [ 'planar_layout', 'random_layout', 'shell_layout', 'fruchterman_reingold_layout', 'spectral_layout', 'kamada_kawai_layout', 'spring_layout', 'circular_layout']
    # Layouts posibles: fruchterman_reingold_layout, spring_layout
    # Sobre parametro k
    # Optimal distance between nodes. If None the distance is set to 1/sqrt(n) where n is 
    # the number of nodes. Increase this value to move nodes farther apart.
    # Si n = 107 -> k = 1/sqrt(107) = 0.0967

    @ url: https://networkx.org/documentation/stable/reference/generated/networkx.drawing.layout.spring_layout.html
    """
    plt.figure(figsize=(12, 8))
    pos = nx.spring_layout(G, k=0.5, iterations=50)
    node_colors = []

    for node in G.nodes():
        cell_type = G.nodes[node].get('cell_type_full', 'Unknown')
        if cell_type in flip_flop_cells:
            node_colors.append('red')  # Flip-flops en rojo
        elif cell_type == 'PI':
            node_colors.append('green')  # Entradas primarias en verde
        else:
            node_colors.append('skyblue')  # Compuertas combinacionales en azul claro

    
    nx.draw_networkx(G, pos, with_labels=True, node_color=node_colors, node_size=500, font_size=8)
    plt.title("Grafo construido")

    # Crear los elementos de la leyenda
    legend_elements = [
        Line2D([0], [0], marker='o', color='w', label='Flip Flops', markerfacecolor='red', markersize=10),
        Line2D([0], [0], marker='o', color='w', label='PI', markerfacecolor='green', markersize=10),
        Line2D([0], [0], marker='o', color='w', label='Celdas logicas', markerfacecolor='skyblue', markersize=10)
    ]

    # Agregar la leyenda al grafico
    plt.legend(handles=legend_elements, loc='lower right')

    # Para mostrar el grafo
    plt.show()  # Nota: Comentar esta linea para omitir ploteo

    plt.close()

    """
     # Paso 3: Realizar ordenamiento topologico
    """
    try:
        topo_order = list(nx.topological_sort(G))
        
        # Caso que se necesitara general todos los posibles ordenam. topolo. de los Nodos
        # topological_order = list(nx.all_topological_sorts(G))

        # Imprimir info  para debuggear
        print("\n--- Ordenamiento Topologico del Grafo---")
        print(topo_order)

        # Paso 3.2 (Opcional): Dibujar el grafo
        # Visualizar el grafo despues del ordenamiento topologico

        plt.figure(figsize=(12, 8))
        # Crear una posicion para cada nodo segun su orden topologico
        pos = {}
        for idx, node in enumerate(topo_order):
            pos[node] = (idx, 0)  # Posicion horizontal segun el orden, vertical fija
        # Lista para los colores de los nodos
        node_colors = []

        for node in G.nodes():
            cell_type = G.nodes[node].get('cell_type_full', 'Unknown')
            if cell_type in flip_flop_cells:
                node_colors.append('red')
            elif cell_type == 'PI':
                node_colors.append('green')
            else:
                node_colors.append('skyblue')
        
        nx.draw_networkx(G, pos, with_labels=True, node_color=node_colors, node_size=500, font_size=8)
        plt.title("Grafo despues del ordenamiento topologico")

        # Crear los elementos de la leyenda
        legend_elements = [
            Line2D([0], [0], marker='o', color='w', label='Flip Flops', markerfacecolor='red', markersize=10),
            Line2D([0], [0], marker='o', color='w', label='PI', markerfacecolor='green', markersize=10),
            Line2D([0], [0], marker='o', color='w', label='Celdas lógicas', markerfacecolor='skyblue', markersize=10)
        ]

        # Agregar la leyenda al grafico
        plt.legend(handles=legend_elements, loc='lower right')

        # Para mostrar el grafo
        plt.show()  # Nota: Comentar esta linea para omitir ploteo

        plt.close()


    # Manejo de Errores
    except nx.NetworkXUnfeasible:
        print("Error: No es posible realizar ordenamiento topologico. Hay ciclos en el grafo")

        # Deteccion de ciclos
        cycles = list(nx.simple_cycles(G))

        # Mostrar los ciclos encontrados
        print("Ciclos encontrados en el grafo en los Wire_name: ")
        counter_cycles = 0
        for i in cycles:
            print("-->".join(i))
            counter_cycles += 1
        print(f"Numero ciclos en el grafo: {counter_cycles}")
        return


    """ 
    #  # Paso 4: Calcular probabilidades de conmutacion y factores de actividad
    """
    
    # Asignar probabilidades de conmutacion a los nodos de entrada primaria
    for node in G.nodes():
        node_data = G.nodes[node]
        cell_type = node_data.get('cell_type_base')
        if cell_type == 'PI':
            # Asignar probabilidad de conmutacion y factor de actividad a entradas primarias PI
            G.nodes[node]['switching_probability'] = 0.5
            G.nodes[node]['activity_factor'] = 0.25  # alpha = p * (1 - p)

    # Calcular probabilidades de conmutacion y factores de actividad para los demas nodos siguiendo el orden topologico
    # 
    for node in topo_order:
        node_data = G.nodes[node]
        # Si ya tiene asignada la probabilidad, continuar
        if 'switching_probability' in node_data:
            continue
        cell_type_full = node_data.get('cell_type_full')
        cell_type_base = node_data.get('cell_type_base')
        # cell_type = node_data.get('cell_type')

        # Verificar que cell_type no sea None
        if cell_type_base is None:
        # if cell_type is None:
            print(f"Advertencia: Nodo {node} no tiene 'cell_type' definido.")
            continue
        
        if cell_type_base in flip_flop_cells:
        # if cell_type in flip_flop_cells:
            # Para flip-flops, la salida /Q tiene la probabilidad de conmutacion de la entrada /D
            # Obtener el nodo /D correspondiente
            d_node = node.replace('/Q', '/D')
            if G.has_node(d_node):
                d_node_data = G.nodes[d_node]
                # Obtener los predecesores del nodo /D
                predecessors = list(G.predecessors(d_node))
                if not predecessors:
                    # Si no hay predecesores, asignar probabilidad por defecto
                    p_d = 0.5
                else:
                    # Obtener la probabilidad de conmutacion de los predecesores
                    p_d_list = [G.nodes[pred].get('switching_probability', 0.5) for pred in predecessors]
                    # Promediar las probabilidades
                    p_d = sum(p_d_list) / len(p_d_list)
                # Asignar la probabilidad de conmutación al nodo /D
                G.nodes[d_node]['switching_probability'] = p_d
                G.nodes[d_node]['activity_factor'] = p_d * (1 - p_d)
                # Asignar la misma probabilidad al nodo /Q
                G.nodes[node]['switching_probability'] = p_d
                G.nodes[node]['activity_factor'] = p_d * (1 - p_d)
            else:
                # No se encontro el nodo /D, asignar probabilidad por defecto
                G.nodes[node]['switching_probability'] = 0.5
                G.nodes[node]['activity_factor'] = 0.25
        else:
            # Para celdas combinacionales
            # Obtener las probabilidades de los predecesores =
            incoming_edges = G.in_edges(node, data=True)
            # Las probabilidades de entrada de las celdas
            input_probs = {}

            for pred, _, edge_data in incoming_edges:
                pin_name = edge_data.get('sink_pin')
                pred_data = G.nodes[pred]
                p = pred_data.get('switching_probability', 0.5)
                input_probs[pin_name] = p

            # Imprimir para debuggear
            # print(f"\nNodo: {node}, input_probs: {input_probs}")

            # Crear una instancia de LogicGateActivity
            logic_gate = LogicGateActivity(
                gate_type = cell_type_base,
                input_probs = input_probs  # Mapear con los dicts las probabilidades de entrada según los pines de la compuerta
            )

            # Calcular la probabilidad de conmutacion y el factor de actividad
            p_y = logic_gate.calc_switching_probability()
            alpha_y = logic_gate.activity_factor()

            # Asignar al nodo
            G.nodes[node]['switching_probability'] = p_y
            G.nodes[node]['activity_factor'] = alpha_y

            # Imprimir info del grafo para debuggear
            print("\n ------ Probabilidad de Conmutacion y Factor de Actividad  ---------")
            print( f"Nodo: {node}")
            print( f"   Tipo de Celda:                  {cell_type_full}")
            print( f"   Probabilidad de Conmutacion:    {G.nodes[node]['switching_probability']}")
            print( f"   Factor de Actividad:            {G.nodes[node]['activity_factor']}")
            print( f"   Probabilidades de Entradas:     {input_probs}")
            # print(f"\nNodo: {node}, input_probs: {input_probs}")

 
    
    """ 
    # Paso 5: Calcular potencia dinamica para cada salida de celda
    """

    Vdd = 1.8  # Voltaje de alimentacion, de lib Sky130_fd_sc_hd usar 1.8 V ; otros valores a probar: 1 V, 1.8
    frequency = 100e6  # Frecuencia de 100 MHz, otros valores a probar: 66 MHz, 110 MHz

    # Para almacenar los resultados del calculo de potencia
    results = []

    # Recorremos todos los nodos del grafo
    for node in G.nodes():
        node_data = G.nodes[node]
        # Verificamos que el nodo tenga asignados 'cell_type' y 'activity_factor' antes de calcular la potencia
        if 'cell_type_full' in node_data and 'activity_factor' in node_data:
            instance_name = node
            
            cell_type_full = node_data['cell_type_full']
            cell_type_base = node_data['cell_type_base']

            # Imprimir para debuggear
            # print(f"------Paso #5-------: \nNode es {node}")

            alpha = node_data['activity_factor']

            # Para omitir los primary inputs en el calculo de la potencia
            if cell_type_base == 'PI':
                continue  # Omite calc Potencia para primary inputs

            # Obtener los pins de la instancia
            pins = instance_pin_mapping.get(instance_name, {})

            # Encontrar pins de salida
            output_pins = []
            for pin_name in pins:
                cell_pin_name = f"{cell_type_full}/{pin_name}"
                direction = dir_dict.get(cell_pin_name, None)
                if direction == 'output':
                    output_pins.append(pin_name)

            cell_pin_name = f"{cell_type_full}/{pin_name}"
            

            # Obtener la capacitancia desde el diccionario cap_dict
            # Si no se encuentra, usamos un valor por defecto pequeño: 1e-15 o 0
            capi_default_value = 0.001      # Equivale a 1e-15
            capi = cap_dict.get(cell_pin_name, capi_default_value)

            # Imprimir para debuggear
            # print("\n ------ Capacitancia para las celdas  ---------")
            # print(f"\nCapitancia en pF para {cell_type_full}: {capi}")

            """
            # Calcular la potencia dinamica usando la ecuacion P = alpha * C * Vdd^2 * f
            # Usando que la capacitancia es dada en pF = 1e-12 
            # @url: skywater-pdk.readthedocs.io/en/main/contents/libraries/foundry-provided.html
            """
            P_dyn = alpha * ((capi)*(1e-12)) * (Vdd * Vdd) * frequency


            # Guardar los resultados en una lista de diccionarios
            results.append({
                'Instance Name': instance_name,
                'Cell Type': cell_type_full,
                'Probabilidad de Conmutacion': node_data['switching_probability'],
                'Factor de Actividad': alpha,
                'Capacitancia (pF)': capi,
                'Potencia Dinamica (W)': P_dyn
            })

            # Imprimir info  para debuggear
            print("\n------ Potencia Dinamica por celda  ---------")
            print( f"Nodo (Instance Name):              {node} ")
            print( f"   Cell Type:                      {cell_type_full}")
            print( f"   Probabilidad de Conmutacion:    {node_data['switching_probability']}")
            print( f"   Factor de Actividad:            {alpha}")
            print( f"   Capacitancia (pF):              {capi}")
            print( f"   Potencia Dinamica (W):          {P_dyn}")

            # Imprimir para debuggear
            # print(f"Nodo: {node}, input_probs: {input_probs}")

        else:
            print(f"Advertencia:\nPara el tipo de celda {cell_type} no tiene 'activity_factor' definido.")
            continue

    # Guardar los resultados en un DataFrame
    results_df = pd.DataFrame(results)

    """ 
      # Paso 6: Calcular potencia dinamica total
    """

    # Calcular potencia dinamica total del netlist a travez de la propagacion en el grafo
    total_dynamic_power = results_df['Potencia Dinamica (W)'].sum()
   
    print("\n ------ Potencia dinamica total del Netlist  ---------")
    print(f"Potencia dinamica total: \n     {total_dynamic_power:.6e} W") # Mostrar en notacion cientifica

    # Guardar los resultados en un archivo CSV
    results_df.to_csv('resultados_potencia_dinamica_por_celda.csv', index=False)

    # Mostrar los celdas
    # Imprimir para debuggear
    print("\n ------ Potencia dinamica Resultados por Celda  ---------")
    
    # pd.set_option('display.float_format', '{:.6e}'.format) # Configurar el formato de visualizacion para todas las columnas para la columna especifica
     # Configurar el formato de visualizacion para la columna de Potencia Dinamica unicamente
    results_df['Potencia Dinamica (W)'] = results_df['Potencia Dinamica (W)'].apply('{:.6e}'.format)
    print(results_df.head(10))

    
   # Guardar resultados en archivo txt: Informe
    save_results_to_txt(
        netlist_file='pipeline_8b_adder.v',
        fanout_file='output.csv',
        total_dynamic_power=total_dynamic_power,
        results_df=results_df,
        output_file='resultados_potencia_dinamica_total.txt'
    )

if __name__ == "__main__":
    main()