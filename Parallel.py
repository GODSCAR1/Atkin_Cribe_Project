import math
import multiprocessing
import multiprocessing.shared_memory as sm
import time
import csv

def atkin_worker_shared_memory(start, end, n, shm_name):
   
    existing_shm = sm.SharedMemory(name=shm_name)
    shared_array = memoryview(existing_shm.buf).cast('B')

    try:
        for x in range(start, end):
            for y in range(1, int(math.sqrt(n)) + 1):
                num1 = 4 * x**2 + y**2
                if num1 <= n and (num1 % 12 == 1 or num1 % 12 == 5):
                    shared_array[num1] ^= 1
                num2 = 3 * x**2 + y**2
                if num2 <= n and num2 % 12 == 7:
                    shared_array[num2] ^= 1  # Toggle the value
                num3 = 3 * x**2 - y**2
                if x > y and num3 <= n and num3 % 12 == 11:
                    shared_array[num3] ^= 1  # Toggle the value
    finally:
        shared_array.release()
        existing_shm.close()

def eliminate_multiples_of_squares_shared_memory(n, shm_name):
   
    existing_shm = sm.SharedMemory(name=shm_name)
    shared_array = memoryview(existing_shm.buf).cast('B')

    try:
        for x in range(5, int(math.sqrt(n)) + 1):
            if shared_array[x]:
                for k in range(x**2, n + 1, x**2):
                    shared_array[k] = 0  
    finally:
        shared_array.release()
        existing_shm.close()

def parallel_atkin_shared_memory(n, num_workers=4):
    
    shm = sm.SharedMemory(create=True, size=n + 1)
    shared_array = memoryview(shm.buf).cast('B')  
    shared_array[:] = bytes(n + 1) 

    try:
        
        sqrt_n = int(math.sqrt(n))
        chunk_size = math.ceil(sqrt_n / num_workers)
        ranges = [
           (i * chunk_size + 1, min((i + 1) * chunk_size, sqrt_n) + 1, n, shm.name) for i in range(num_workers)
        ]
       
        with multiprocessing.Pool(processes=num_workers) as pool:
            pool.starmap(atkin_worker_shared_memory, ranges)
       
        eliminate_multiples_of_squares_shared_memory(n, shm.name)
        
        primes = sum(shared_array) + 2
    finally:
        # Clean up shared memory
        shared_array.release()
        shm.close()
        shm.unlink()
    return primes


def exportar_csv(data, filename):
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["Primo en posición", "Tiempo de ejecución (s)"])  # Cabecera
        writer.writerows(data)

if __name__ == "__main__":
    limit = 179424673 
    dataset = []
    times = 30
    for i in range(times):
        start_time = time.time()  
        primes = parallel_atkin_shared_memory(limit, num_workers=4)
        end_time = time.time()      
        total_time = end_time - start_time

        print(f"Límite: {limit}")
        print(f"Tiempo de ejecución: {total_time:.6f} segundos")
        print(f"Número de primos encontrados: {primes}")
        print(i)
        print("-" * 40)

        dataset.append([i + 1, total_time])
    # Exportar los resultados
    exportar_csv(dataset, "30_runs_parallel_mint.csv")
    print("Datos exportados a '30_runs_parallel_mint.csv'")