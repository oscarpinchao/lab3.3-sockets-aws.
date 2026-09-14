import socket
import json

HOST = "0.0.0.0"
PORT = 8080

def handle_request(raw_data, client_ip):
    response = {"result": None, "error": None, "code": 500}
    
    try:
        payload = json.loads(raw_data)
    except Exception:
        response["error"] = "Invalid JSON format"
        response["code"] = 400
        print(f"Client: {client_ip}\nError: Invalid JSON\nCode: 400\n" + "-"*30)
        return response

    if not isinstance(payload, dict) or "a" not in payload or "b" not in payload or "operation" not in payload:
        response["error"] = "Missing required fields (a, b, operation)"
        response["code"] = 400
        print(f"Client: {client_ip}\nError: Missing fields\nCode: 400\n" + "-"*30)
        return response

    a_raw = payload.get("a")
    b_raw = payload.get("b")
    op = str(payload.get("operation")).lower()

    try:
        a = float(a_raw)
        b = float(b_raw)
    except (ValueError, TypeError):
        response["error"] = "Invalid input: 'a' and 'b' must be numbers"
        response["code"] = 422
        print(f"Client: {client_ip}\nOperation: {op}\na: {a_raw}\nb: {b_raw}\nError: Invalid input\nCode: 422\n" + "-"*30)
        return response

    if op == "add":
        res = a + b
    elif op == "sub":
        res = a - b
    elif op == "mul":
        res = a * b
    elif op == "div":
        if b == 0:
            response["error"] = "Division by zero"
            response["code"] = 422
            print(f"Client: {client_ip}\nOperation: {op}\na: {a}\nb: {b}\nError: Division by zero\nCode: 422\n" + "-"*30)
            return response
        res = a / b
    else:
        response["error"] = f"Unsupported operation '{op}'"
        response["code"] = 400
        print(f"Client: {client_ip}\nOperation: {op}\na: {a}\nb: {b}\nError: Unsupported operation\nCode: 400\n" + "-"*30)
        return response

    response["result"] = res
    response["code"] = 200

    print(f"Client: {client_ip}")
    print(f"Operation: {op}")
    print(f"a: {a}")
    print(f"b: {b}")
    print(f"Result: {res}")
    print(f"Code: 200")
    print("-" * 30)
    return response

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((HOST, PORT))
server_socket.listen(5)

print(f"Calculator server running on {HOST}:{PORT}")

while True:
    conn, addr = server_socket.accept()
    client_ip = addr[0]
    try:
        data = conn.recv(1024).decode('utf-8')
        if data:
            res = handle_request(data, client_ip)
            conn.send(json.dumps(res).encode('utf-8'))
    except Exception as e:
        err_res = {"result": None, "error": str(e), "code": 500}
        conn.send(json.dumps(err_res).encode('utf-8'))
    finally:
        conn.close()