import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import matplotlib.pyplot as plt


resistencia = ctrl.Antecedent(np.arange( 0, 101, 1),"resistencia")
risco = ctrl.Consequent(np.arange( 0,101, 1),"risco")

# 2- Conjunto fuzzy(Resistencia)
resistencia['muito_baixa'] = fuzz.trimf(resistencia.universe, [0, 3, 6])
resistencia['baixa'] = fuzz.trimf(resistencia.universe, [3, 6, 15])
resistencia['media_baixa'] = fuzz.trimf(resistencia.universe, [6, 15, 30])
resistencia['media'] = fuzz.trimf(resistencia.universe, [30, 40, 50])
resistencia['media_alta'] = fuzz.trimf(resistencia.universe, [50, 60, 70])
resistencia['alta'] = fuzz.trimf(resistencia.universe, [70, 90, 100])


# 3- Conjunto Fuzzy(Risco)
risco['muito_alto'] = fuzz.trimf(risco.universe, [70, 85, 100])
risco['alto'] = fuzz.trimf(risco.universe, [55, 70, 85])
risco['medio'] = fuzz.trimf(risco.universe, [35, 50, 65])
risco['baixo'] = fuzz.trimf(risco.universe, [15, 30, 45])
risco['muito_baixo'] = fuzz.trimf(risco.universe, [0, 10, 20])

# 4- Regras Fuzzy - 10
regras = [
    ctrl.Rule(resistencia['muito_baixa'], risco['muito_alto']),
    ctrl.Rule(resistencia['baixa'], risco['alto']),
    ctrl.Rule(resistencia['media_baixa'], risco['alto']),
    ctrl.Rule(resistencia['media_baixa'], risco['medio']),
    ctrl.Rule(resistencia['media'], risco['medio']),
    ctrl.Rule(resistencia['media'], risco['baixo']),
    ctrl.Rule(resistencia['media_alta'], risco['baixo']),
    ctrl.Rule(resistencia['media_alta'], risco['muito_baixo']),
    ctrl.Rule(resistencia['alta'], risco['muito_baixo']),
    ctrl.Rule(resistencia['alta'], risco['muito_baixo']),
]

#5-Sistema de controle
sistema = ctrl.ControlSystem(regras)
simulador = ctrl.ControlSystemSimulation(sistema)

#6- Exemplo
try:
    z = float(input("Digite um valor de Resistencia de isolamento eletrico entre **0 a 100**MΩ \n>>>"))
    if not (0 <= z <= 100):
        raise ValueError("Valor fora do intervalo permitido (0 a 100).")

    simulador.input['resistencia'] = z # Resistencia Baixa
    simulador.compute()

    #Resultado
    valorfinal = simulador.output['risco']
    print(f"Resistencia : {z}MΩ")
    print(f"Risco: {valorfinal:.2f}%")

    if valorfinal <= 33:
        categoria = 'baixo'
        print(f"Risco: {categoria} ")
    elif valorfinal <= 66:
        categoria = 'medio'
        print(f"Risco: {categoria} ")
    else:
        categoria = 'alto'
        print(f"Risco: {categoria} ")


    #Visualizações
    resistencia.view(sim = simulador)
    risco.view(sim = simulador)
    plt.show() # Manter Janela aberta

except ValueError as e:
    print("Erro:", e)