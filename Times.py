import math
import time
import csv


# Función para la Criba de Atkin
def criba_de_atkin(limit):
    if limit < 2:
        return [] 

    primes = [False] * (limit + 1)
    sqrt_limit = int(math.sqrt(limit)) + 1

    for x in range(1, sqrt_limit):
        for y in range(1, sqrt_limit):
            
            n = 4 * x**2 + y**2
            if n <= limit and (n % 12 == 1 or n % 12 == 5):
                primes[n] = not primes[n]

            n = 3 * x**2 + y**2
            if n <= limit and n % 12 == 7:
                primes[n] = not primes[n]

            n = 3 * x**2 - y**2
            if x > y and n <= limit and n % 12 == 11:
                primes[n] = not primes[n]
    
    for x in range(5, sqrt_limit):
        if primes[x]:
            for y in range(x**2, limit + 1, x**2):
                primes[y] = False
    
    primes[2] = True
    primes[3] = True

    return [x for x in range(limit + 1) if primes[x]]


# Exportar los resultados como CSV
def exportar_csv(data, filename):
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["Primo en posición", "Tiempo de ejecución (s)"]) 
        writer.writerows(data)



if __name__ == "__main__":
    limits = [29, 541, 7919, 1299709, 15485863, 179424673] 
    dataset = []


    for i, limit in enumerate(limits, start=1):
        start_time = time.time()  
        primes = criba_de_atkin(limit)
        end_time = time.time()
        total_time = end_time - start_time  


        print(f"Límite: {limit}")
        print(f"Tiempo de ejecución: {total_time:.6f} segundos")
        print(f"Número de primos encontrados: {len(primes)}")
        print("-" * 40)

        dataset.append([i, total_time])


    # Exportar los resultados
    exportar_csv(dataset, "primos_tiempos.csv")
    print("Datos exportados a 'primos_tiempos.csv'")