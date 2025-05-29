import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import matplotlib.pyplot as plt

#Resistência do isolamento elétrico
def ResistenciaIsolamentoEletrico():
    # 1 - Entradas
    resistencia = ctrl.Antecedent(np.arange( 0, 101, 1),"resistencia")
    risco = ctrl.Consequent(np.arange( 0,101, 1),"risco")

    # 2- Conjunto fuzzy(Resistencia)
    resistencia['muito_baixa'] = fuzz.trimf(resistencia.universe, [0, 3, 6])
    resistencia['baixa'] = fuzz.trimf(resistencia.universe, [3, 6, 15])
    resistencia['media_baixa'] = fuzz.trimf(resistencia.universe, [6, 15, 30])
    resistencia['media'] = fuzz.trimf(resistencia.universe, [30, 45, 60])
    resistencia['media_alta'] = fuzz.trimf(resistencia.universe, [50, 65, 80])
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

#Corrente de partida
def CorrenteDePartida():
    # 1- Entradas
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

        valorfinal = simulador.output['risco']
        print(f"Corrente de Partida: {z}")
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

        # Visualização dos gráficos
        corrente_partida.view(sim=simulador)
        risco.view(sim=simulador)
        plt.show() # Manter Janela aberta

    except ValueError as e:
        print("Erro:", e)

#Carga aplicada ao motor
def CargaAplicada():
    # 1- Entradas
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

        valorfinal = simulador.output['risco']
        print(f"Carga aplicada ao motor: {z}%")
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

        # Visualização dos gráficos
        CargaAplicada.view(sim=simulador)
        risco.view(sim=simulador)
        plt.show() # Manter Janela aberta

    except ValueError as e:
        print("Erro:", e)

#Temperatura ambiente
def TemperaturaAmbiente():
    # 1- Entrada
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

        valorfinal = simulador.output['risco']
        print(f"Temperatura Ambiente: {z}° Celsius")
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

        # Visualização dos gráficos
        TemperaturaAmbiente.view(sim=simulador)
        risco.view(sim=simulador)
        plt.show() # Manter Janela aberta

    except ValueError as e:
        print("Erro:", e)

#Desbalanceamento de carga
def DesbalanceamentodeCarga():
    # 1- Entradas
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

        valorfinal = simulador.output['risco']
        print(f"Desbalanceamento de Carga: {z}%")
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


        # Visualização dos gráficos
        Desbalanceamentodecarga .view(sim=simulador)
        risco.view(sim=simulador)
        plt.show() # Manter Janela aberta

    except ValueError as e:
        print("Erro:", e)


def main():
    print('1.Resistência do isolamento elétrico\n2.Corrente de partida\n3.Carga aplicada ao motor\n4.Temperatura ambiente\n5.Desbalanceamento de carga')
    x: int = int(input("Escolha uma variável (Por número): "))

    if x ==  1:
        ResistenciaIsolamentoEletrico()
    if x == 2:
        CorrenteDePartida()
    if x == 3:
        CargaAplicada()
    if x == 4:
        TemperaturaAmbiente()
    if x == 5:
        DesbalanceamentodeCarga()
    else:
        print("Digite um valor entre 1 e 5 ")
        return main
    

if __name__ == '__main__':
    main()