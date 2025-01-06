import grpc
from concurrent import futures
import time
import random
import numbers_pb2
import numbers_pb2_grpc
from datetime import datetime
import ssl
import argparse

class NumberServiceServicer(numbers_pb2_grpc.NumberServiceServicer):
    def SendNumber(self, request, context):
        # Generate a random number between 1 and 6
        number = random.randint(1, 6)
        log_message(f"{request.client_id}: {request.number} --> server: {number}")
        return numbers_pb2.NumberResponse(number=number, client_id=request.client_id)

def log_message(message):
    # Get the current time and format it as "YYYY-MM-DD HH:MM:SS"
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"{timestamp} - {message}")

def serve(cert_file=None, key_file=None, port=50051, tls_enabled=False):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    numbers_pb2_grpc.add_NumberServiceServicer_to_server(NumberServiceServicer(), server)

    if tls_enabled:
        # TLS configuration
        if cert_file and key_file:
            server_credentials = grpc.ssl_server_credentials(
                [(open(key_file, 'rb').read(), open(cert_file, 'rb').read())]
            )
            server.add_secure_port(f'[::]:{port}', server_credentials)
            log_message(f"Server started on port {port} with TLS...")
        else:
            log_message("TLS is enabled, but certificate or key is missing.")
            return
    else:
        # Insecure connection
        server.add_insecure_port(f'[::]:{port}')
        log_message(f"Server started on port {port} without TLS...")

    server.start()
    try:
        while True:
            time.sleep(86400)  # Keep the server running
    except KeyboardInterrupt:
        server.stop(0)

if __name__ == '__main__':
    # Argument parsing for certificate files, port number, and TLS enabling
    parser = argparse.ArgumentParser(description="Start the gRPC server on a given port")
    parser.add_argument('--cert', type=str, help="Path to the server certificate (only for TLS)")
    parser.add_argument('--key', type=str, help="Path to the server private key (only for TLS)")
    parser.add_argument('--port', type=int, default=50051, help="Port number for the server to run on")
    parser.add_argument('--tls', action='store_true', help="Use TLS for the connection")
    args = parser.parse_args()

    # Start the server with the provided port number, certificate, and TLS enabling
    serve(cert_file=args.cert, key_file=args.key, port=args.port, tls_enabled=args.tls)
