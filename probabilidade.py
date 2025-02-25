import tkinter as tk
from tkinter import messagebox

def calcular_probabilidade_dac(idade, sexo, sintoma, fatores_risco):
    """
    Calcula a probabilidade de pré-teste de DAC.
    
    :param idade: Idade do paciente (int)
    :param sexo: "homem" ou "mulher"
    :param sintoma: "tipica", "atipica", "nao_anginosa", "assintomatico"
    :param fatores_risco: Lista de fatores de risco presentes (ex: ["diabetes", "hipertensao"])
    :return: Probabilidade estimada (%) ou mensagem de erro
    """
    tabela_prob = {
        "homem": {
            (30, 39): {"tipica": 12, "atipica": 3, "nao_anginosa": 0, "assintomatico": 0},
            (40, 49): {"tipica": 22, "atipica": 10, "nao_anginosa": 3, "assintomatico": 1},
            (50, 59): {"tipica": 32, "atipica": 17, "nao_anginosa": 8, "assintomatico": 3},
            (60, 69): {"tipica": 44, "atipica": 26, "nao_anginosa": 13, "assintomatico": 6},
        },
        "mulher": {
            (30, 39): {"tipica": 1, "atipica": 0, "nao_anginosa": 0, "assintomatico": 0},
            (40, 49): {"tipica": 4, "atipica": 2, "nao_anginosa": 1, "assintomatico": 0},
            (50, 59): {"tipica": 13, "atipica": 6, "nao_anginosa": 2, "assintomatico": 1},
            (60, 69): {"tipica": 32, "atipica": 12, "nao_anginosa": 3, "assintomatico": 2},
        }
    }
    
    faixa_etaria = next((k for k in tabela_prob[sexo] if k[0] <= idade <= k[1]), None)
    if faixa_etaria is None:
        return None, "Idade fora da faixa considerada (30-69 anos)"
    
    probabilidade_base = tabela_prob[sexo][faixa_etaria].get(sintoma, 0)
    
    ajuste = 1 + (0.1 * len(fatores_risco))
    probabilidade_final = min(probabilidade_base * ajuste, 100)
    
    return round(probabilidade_final, 2), None

def recomendar_conduta(probabilidade):
    if probabilidade < 15:
        return "Conduta: Acompanhamento clínico, medidas preventivas.\nMedidas preventivas: Alimentação saudável, prática regular de exercícios, controle de peso, cessação do tabagismo, controle da pressão arterial e glicemia."
    elif 15 <= probabilidade < 85:
        return "Conduta: Exames adicionais como teste ergométrico ou cintilografia miocárdica."
    else:
        return "Conduta: Avaliação invasiva com cateterismo cardíaco."

def calcular():
    try:
        idade = int(entry_idade.get())
        sexo = var_sexo.get()
        sintoma = var_sintoma.get()
        fatores_risco = [f for f, v in fatores.items() if v.get()]
        
        probabilidade, erro = calcular_probabilidade_dac(idade, sexo, sintoma, fatores_risco)
        if erro:
            messagebox.showerror("Erro", erro)
            return
        
        conduta = recomendar_conduta(probabilidade)
        messagebox.showinfo("Resultado", f"Probabilidade estimada de DAC: {probabilidade}%\n{conduta}")
    except ValueError:
        messagebox.showerror("Erro", "Por favor, insira uma idade válida.")

root = tk.Tk()
root.title("Calculadora de Probabilidade de DAC")

tk.Label(root, text="Idade:").grid(row=0, column=0)
entry_idade = tk.Entry(root)
entry_idade.grid(row=0, column=1)

var_sexo = tk.StringVar(value="homem")
tk.Label(root, text="Sexo:").grid(row=1, column=0)
tk.Radiobutton(root, text="Homem", variable=var_sexo, value="homem").grid(row=1, column=1)
tk.Radiobutton(root, text="Mulher", variable=var_sexo, value="mulher").grid(row=1, column=2)

var_sintoma = tk.StringVar(value="tipica")
tk.Label(root, text="Sintoma:").grid(row=2, column=0)
tk.OptionMenu(root, var_sintoma, "tipica", "atipica", "nao_anginosa", "assintomatico").grid(row=2, column=1)

fatores = {
    "diabetes": tk.BooleanVar(),
    "hipertensao": tk.BooleanVar(),
    "tabagismo": tk.BooleanVar(),
    "dislipidemia": tk.BooleanVar(),
    "hist_familiar": tk.BooleanVar()
}

tk.Label(root, text="Fatores de Risco:").grid(row=3, column=0)
i = 1
for fator, var in fatores.items():
    tk.Checkbutton(root, text=fator.capitalize(), variable=var).grid(row=3, column=i)
    i += 1

tk.Button(root, text="Calcular", command=calcular).grid(row=4, columnspan=3)

root.mainloop()
