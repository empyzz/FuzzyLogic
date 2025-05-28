import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import matplotlib.pyplot as plt


corrente_partida = ctrl.Antecedent(np.arange( 0, 11, 0.1),"corrente_partida")
risco = ctrl.Consequent(np.arange( 0,101, 1),"risco")

# 2- Conjunto fuzzy(Corrente de partida)
corrente_partida['muito_baixa'] = fuzz.trapmf(corrente_partida.universe, [0, 0, 1.5, 2.5])
corrente_partida['baixa'] = fuzz.trapmf(corrente_partida.universe, [2.0, 2.5, 3.5, 4.5])
corrente_partida['media'] = fuzz.trapmf(corrente_partida.universe, [4.0, 4.5, 6.0, 7.0])
corrente_partida['alta'] = fuzz.trapmf(corrente_partida.universe, [6.5, 7.5, 10, 10])

# 3- Conjunto Fuzzy(Risco)
risco['muito_alto'] = fuzz.trimf(risco.universe, [70, 85, 100])
risco['alto'] = fuzz.trimf(risco.universe, [55, 70, 85])
risco['medio'] = fuzz.trimf(risco.universe, [35, 50, 65])
risco['baixo'] = fuzz.trimf(risco.universe, [15, 30, 45])
risco['muito_baixo'] = fuzz.trimf(risco.universe, [0, 10, 20])

# 4- Regras Fuzzy - 10
regras = [
    ctrl.Rule(corrente_partida['muito_baixa'], risco['muito_alto']),
    ctrl.Rule(corrente_partida['muito_baixa'], risco['alto']),
    ctrl.Rule(corrente_partida['baixa'], risco['alto']),
    ctrl.Rule(corrente_partida['baixa'], risco['medio']),
    ctrl.Rule(corrente_partida['media'], risco['medio']),
    ctrl.Rule(corrente_partida['media'], risco['baixo']),
    ctrl.Rule(corrente_partida['media'], risco['baixo']),
    ctrl.Rule(corrente_partida['alta'], risco['baixo']),
    ctrl.Rule(corrente_partida['alta'], risco['muito_baixo']),
    ctrl.Rule(corrente_partida['alta'], risco['muito_baixo']),
]

#5-Sistema de controle
sistema = ctrl.ControlSystem(regras)
simulador = ctrl.ControlSystemSimulation(sistema)

#6- Exemplo
try:
    z = float(input("Digite um valor da Corrente de partida entre **0 a 10** \n>>> "))
    if not (0 <= z <= 10):
        raise ValueError("Valor fora do intervalo permitido (0 a 10).")

    simulador.input['corrente_partida'] = z
    simulador.compute()

    print(f"Corrente de Partida: {z}")
    print(f"Risco: {simulador.output['risco']:.2f}%")

    # Visualização dos gráficos
    corrente_partida.view(sim=simulador)
    risco.view(sim=simulador)
    plt.show() # Manter Janela aberta

except ValueError as e:
    print("Erro:", e)