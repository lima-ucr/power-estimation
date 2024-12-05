### Version 2.4 Depurada

import re
import pandas as pd
import sys

def main():
    """
    @brief Función principal que coordina la ejecución del script.
    """
    # Procesar argumentos de línea de comandos
    archivo_library_pins, archivo_NETLIST, ruta_guardar_fanout_csv = process_arguments()

    # Leer el archivo de pines de la biblioteca
    pin_table = read_pin_table(archivo_library_pins)

    # Parsear el netlist y construir el diccionario de netlist y el conjunto de entradas primarias
    netlist_dict, primary_inputs_set = parse_netlist(archivo_NETLIST, pin_table)

    # Escribir el archivo CSV de salida
    write_output_csv(netlist_dict, primary_inputs_set, ruta_guardar_fanout_csv)

def process_arguments():
    """
    @brief Procesa los argumentos de línea de comandos.
    @return Tuple con los archivos de pines, netlist y ruta de salida.
    """
    if len(sys.argv) != 4:
        print("Uso: get_fanout_names.py "
              "<leer_archivo_library_pins> <leer_archivo_NETLIST> "
              "<ruta_guardar_fanout_csv>")
        sys.exit(1)

    archivo_library_pins = sys.argv[1]
    archivo_NETLIST = sys.argv[2]
    ruta_guardar_fanout_csv = sys.argv[3]

    print("\t\t\t\tLeyendo pin_csv:", archivo_library_pins)
    print("\t\t\t\tLeyendo .v:", archivo_NETLIST)
    print("\t\t\t\tsalida fanout.csv:", ruta_guardar_fanout_csv)

    return archivo_library_pins, archivo_NETLIST, ruta_guardar_fanout_csv

def read_pin_table(file_path):
    """
    @brief Lee el archivo CSV de pines de la biblioteca.
    @param file_path Ruta al archivo CSV.
    @return DataFrame con la información de los pines.
    """
    return pd.read_csv(file_path, index_col=0, header=0)

def parse_netlist(netlist_file, pin_table):
    """
    @brief Parsea el archivo netlist y construye el diccionario de netlist y el conjunto de entradas primarias.
    @param netlist_file Ruta al archivo netlist en formato Verilog.
    @param pin_table DataFrame con información de los pines de la biblioteca.
    @return Tuple con netlist_dict y primary_inputs_set.
    """
    netlist_dict = {}
    primary_inputs_set = set()

    wire_regexp = (
        r"\s*(wire|input|output)\s+\[*([\d:]*)\]*\s*(\\*[\w.]+)*\[*(\d*)\]*\s*\[*(\d*)\]*\s*\;")
    start_instance_regexp = r"\s*(\w+)\s*(\w+)\s*\($"
    start_instance_w_pin_regexp = r"\s*(\w+)\s*(\w+)\s*\(.(\w+)\((.*)\)\,$"
    end_instance_regexp = r"\s*\)\;$"
    end_instance_w_pin_regexp = r"^\s*\.(\w+)\((.*)\)\)\;$"
    pin_regexp = r"\s*.(\w+)\((.*)\)"

    with open(netlist_file, "r") as netlist_fh:
        inside_cell_instance = False

        for line in netlist_fh:
            line = line.strip()

            # Procesar declaraciones de señales
            if re.match(wire_regexp, line):
                process_signal_declaration(line, netlist_dict, primary_inputs_set)
                continue

            # Procesar instancias de celdas
            if not inside_cell_instance:
                inside_cell_instance, current_cell_ref, current_cell_name = check_start_instance(
                    line, start_instance_regexp, start_instance_w_pin_regexp)
            else:
                inside_cell_instance = process_cell_instance(
                    line, netlist_dict, pin_table, current_cell_ref, current_cell_name,
                    end_instance_regexp, end_instance_w_pin_regexp, pin_regexp)

    return netlist_dict, primary_inputs_set

def process_signal_declaration(line, netlist_dict, primary_inputs_set):
    """
    @brief Procesa una línea de declaración de señal y actualiza el netlist_dict y primary_inputs_set.
    @param line Línea del netlist que declara una señal.
    @param netlist_dict Diccionario con la información de netlist.
    @param primary_inputs_set Conjunto de nombres de señales de entrada primaria.
    """
    wire_regexp = (
        r"\s*(wire|input|output)\s+\[*([\d:]*)\]*\s*(\\*[\w.]+)*\[*(\d*)\]*\s*\[*(\d*)\]*\s*\;")
    match_results = re.search(wire_regexp, line)
    wire_type = match_results.group(1)
    multibit_str = match_results.group(2)
    signal_name = match_results.group(3)
    signal_index = match_results.group(4)
    signal_index_2d = match_results.group(5)

    # Asignar "PI" como fuente si es una entrada primaria
    default_source = "PI" if wire_type == "input" else ""

    if wire_type == "input":
        primary_inputs_set.add(signal_name)

    # Manejo de señales multibit o con índices
    if multibit_str and not signal_index:
        index_end, index_start = multibit_str.split(":")
        for i in range(int(index_start), int(index_end)+1):
            signal_with_index = f"{signal_name}[{i}]"
            netlist_dict[signal_with_index] = [default_source, []]
    elif multibit_str and signal_index:
        index_end, index_start = multibit_str.split(":")
        for i in range(int(index_start), int(index_end)+1):
            signal_with_index = f"{signal_name}[{signal_index}][{i}]"
            netlist_dict[signal_with_index] = [default_source, []]
    elif signal_index and not signal_index_2d:
        signal_with_index = f"{signal_name}[{signal_index}]"
        netlist_dict[signal_with_index] = [default_source, []]
    elif signal_index and signal_index_2d:
        signal_with_index = f"{signal_name}[{signal_index}][{signal_index_2d}]"
        netlist_dict[signal_with_index] = [default_source, []]
    else:
        netlist_dict[signal_name] = [default_source, []]

