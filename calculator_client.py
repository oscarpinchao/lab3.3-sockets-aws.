import socket
import json

HOST = "18.222.136.221"
PORT = 8080

def start_client():
    while True:
        print("\n=== CALCULADORA TCP EN AWS ===")
        print("Operaciones soportadas: add, sub, mul, div")
        op = input("Ingrese operación (o 'exit' para salir): ").strip()
        
        if op.lower() == 'exit':
            print("Cerrando sesión del cliente...")
            break

        a_input = input("Ingrese primer número (a): ").strip()
        b_input = input("Ingrese segundo número (b): ").strip()

        try:
            a_val = float(a_input)
        except ValueError:
            a_val = a_input

        try:
            b_val = float(b_input)
        except ValueError:
            b_val = b_input

        payload = {
            "a": a_val,
            "b": b_val,
            "operation": op
        }

        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((HOST, PORT))
            s.send(json.dumps(payload).encode('utf-8'))

            raw_response = s.recv(1024).decode('utf-8')
            response = json.loads(raw_response)

            print("\n--- Respuesta del Servidor ---")
            print(f"Código HTTP: {response.get('code')}")
            print(f"Resultado:   {response.get('result')}")
            print(f"Error:       {response.get('error')}")
            s.close()
        except Exception as e:
            print(f"\n[!] Error de conexión: {e}")

if __name__ == "__main__":
    start_client()