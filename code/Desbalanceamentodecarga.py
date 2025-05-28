import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import matplotlib.pyplot as plt


Desbalanceamentodecarga = ctrl.Antecedent(np.arange(0, 3.01, 0.01), "Desbalanceamentodecarga")
risco = ctrl.Consequent(np.arange( 0,101, 1),"risco")

# 2- Conjunto fuzzy(Desbalanceamento de carga)
Desbalanceamentodecarga['muito_baixo'] = fuzz.trapmf(Desbalanceamentodecarga.universe, [0.00, 0.00, 0.20, 0.60])
Desbalanceamentodecarga['baixo'] = fuzz.trapmf(Desbalanceamentodecarga.universe, [0.50, 0.70, 1.00, 1.20])
Desbalanceamentodecarga['medio_baixo'] = fuzz.trapmf(Desbalanceamentodecarga.universe, [1.00, 1.20, 1.30, 1.40])
Desbalanceamentodecarga['medio'] = fuzz.trapmf(Desbalanceamentodecarga.universe, [1.30, 1.50, 1.60, 1.70])
Desbalanceamentodecarga['medio_alto'] = fuzz.trapmf(Desbalanceamentodecarga.universe, [1.60, 1.80, 1.90, 2.00])
Desbalanceamentodecarga['alto'] = fuzz.trapmf(Desbalanceamentodecarga.universe, [1.90, 2.10, 2.20, 2.30])
Desbalanceamentodecarga['muito_alto'] = fuzz.trapmf(Desbalanceamentodecarga.universe, [2.20, 2.50, 3.00, 3.00])


# 3- Conjunto Fuzzy(Risco)
risco['muito_baixo'] = fuzz.trimf(risco.universe, [0, 10, 20])
risco['baixo'] = fuzz.trimf(risco.universe, [15, 30, 45])
risco['medio'] = fuzz.trimf(risco.universe, [35, 50, 65])
risco['alto'] = fuzz.trimf(risco.universe, [55, 70, 85])
risco['muito_alto'] = fuzz.trimf(risco.universe, [70, 85, 100])

# 4- Regras Fuzzy - 10
regras = [
    ctrl.Rule(Desbalanceamentodecarga['muito_baixo'], risco['muito_baixo']),
    ctrl.Rule(Desbalanceamentodecarga['baixo'], risco['baixo']),
    ctrl.Rule(Desbalanceamentodecarga['medio_baixo'], risco['medio']),
    ctrl.Rule(Desbalanceamentodecarga['medio'], risco['medio']),
    ctrl.Rule(Desbalanceamentodecarga['medio_alto'], risco['alto']),
    ctrl.Rule(Desbalanceamentodecarga['alto'], risco['alto']),
    ctrl.Rule(Desbalanceamentodecarga['muito_alto'], risco['muito_alto']),
    ctrl.Rule(Desbalanceamentodecarga['baixo'] & risco['baixo'], risco['medio']),  
    ctrl.Rule(Desbalanceamentodecarga['medio_baixo'] & risco['medio'], risco['alto']),
    ctrl.Rule(Desbalanceamentodecarga['alto'] & risco['alto'], risco['muito_alto']),
]

#5-Sistema de controle
sistema = ctrl.ControlSystem(regras)
simulador = ctrl.ControlSystemSimulation(sistema)

#6- Exemplo
try:
    z = float(input("Digite um valor do Desbalanceamento da Carga entre **0 a 3**% \n>>> "))
    if not (0 <= z <= 3):
        raise ValueError("Valor fora do intervalo permitido (0 a 3).")

    simulador.input['Desbalanceamentodecarga'] = z
    simulador.compute()

    print(f"Desbalanceamento de Carga: {z}%")
    print(f"Risco: {simulador.output['risco']:.2f}%")

    # Visualização dos gráficos
    Desbalanceamentodecarga .view(sim=simulador)
    risco.view(sim=simulador)
    plt.show() # Manter Janela aberta

except ValueError as e:
    print("Erro:", e)