def check_start_instance(line, start_instance_regexp, start_instance_w_pin_regexp):
    """
    @brief Verifica si la línea indica el inicio de una instancia de celda.
    @param line Línea actual del netlist.
    @return Tuple con inside_cell_instance (bool), current_cell_ref, current_cell_name.
    """
    match_results = re.match(start_instance_regexp, line)
    if match_results:
        inside_cell_instance = True
        current_cell_ref = match_results.group(1)
        current_cell_name = match_results.group(2)
        return inside_cell_instance, current_cell_ref, current_cell_name

    match_results = re.match(start_instance_w_pin_regexp, line)
    if match_results:
        inside_cell_instance = True
        current_cell_ref = match_results.group(1)
        current_cell_name = match_results.group(2)
        return inside_cell_instance, current_cell_ref, current_cell_name

    return False, None, None

def process_cell_instance(line, netlist_dict, pin_table, current_cell_ref, current_cell_name,
                          end_instance_regexp, end_instance_w_pin_regexp, pin_regexp):
    """
    @brief Procesa las líneas dentro de una instancia de celda.
    @param line Línea actual del netlist.
    @return inside_cell_instance Indica si aún estamos dentro de una instancia.
    """
    if re.match(end_instance_regexp, line):
        return False
    elif re.match(end_instance_w_pin_regexp, line):
        process_pin_connection(line, netlist_dict, pin_table, current_cell_ref, current_cell_name)
        return False
    else:
        if re.match(pin_regexp, line):
            process_pin_connection(line, netlist_dict, pin_table, current_cell_ref, current_cell_name)
        return True

def process_pin_connection(line, netlist_dict, pin_table, cell_ref, cell_name):
    """
    @brief Procesa la conexión de un pin dentro de una instancia.
    @param line Línea actual del netlist.
    """
    pin_regexp = r"\s*.(\w+)\((.*)\)"
    match_results = re.search(pin_regexp, line)
    pin_name = match_results.group(1)
    signal_name = match_results.group(2).strip().replace(" ", "")

    # Ignorar pines de alimentación
    if pin_name in {"VGND", "VNB", "VPWR", "VPB"}:
        return

    pin_key = f"{cell_ref}/{pin_name}"
    if pin_key not in pin_table.index:
        print(f"Advertencia: {pin_key} no encontrado en la tabla de pines.")
        return

    pin_direction = pin_table.loc[pin_key, " Direction"]

    # Inicializar la señal en netlist_dict si no existe
    if signal_name not in netlist_dict:
        netlist_dict[signal_name] = ["", []]

    if pin_direction == "output":
        # Evitar sobrescribir si la fuente es "PI"
        if netlist_dict[signal_name][0] == "PI":
            print(f"Advertencia: Se está intentando sobrescribir una señal de entrada PI en {signal_name}")
        elif not netlist_dict[signal_name][0]:
            netlist_dict[signal_name][0] = f"{cell_name}/{pin_name}"
    elif pin_direction == "input":
        # Evitar duplicados en sinks
        sink = f"{cell_name}/{pin_name}"
        if sink not in netlist_dict[signal_name][1]:
            netlist_dict[signal_name][1].append(sink)

def write_output_csv(netlist_dict, primary_inputs_set, output_file):
    """
    @brief Escribe el archivo CSV de salida con la información de fanout.
    @param netlist_dict Diccionario con la información de netlist.
    @param primary_inputs_set Conjunto de nombres de señales de entrada primaria.
    @param output_file Ruta del archivo CSV de salida.
    """
    with open(output_file, "w") as out_fh:
        out_fh.write("Wire_Name,Source,Sinks\n")
        for wire in netlist_dict:
            source = netlist_dict[wire][0]
            # Asignar "PI" como fuente si es una entrada primaria
            wire_base = wire.split('[')[0]
            if wire_base in primary_inputs_set:
                source = "PI"

            sink_list = netlist_dict[wire][1]
            # Eliminar duplicados en sinks
            sink_list = list(set(sink_list))

            out_str = f"{wire},{source},"
            out_str += ",".join(sink_list)
            out_str += "\n"
            out_fh.write(out_str)

if __name__ == "__main__":
    main()
