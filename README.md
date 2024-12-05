

## Nombre de Proyecto: Desarrollo de algoritmos para estimación de factores de actividad y consumo de potencia dinámica para circuitos digitales utilizando técnicas basadas en grafos

### Autor: J. Antonio Franchi

## Requisitos del programa

<details><summary><b>Mostrar dependencias necesarias y como instalarlas</b></summary>
Para Debian/Ubuntu:

* git
    ```bash
    sudo apt install git
    ```
* make
    ```bash
    sudo apt install make
    ```
* Python 3
    ```bash
    sudo apt install python3
    ```
* PIP
    ```bash
    sudo apt install pip
    ```

* Pandas
    ```bash
    sudo pip install pandas
    ```
   
* NetworkX
    ```bash
     sudo pip install networkx
    ```

Para Windows:

El proceso de instalación es más complejo, se sugiera buscar ayuda en la Web, para ir instalando la dependencias.

</details>

## Uso
### Pasos 

<details><summary><b>Mostrar instrucciones</b></summary>

1. Clona el repositorio:
    ```bash
    git clone https://github.com/.....
    ```

2. Navega al directorio `src`:
    ```bash
    cd power_estimation/src
    ```

3. Navegar al directorio del netlist deseado: `full_adder` (para el Sumador de 1 bit) o `full_adder_pipeline` (para el Sumador con Pipeline de 8 bits)

4. Obtener el archivo de salida con el FanOut del Netlist:
    
    ```bash
    make run-fanout
    ```

5. Para calcular la potencia dinamica del Netlist:
    ```bash
    make run-power
    ```

6. Para correr el paso 4 y 5 en una sola instrucción:
    ```bash
    make all
    ```


---
