#######################################################
#       Comentario
# 
#
#       @note: del Weste-Harris:
#
#       Completely random data has P = 0.5 and thus alpha = 0.25. 
#       When paths contain reconvergent fanouts, signals become correlated and conditional 
#       probabilities become required. Power analysis tools are the most convenient way to handle 
#       large complex circuits.
#       Preliminary power estimation requires guessing an activity factor before RTL code is 
#       written and workloads are known. alpha = 0.1 is a reasonable choice in the absence of better data.
# 
#  
#######################################################


import re
import pandas as pd
import numpy as np
import networkx as nx

import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

class LogicGateActivity:
    """
    @class LogicGateActivity
    @brief Clase para calcular la actividad de compuertas logicas.

    @details Esta clase implementa los cálculos de probabilidad de conmutación y factores de actividad
    para diferentes (no completa) tipos de compuertas de la biblioteca sky130_fd_sc_hd.

    #TODO: La lib biblioteca sky130_fd_sc_hd no esta implementanda de forma completa, la lib completa consiste de 194 celdas
           actualmente se ha implementado
    """
    # Variables para valores por default
    DEFAULT_PI_PROB = 0.5
    DEFAULT_GATE_PROB = 0.1     # Se asume una probabilidad por defecto de 0.1 basado en el Weste-Harris


    def __init__(self, gate_type, input_probs):
        """
        @brief Constructor de la clase.

        @param gate_type str Tipo de compuerta logica.
        @param input_probs dict Diccionario con probabilidades de entrada
        @param p_b Probabilidad de conmutación de la entrada B.
        @param p_c Probabilidad de conmutación de la entrada C.
        @param p_d Probabilidad de conmutación de la entrada D.
        @param p_e Probabilidad de conmutación de la entrada E.
        """

        # Manejo de errores
        if not isinstance(input_probs, dict):
            raise ValueError("Error: input_probs debe ser un diccionario")
        
        for pin, prob in input_probs.items():
            if not isinstance(prob, (int, float)):
                raise ValueError(f"Error: Probabilidad invalida para pin {pin}: debe ser un numero")
            if not 0 <= prob <= 1:
                raise ValueError(f"Error: Probabilidad invalida para pin {pin}: {prob} (debe estar entre 0 y 1)")

        self.gate_type = gate_type
        self.input_probs = input_probs


    def calc_switching_probability(self):
        """
        @brief Calcula la probabilidad de conmutación de la salida de la compuerta lógica.

        @details
            Formato de los comentarios para los distintos tipo de celdas: 
            <Nombre_Celda>: <Funcion_Logica>
            A partir de la funcion logica se calcula la probabilidad de conmutacion
            pero no siempre es una relacion directa

        @return Probabilidad de conmutación de la salida.
        """

        """
        Celdas logicas combinacionales: Caso de FullAdder 1bit, FullAdder con pipeline 8 bits
        TODO: No esta completa para toda la libreria de SkyWater sky130_fd_sc_hd
        """

        # Primary Inputs
        if self.gate_type == "PI":
            return self.DEFAULT_PI_PROB
        
        # Celdas Lógicas 

        # Gates AND/NAND and with inverter ANDB
        # AND2: Y = A & B
        elif self.gate_type == "sky130_fd_sc_hd__and2":
            p_a = self.input_probs.get('A', 0)
            p_b = self.input_probs.get('B', 0)
            return p_a * p_b
        
        # AND3: Y = A & B & C
        elif self.gate_type == "sky130_fd_sc_hd__and3":
            p_a = self.input_probs.get('A', 0)
            p_b = self.input_probs.get('B', 0)
            p_c = self.input_probs.get('C', 0)
            return p_a * p_b * p_c
        
        # AND2B: Y = (!A_N) & B
        elif self.gate_type == "sky130_fd_sc_hd__and2b":
            p_a = self.input_probs.get('A_N', 0)
            p_b = self.input_probs.get('B', 0)
            return (1 - p_a) * p_b
        
        # AND3B: Y = (!A_N) & B & C
        elif self.gate_type == "sky130_fd_sc_hd__and3b":
            p_a = self.input_probs.get('A_N', 0)
            p_b = self.input_probs.get('B', 0)
            p_c = self.input_probs.get('C', 0)
            return (1 - p_a) * p_b * p_c
        
        # NAND2: Y = 1 - (A & B) = !(A & B)
        elif self.gate_type == "sky130_fd_sc_hd__nand2":
            p_a = self.input_probs.get('A', 0)
            p_b = self.input_probs.get('B', 0)
            return 1 - (p_a * p_b)

        # AND4: Y = A & B & C & D
        elif self.gate_type == "sky130_fd_sc_hd__and4":
            p_a = self.input_probs.get('A', 0)
            p_b = self.input_probs.get('B', 0)
            p_c = self.input_probs.get('C', 0)
            p_d = self.input_probs.get('D', 0)
            return p_a * p_b * p_c * p_d
        
        # AND4B: Y = (!A_N) & B & C & D
        elif self.gate_type == "sky130_fd_sc_hd__and4b":
            p_a = self.input_probs.get('A_N', 0)
            p_b = self.input_probs.get('B', 0)
            p_c = self.input_probs.get('C', 0)
            p_d = self.input_probs.get('D', 0)
            return (1 - p_a) * p_b * p_c * p_d



        # Gates OR/NOR and with inverter ORB
        # OR2: Y = A | B
        elif self.gate_type == "sky130_fd_sc_hd__or2":
            p_a = self.input_probs.get('A', 0)
            p_b = self.input_probs.get('B', 0)
            return 1 - (1 - p_a) * (1 - p_b)
        
        # NOR2: Y = !(A | B)
        elif self.gate_type == "sky130_fd_sc_hd__nor2":
            p_a = self.input_probs.get('A', 0)
            p_b = self.input_probs.get('B', 0)
            return (1 - p_a) * (1 - p_b)
        
        # OR3: Y = A | B | C
        elif self.gate_type == "sky130_fd_sc_hd__or3":
            p_a = self.input_probs.get('A', 0)
            p_b = self.input_probs.get('B', 0)
            p_c = self.input_probs.get('C', 0)
            return 1 - (1 - p_a) * (1 - p_b) * (1 - p_c)
        
        # OR4: Y = A | B | C | D
        elif self.gate_type == "sky130_fd_sc_hd__or4":
            p_a = self.input_probs.get('A', 0)
            p_b = self.input_probs.get('B', 0)
            p_c = self.input_probs.get('C', 0)
            p_d = self.input_probs.get('C', 0)

            return 1 - (1 - p_a) * (1 - p_b) * (1 - p_c) * (1 - p_d)

        # OR2B: Y = A | B_N
        elif self.gate_type == "sky130_fd_sc_hd__or2b":
            p_a = self.input_probs.get('A', 0)
            p_b = self.input_probs.get('B_N', 0)
            return 1 - (1 - p_a) * (p_b)
        
        # OR3B: Y = A | B | C_N
        elif self.gate_type == "sky130_fd_sc_hd__or3b":
            p_a = self.input_probs.get('A_N', 0)
            p_b = self.input_probs.get('B', 0)
            p_c = self.input_probs.get('C_N', 0)
            return 1 - (1 - p_a) * (1 - p_b) * (p_c)
        
        # OR4B: Y = A | B | C | D_N
        elif self.gate_type == "sky130_fd_sc_hd__or4b":
            p_a = self.input_probs.get('A_N', 0)
            p_b = self.input_probs.get('B', 0)
            p_c = self.input_probs.get('C', 0)
            p_d = self.input_probs.get('D_N', 0)
            return 1 - (1 - p_a) * (1 - p_b) * (1 - p_c) * (p_d)
        
        # OR4BB: Y = A | B | C | D_N
        elif self.gate_type == "sky130_fd_sc_hd__or4bb":
            p_a = self.input_probs.get('A_N', 0)
            p_b = self.input_probs.get('B', 0)
            p_c = self.input_probs.get('C_N', 0)
            p_d = self.input_probs.get('D_N', 0)
            return 1 - (1 - p_a) * (1 - p_b) * (p_c) * (p_d)


        # Gates XOR/XNOR
        # XOR2: Y = A ^ B 
        elif self.gate_type == "sky130_fd_sc_hd__xor2":
            p_a = self.input_probs.get('A', 0)
            p_b = self.input_probs.get('B', 0)
            return p_a * (1 - p_b) + (1 - p_a) * p_b
        
        # XNOR2: Y = !(A ^ B)
        elif self.gate_type == "sky130_fd_sc_hd__xnor2":
            p_a = self.input_probs.get('A', 0)
            p_b = self.input_probs.get('B', 0)
            return 1 - (p_a * (1 - p_b) + (1 - p_a) * p_b)
        

        # Gates Buffers & Inverters
        # Inverter: Y = !A
        elif self.gate_type == "sky130_fd_sc_hd__inv":
            p_a = self.input_probs.get('A', 0)
            return 1 - p_a
        
        # Buffer: Y = A
        elif self.gate_type == "sky130_fd_sc_hd__buf":
            p_a = self.input_probs.get('A', 0)
            return p_a
        
        # Buffer Inverter: Y = A
        elif self.gate_type == "sky130_fd_sc_hd__bufinv":
            p_a = self.input_probs.get('A', 0)
            p_y = 1 - p_a
            return p_y


        # Gates  OR-AND-Inverter (OAI) and with inverter OAIB
        # O21A: Y = (A1 | A2) & B1
        elif self.gate_type == "sky130_fd_sc_hd__o21a":
            p_a1 = self.input_probs.get('A1', 0)
            p_a2 = self.input_probs.get('A2', 0)
            p_b1 = self.input_probs.get('B1', 0)
            p_a_or = 1 - (1 - p_a1) * (1 - p_a2)    #  A1 | A2
            return p_a_or * p_b1
        
        # O211A: Y = (A1 | A2) & B1 & C1
        elif self.gate_type == "sky130_fd_sc_hd__o211a":
            p_a1 = self.input_probs.get('A1', 0)
            p_a2 = self.input_probs.get('A2', 0)
            p_b1 = self.input_probs.get('B1', 0)
            p_c1 = self.input_probs.get('C1', 0)
            p_a_or = 1 - (1 - p_a1) * (1 - p_a2)    #  A1 | A2
            return p_a_or * p_b1 * p_c1
        
        # O21BAI: Y = !((A1 | A2) & !B1_N)
        elif self.gate_type == "sky130_fd_sc_hd__o21bai":
            p_a1 = self.input_probs.get('A1', 0)
            p_a2 = self.input_probs.get('A2', 0)
            p_b1_n = self.input_probs.get('B1_N', 0)
            p_b1 = 1 - p_b1_n   # !B1_N
            p_a_or = 1 - (1 - p_a1) * (1 - p_a2)
            return 1 - (p_a_or * (1 - p_b1))
        
        # O21AI: Y = !((A1 | A2) & B1)
        elif self.gate_type == "sky130_fd_sc_hd__o21ai":
            p_a1 = self.input_probs.get('A1', 0)
            p_a2 = self.input_probs.get('A2', 0)
            p_b1 = self.input_probs.get('B1', 0)
            p_a_or = 1 - (1 - p_a1) * (1 - p_a2)    # A1 | A2
            p_and = p_a_or * p_b1                   # (A1 | A2) & B1
            p_y =  1 - p_and                        # Y = !(...)
            return p_y


        # Gates AND-OR-Inverter (AOI)
        # A21O: X = (A1 & A2) | B1
        elif self.gate_type == "sky130_fd_sc_hd__a21o":
            p_a1 = self.input_probs.get('A1', 0)
            p_a2 = self.input_probs.get('A2', 0)
            p_b1 = self.input_probs.get('B1', 0)
            p_a_and = p_a1 * p_a2               #  A1 & A2
            return 1 - (1 - p_a_and) * (1 - p_b1)

        # A211O: X = (A1 & A2) | B1 | C1
        elif self.gate_type == "sky130_fd_sc_hd__a211o":
            p_a1 = self.input_probs.get('A1', 0)
            p_a2 = self.input_probs.get('A2', 0)
            p_b1 = self.input_probs.get('B1', 0)
            p_c1 = self.input_probs.get('C1', 0)
            p_a_and = p_a1 * p_a2               #  A1 & A2
            return 1 - (1 - p_a_and) * (1 - p_b1) * (1 - p_c1)

        # A21BOI: Y = !((A1 & A2) | (!B1_N))
        elif self.gate_type == "sky130_fd_sc_hd__a21boi":
            p_a1 = self.input_probs.get('A1', 0)
            p_a2 = self.input_probs.get('A2', 0)
            p_b1_n = self.input_probs.get('B1_N', 0)
            p_b1 = 1 - p_b1_n   # !B1_N
            p_a_and = p_a1 * p_a2           #  A1 & A2
            return (1 - p_a_and) * p_b1


        # Celdas Secuenciales: 
        # DFXTP: FF Igual que la entrada
        elif self.gate_type == "sky130_fd_sc_hd__dfxtp":
            p_q = self.input_probs.get('D', 0)  # Usa D como entrada para flip-flops
            return p_q
        
        # Conb "Constant value, low, high outputs"
        # Pone la probabilidad de switching de la entrada a cero
        elif self.gate_type == "sky130_fd_sc_hd__conb":
            p_y = self.input_probs.get('LO', 0)  
            return 0    # Retorna cero por el LOW
        

        # TODO: Faltan completar...

        else:
            # Asumimos una probabilidad por defecto de 0.1 basado en el Weste-Harris
            return self.DEFAULT_GATE_PROB 
        

    def activity_factor(self):
        """
        @brief Calcula el factor de actividad de la salida de la compuerta logica.

        @return Factor de actividad de la salida.
        """
        p_y = self.calc_switching_probability()
        alpha_y = p_y * (1 - p_y)
        return alpha_y