import grpc
import numbers_pb2
import numbers_pb2_grpc
import random
import time
import argparse
from datetime import datetime
import ssl

# List of random client names
client_names = ["Alice", "Bob", "Charlie", "David", "Eve", "Frank", "Grace", "Hannah", "Ivy", "Jack"]

def log_message(message):
    # Get the current time and format it as "YYYY-MM-DD HH:MM:SS"
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"{timestamp} - {message}")

def run(host, port, ca_cert=None, tls_enabled=False):
    # Choose a random name for the client (this remains constant)
    client_id = random.choice(client_names)  # Choose a random name
    log_message(f"Client started with name: {client_id}")

    while True:
        try:
            # TLS configuration, only if tls_enabled is True
            if tls_enabled:
                credentials = grpc.ssl_channel_credentials(
                    root_certificates=open(ca_cert, 'rb').read()  # The CA certificate for server verification
                )
                channel = grpc.secure_channel(f'{host}:{port}', credentials)
            else:
                # Insecure connection
                channel = grpc.insecure_channel(f'{host}:{port}')

            stub = numbers_pb2_grpc.NumberServiceStub(channel)

            # Run an infinite loop to continuously send numbers
            while True:
                # Generate a random number between 1 and 6
                number = random.randint(1, 6)
                log_message(f"Client {client_id} sending number: {number}")

                # Call the SendNumber method and receive the response
                try:
                    response = stub.SendNumber(numbers_pb2.NumberRequest(number=number, client_id=client_id))
                    log_message(f"Client {client_id} received number: {response.number} from server")
                except grpc.RpcError as e:
                    log_message(f"Error while communicating with the server: {e}")
                    time.sleep(5)
                    break  # Stop the current communication if an error occurs

                # Wait a short time before sending another number
                time.sleep(1)

        except grpc.RpcError as e:
            log_message(f"Error connecting to the server: {e}")
            log_message("Retrying connection in 5 seconds...")
            time.sleep(5)  # Wait 5 seconds before retrying

if __name__ == '__main__':
    # Argument parsing for host, port number, CA certificate, and TLS enabling
    parser = argparse.ArgumentParser(description="Start the gRPC client and connect to the server on a given host and port")
    parser.add_argument('--host', type=str, default='localhost', help="The server address")
    parser.add_argument('--port', type=int, default=50051, help="The server port number")
    parser.add_argument('--ca-cert', type=str, help="Path to the server's CA certificate (only for TLS)")
    parser.add_argument('--tls', action='store_true', help="Use TLS for the connection")
    args = parser.parse_args()

    # Start the client with the provided host, port number, CA certificate, and TLS enabling
    run(args.host, args.port, ca_cert=args.ca_cert, tls_enabled=args.tls)
