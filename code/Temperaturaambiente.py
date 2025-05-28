import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import matplotlib.pyplot as plt


TemperaturaAmbiente = ctrl.Antecedent(np.arange(0, 61, 1), "TemperaturaAmbiente")
risco = ctrl.Consequent(np.arange( 0,101, 1),"risco")

# 2- Conjunto fuzzy(Temperatura Ambiente)
TemperaturaAmbiente['muito_baixa'] = fuzz.trapmf(TemperaturaAmbiente.universe, [0, 5, 10, 20])  
TemperaturaAmbiente['baixa'] = fuzz.trapmf(TemperaturaAmbiente.universe, [15, 20, 25, 28])
TemperaturaAmbiente['media'] = fuzz.trapmf(TemperaturaAmbiente.universe, [28, 34, 40, 45])
TemperaturaAmbiente['alta'] = fuzz.trapmf(TemperaturaAmbiente.universe, [45, 50, 55, 60])

# 3- Conjunto Fuzzy(Risco)
risco['muito_alto'] = fuzz.trimf(risco.universe, [70, 85, 100])
risco['alto'] = fuzz.trimf(risco.universe, [55, 70, 85])
risco['medio'] = fuzz.trimf(risco.universe, [35, 50, 65])
risco['baixo'] = fuzz.trimf(risco.universe, [15, 30, 45])
risco['muito_baixo'] = fuzz.trimf(risco.universe, [0, 10, 20])

# 4- Regras Fuzzy - 10
regras = [
    ctrl.Rule(TemperaturaAmbiente['muito_baixa'], risco['muito_alto']), # Muito frio
    ctrl.Rule(TemperaturaAmbiente['muito_baixa'], risco['alto']),
    ctrl.Rule(TemperaturaAmbiente['baixa'], risco['alto']),
    ctrl.Rule(TemperaturaAmbiente['baixa'], risco['medio']),
    ctrl.Rule(TemperaturaAmbiente['media'], risco['medio']),
    ctrl.Rule(TemperaturaAmbiente['media'], risco['baixo']),
    ctrl.Rule(TemperaturaAmbiente['media'], risco['baixo']),
    ctrl.Rule(TemperaturaAmbiente['alta'], risco['muito_alto']),
    ctrl.Rule(TemperaturaAmbiente['alta'], risco['alto']), # Muito Quente
]

#5-Sistema de controle
sistema = ctrl.ControlSystem(regras)
simulador = ctrl.ControlSystemSimulation(sistema)

#6- Exemplo
try:
    z = float(input("Digite um valor da Temperatura ambiente entre **0 a 60**°C \n>>> "))
    if not (0 <= z <= 60):
        raise ValueError("Valor fora do intervalo permitido (0 a 60).")

    simulador.input['TemperaturaAmbiente'] = z
    simulador.compute()

    print(f"Temperatura Ambiente: {z}° Celsius")
    print(f"Risco: {simulador.output['risco']:.2f}%")

    # Visualização dos gráficos
    TemperaturaAmbiente.view(sim=simulador)
    risco.view(sim=simulador)
    plt.show() # Manter Janela aberta

except ValueError as e:
    print("Erro:", e)