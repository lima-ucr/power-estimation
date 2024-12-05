# Nombre de los archivos
SOURCE_FILES := power_grapho.py
SOURCE_FILES_2 := get_fanout_names.py
INPUT_FILES := library_pins.csv pipeline_8b_adder.v
OUTPUT_FILE := output.csv

# Reglas
.PHONY: all run-fanout run-power 
# Regla principal
all: run-fanout run-power

# Para ejecutar el programa en Linux
ifeq ($(shell uname),Linux)
run-fanout:
	@echo "Ejecuntado el calculo del FanOut del netlist..."
	python3 $(SOURCE_FILES_2) $(INPUT_FILES) $(OUTPUT_FILE)

run-power:	
	@echo "Ejecuntado la estimacion de la potencia dinamica..."
	python3 $(SOURCE_FILES)
endif

# Para ejecutar el programa en Windows
ifeq ($(OS),Windows_NT)
run-fanout:
	@echo "Ejecuntado el calculo del FanOut del netlist..."
	python $(SOURCE_FILES_2) $(INPUT_FILES) $(OUTPUT_FILE)

run-power:
	@echo "Ejecuntado la estimacion de la potencia dinamica..."
	python $(SOURCE_FILES)
endif

