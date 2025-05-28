import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import matplotlib.pyplot as plt


CargaAplicada = ctrl.Antecedent(np.arange( 0, 151, 1),"CargaAplicada")
risco = ctrl.Consequent(np.arange( 0,101, 1),"risco")

# 2- Conjunto fuzzy(Carga Aplicada)
CargaAplicada['muito_baixa'] = fuzz.trapmf(CargaAplicada.universe, [0, 0, 20, 50])      
CargaAplicada['baixa'] = fuzz.trapmf(CargaAplicada.universe, [40, 50, 60, 80])         
CargaAplicada['media'] = fuzz.trapmf(CargaAplicada.universe, [70, 90, 100, 110])        
CargaAplicada['alta'] = fuzz.trapmf(CargaAplicada.universe, [100, 120, 150, 150])      

# 3- Conjunto Fuzzy(Risco)
risco['muito_alto'] = fuzz.trimf(risco.universe, [70, 85, 100])
risco['alto'] = fuzz.trimf(risco.universe, [55, 70, 85])
risco['medio'] = fuzz.trimf(risco.universe, [35, 50, 65])
risco['baixo'] = fuzz.trimf(risco.universe, [15, 30, 45])
risco['muito_baixo'] = fuzz.trimf(risco.universe, [0, 10, 20])

# 4- Regras Fuzzy - 10
regras = [
    ctrl.Rule(CargaAplicada['muito_baixa'], risco['muito_alto']),
    ctrl.Rule(CargaAplicada['muito_baixa'], risco['alto']),
    ctrl.Rule(CargaAplicada['baixa'], risco['alto']),
    ctrl.Rule(CargaAplicada['baixa'], risco['medio']),
    ctrl.Rule(CargaAplicada['media'], risco['medio']),
    ctrl.Rule(CargaAplicada['media'], risco['baixo']),
    ctrl.Rule(CargaAplicada['media'], risco['baixo']),
    ctrl.Rule(CargaAplicada['alta'], risco['baixo']),
    ctrl.Rule(CargaAplicada['alta'], risco['muito_baixo']),
    ctrl.Rule(CargaAplicada['alta'], risco['muito_baixo']),
]

#5-Sistema de controle
sistema = ctrl.ControlSystem(regras)
simulador = ctrl.ControlSystemSimulation(sistema)

#6- Exemplo
try:
    z = float(input("Digite um valor da Carga aplicada ao motor entre **0 a 150**% \n>>> "))
    if not (0 <= z <= 150):
        raise ValueError("Valor fora do intervalo permitido (0 a 150).")

    simulador.input['CargaAplicada'] = z
    simulador.compute()

    print(f"Carga aplicada ao motor: {z}%")
    print(f"Risco: {simulador.output['risco']:.2f}%")

    # Visualização dos gráficos
    CargaAplicada.view(sim=simulador)
    risco.view(sim=simulador)
    plt.show() # Manter Janela aberta

except ValueError as e:
    print("Erro:", e)