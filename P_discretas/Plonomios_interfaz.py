import tkinter as tk

def limpiar_entrada(f):
    f = f.replace(" ", "").replace("-", "+-")
    f = f.replace("{+-", "-").replace("$", "").replace("{", "").replace("}", "")
    f = f.replace("(", " ").replace(")", " ")
    return f.strip().split("  ")

def separar_terminos(factores):
    coeficientes = []
    for factor in factores:
        terminos = factor.split("+")
        coeficientes.append([t for t in terminos if t])
    return coeficientes


def extraer_coeficientes_exponentes(terminos):
    coeficientes = []
    exponentes = []
    for factor in terminos:
        c_factor = []
        e_factor = []
        for termino in factor:
            if "x" in termino:
                pos = termino.index("x")
                coef_str = termino[:pos]
                coef = -1 if coef_str == "-" else (1 if coef_str == "" else int(coef_str))
                if "^" in termino:
                    exp = int(termino.split("^")[1])
                else:
                    exp = 1
            else:
                coef = int(termino)
                exp = 0
            c_factor.append(coef)
            e_factor.append(exp)
        coeficientes.append(c_factor)
        exponentes.append(e_factor)
    return coeficientes, exponentes

def multiplicar_polinomios(coeficientes, exponentes):
    while len(coeficientes) >= 2:
        a, b = coeficientes[0], coeficientes[1]
        c, d = exponentes[0], exponentes[1]
        productoC = [a[i]*b[j] for i in range(len(a)) for j in range(len(b))]
        sumaE = [c[i]+d[j] for i in range(len(c)) for j in range(len(d))]
        coeficientes = [productoC] + coeficientes[2:]
        exponentes = [sumaE] + exponentes[2:]
    return coeficientes[0], exponentes[0]

def sumar_terminos_semejantes(coeficientes, exponentes):
    i = 0
    while i < len(exponentes):
        j = i + 1
        while j < len(exponentes):
            if coeficientes[i] == 0:
                coeficientes.pop(i)
                exponentes.pop(i)
                j = i + 1
            elif exponentes[i] == exponentes[j]:
                coeficientes[i] += coeficientes[j]
                coeficientes.pop(j)
                exponentes.pop(j)
                j = i + 1
            else:
                j += 1
        i += 1
    return coeficientes, exponentes

def ordenar(coeficientes, exponentes):
    pares = sorted(zip(exponentes, coeficientes), reverse=True)
    exp_ordenado, coef_ordenado = zip(*pares)
    return list(coef_ordenado), list(exp_ordenado)

def formato_LaTex(coef, exp):
    pol = []
    for c, e in zip(coef, exp):
        termino = ""
        if e == 0 or c != 1:
            termino += str(c)
        if e != 0:
            termino += 'x'
        if e > 1:
            termino += f'^{{{e}}}'
        pol.append(termino)
    return '$' + ' + '.join(pol).replace(' + -', ' - ') + '$'

def procesar_entrada():
    f = polinomio.get()
    factores = limpiar_entrada(f)
    terminos = separar_terminos(factores)
    coeficientes, exponentes = extraer_coeficientes_exponentes(terminos)
    coef_final, exp_final = multiplicar_polinomios(coeficientes, exponentes)
    coef_final, exp_final = sumar_terminos_semejantes(coef_final, exp_final)
    coef_final, exp_final = ordenar(coef_final, exp_final)
    return formato_LaTex(coef_final, exp_final)

def ejecutar():
    procesado = procesar_entrada()
    resultado.set(f"Resultado: {procesado}") 
    
wind = tk.Tk()
#dimensiones HxL
wind.geometry('600x300')
wind.configure(background="#f0f0f0")
wind.resizable(False,False)

tk.Wm.wm_title(wind,'Multiplicador de polinomios')

frame1=tk.Frame(
    wind,
    bg="#f0f0f0",
)
frame1.pack(expand=True, fill='both')

frame = tk.Frame(frame1, bg="#f0f0f0")
frame.place(relx=0.5, rely=0.5, anchor='center')

tk.Label(
    frame, 
    text="Ingrese el polinomio en LaTeX (Ej: $(x+1)(x+2)$):",
    bg="#f0f0f0",
    font=('arial', 12)
    
    ).pack(pady=10)

polinomio=tk.Entry(
    frame,
    width=30)

polinomio.pack(pady=10)

tk.Button(
    frame,
    text='Ejecutar',
    font=('arial', 12),
    bg="#81a3b0",
    #command= llamar funcion como objeto
    command=ejecutar).pack(pady=10)

resultado = tk.StringVar()

tk.Label(
    frame, 
    textvariable=resultado, 
    font=("arial", 14), 
    bg="#f0f0f0"
    ).pack(pady=10)

wind.mainloop()


 