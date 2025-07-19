

import json
import math
from decimal import Decimal, getcontext
import matplotlib.pyplot as plt

# Imposta la precisione per i calcoli Decimal. 
# La precisione di 50 dovrebbe essere più che sufficiente per la mantissa.
getcontext().prec = 50

def log_from_str(numero_str: str) -> tuple[int, float]:
    """
    Data una stringa numerica, calcola la caratteristica e la mantissa del suo logaritmo in base 10.

    Args:
        numero_str: Il numero in formato stringa.

    Returns:
        Una tupla (caratteristica, mantissa).
    """
    if not numero_str.isdigit() or int(numero_str) <= 0:
        # Il logaritmo di numeri non positivi non è definito nei reali.
        # Gestiamo questo caso, anche se il file JSON fornito sembra contenere solo interi positivi.
        return 0, 0.0

    # La caratteristica del logaritmo in base 10 di un intero è il numero di cifre meno 1.
    caratteristica = len(numero_str) - 1

    # Per calcolare la mantissa con alta precisione, usiamo il tipo Decimal.
    # Normalizziamo il numero per portarlo nel range [1, 10)
    # Esempio: "12345" -> Decimal("1.2345")
    decimal_val = Decimal(numero_str[0] + '.' + numero_str[1:])
    
    # La mantissa è il log10 di questo valore normalizzato.
    mantissa = decimal_val.log10()

    return caratteristica, float(mantissa)

def json_from_log_str(file_path: str) -> list[tuple[int, float]]:
    """
    Legge un file JSON contenente una serie di Fibonacci, calcola il logaritmo di ogni numero
    e restituisce una lista di tuple (n, log(fib(n))).

    Args:
        file_path: Il percorso del file JSON.

    Returns:
        Una lista di tuple nel formato (n, valore_log).
    """
    try:
        with open(file_path, 'r') as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"Errore: File non trovato in {file_path}")
        return []
    except json.JSONDecodeError:
        print(f"Errore: Il file in {file_path} non è un JSON valido.")
        return []

    serie_fibonacci = data.get("serie_fibonacci", [])
    log_list = []

    for item in serie_fibonacci:
        for n_str, numero_str in item.items():
            n = int(n_str)
            
            # Calcola caratteristica e mantissa
            caratteristica, mantissa = log_from_str(numero_str)
            
            # Il valore del logaritmo è la loro somma
            log_value = caratteristica + mantissa
            
            log_list.append((n, log_value))

    return log_list

def plot_graph():
    xy_data = json_from_log_str('fibonacci-sorted.json')

    # Unzip della lista di tuple in due liste separate per gli assi
    x_values = [item[0] for item in xy_data]
    y_values = [item[1] for item in xy_data]

    # Utilizza le funzioni di `matplotlib` per generare il grafico, personalizzarlo con etichette e un titolo,
    # e infine mostrarlo a schermo.

    plt.figure(figsize=(12, 7))  # Dimensioni del grafico
    plt.plot(x_values, y_values, marker='.', linestyle='-', color='b')
    plt.title('Crescita del Logaritmo dei Numeri di Fibonacci')
    plt.xlabel('Indice (n)')
    plt.ylabel('Logaritmo in base 10 di Fib(n)')
    plt.grid(True, which='both', linestyle='--', linewidth=0.5)
    plt.show()

if __name__ == "__main__":
    file_to_process = 'fibonacci-sorted_v2.json'
    log_data = json_from_log_str(file_to_process)

    # Plotta il grafico
    plot_graph()

