import urllib.request
import random
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

ENLACE = "https://nintendoproject.com/redir/?ref=erdigos"

navegadores = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Safari/605.1.15",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/119.0",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Mobile/15E148 Safari/604.1"
]

def simular_visita(numero):
    user_agent = random.choice(navegadores)
    req = urllib.request.Request(
        ENLACE, 
        headers={
            'User-Agent': user_agent,
            'Accept-Language': 'es-ES,es;q=0.9',
            'Connection': 'close'
        }
    )
    # Pequeña pausa aleatoria para no saturar la pasarela de golpe
    time.sleep(random.uniform(0.1, 0.4))
    
    try:
        with urllib.request.urlopen(req, timeout=6) as response:
            return f"[{numero}] OK ({response.status})"
    except Exception as e:
        return f"[{numero}] Error: {e}"

def main():
    TOTAL_PETICIONES = 300  # Lote optimizado para evitar bloqueos
    HILOS_CONCURRENTES = 20 # 20 hilos simultáneos estables (ni muy lentos ni saturados)

    print(f"[*] Lanzando {TOTAL_PETICIONES} visitas con {HILOS_CONCURRENTES} hilos controlados...")
    
    with ThreadPoolExecutor(max_workers=HILOS_CONCURRENTES) as executor:
        futures = [executor.submit(simular_visita, i) for i in range(1, TOTAL_PETICIONES + 1)]
        for future in as_completed(futures):
            print(future.result())

if __name__ == "__main__":
    main()
