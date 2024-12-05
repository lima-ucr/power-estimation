import re
# import pandas as pd
# import numpy as np
# import networkx as nx

def parse_netlist_rtl(netlist_file):
    """
    @brief Parsea el netlist RTL y obtiene el mapeo de instancias a tipos de celdas.

    @param netlist_file Archivo de netlist en formato Verilog.

    @return Tupla con mappings de instancias a celdas y pines.
    """
    
    # Inicializacon de Diccionarios
    instance_cell_mapping = {}  # Para Cell Name + Drive Strength
    instance_cell_base_mapping = {}     # Para Cell Name unicamente
    instance_pin_mapping = {}
    
    # Reg Exp para detectar instancias de celdas
    # cell_instance_regex = r'^\s*(\S+)\s+(\S+)\s*\('
    cell_instance_regex = r'^\s*(?!(module|endmodule|input|output|wire|assign|always|initial|parameter)\b)(\w+)\s+(\w+)\s*\('

    # Reg Exp para detectar conexiones de pines
    pin_connection_regex = r'\.(\w+)\(([\w\[\]\\/]+)\)'

    # Keywords para excluir 
    keywords_exclude = {'module', 'endmodule', 'input', 'output', 'wire', 'assign', 'always', 'initial', 'parameter'} 

    # Abrir file con el netlist
    with open(netlist_file, 'r') as file:
        lines = file.readlines()
        i = 0   # Contador de la posicion actual a leerse

        while i < len(lines):
            line = lines[i]
            cell_match = re.match(cell_instance_regex, line)
            if cell_match:
                cell_type_full = cell_match.group(2)
                instance_name = cell_match.group(3)

                # Estandarizar el cell_type eliminando sufijos numericos del Drive Strength
                cell_type_base = re.sub(r'_\d+$', '', cell_type_full)
                
                cell_type = cell_type_full

                # Chequear que el tipo de celda no sea un keyword a excluir
                if cell_type in keywords_exclude:
                    i += 1  # Pasar siguiente posicion
                    continue

                # Inicializar diccionario para tipos de celdas full
                instance_cell_mapping[instance_name] = cell_type
                # Inicializar diccionario para tipos de celdas sin Drive Strength
                instance_cell_base_mapping[instance_name] = cell_type_base
                # Inicializar diccionario para Pines de la celda 
                instance_pin_mapping[instance_name] = {}

                # Leer conexiones de pines
                i += 1
                while i < len(lines):
                    line = lines[i].strip()     # Strip
                    if line.startswith(');'):
                        break
                    pin_matches = re.findall(pin_connection_regex, line)
                    for pin_name, signal_name in pin_matches:
                        instance_pin_mapping[instance_name][pin_name] = signal_name.strip()     # Se guarda en el dict
                    i += 1
            else:
                i += 1  # Pasar siguiente posicion
                
    return instance_cell_mapping, instance_cell_base_mapping, instance_pin_mapping


def read_output_fanout(file_path):
    """
    @brief Lee el archivo output.csv y extrae la información del netlist.

    @param file_path Ruta al archivo output.csv.

    @return Lista de diccionarios con 'Wire_Name', 'Source' y 'Sinks'.
    """
    netlist_data = []

    with open(file_path, 'r') as file:
        lines = file.readlines()

        # Saltar la linea con el encabezado
        start_idx = 0
        if lines[0].strip().startswith('Wire_Name'):
            start_idx = 1

        for line in lines[start_idx:]:
            line = line.strip()
            # Condiciones 
            # Saltar linea vacias
            if not line:
                continue  
            fields = line.split(',')
            if len(fields) < 2:
                continue  # Saltar linea que no tengan wire_name y source

            wire_name = fields[0].strip()
            source = fields[1].strip()
            sinks = [sink.strip() for sink in fields[2:] if sink.strip() != '']

            netlist_data.append({
                'Wire_Name': wire_name,
                'Source': source,
                'Sinks': sinks
            })

    return netlist_data


def save_results_to_txt(netlist_file, fanout_file, total_dynamic_power, results_df, output_file):
    """
    @brief Guarda los resultados del análisis de potencia en un archivo de texto para funcionar como informe.
    
    @param    netlist_file (str): Nombre del archivo netlist
    @param    fanout_file (str): Nombre del archivo fanout
    @param    total_dynamic_power (float): Potencia dinámica total calculada
    @param    results_df (pd.DataFrame): DataFrame con resultados por celda
    @param    output_file (str): Nombre del archivo de salida
    """

    with open(output_file, 'w') as f:
        f.write("------------------------------------ Informe de resultados ------------------------------------\n \n")
        f.write(f"netlist_file := {netlist_file}\n")
        f.write(f"fanout_file := {fanout_file}\n \n")
        f.write("--------- Potencia Dinamica total del Netlist (W) ---------\n")
        f.write(f"Potencia de Conmutacion Total := {total_dynamic_power:e}\n \n")
        f.write("------ Potencia dinamica Resultados por Celda  ---------\n\n")
        f.write(results_df.to_string())