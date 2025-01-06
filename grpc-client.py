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

def run(host, port, ca_cert=None, cert_file=None, key_file=None, tls_enabled=False, m_tls_enabled=False):
    # Choose a random name for the client (this remains constant)
    client_id = random.choice(client_names)  # Choose a random name
    log_message(f"Client started with name: {client_id}")

    while True:
        try:
            # TLS or mTLS configuration, depending on the settings
            if tls_enabled:
                if m_tls_enabled:
                    # mTLS configuration: the client uses both a certificate and a private key
                    credentials = grpc.ssl_channel_credentials(
                        root_certificates=open(ca_cert, 'rb').read(),
                        private_key=open(key_file, 'rb').read(),
                        certificate_chain=open(cert_file, 'rb').read()
                    )
                else:
                    # TLS: the client verifies with the CA-certificate
                    credentials = grpc.ssl_channel_credentials(
                        root_certificates=open(ca_cert, 'rb').read()
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
    parser.add_argument('--ca-cert', type=str, help="Path to the server's CA certificate (only for TLS/mTLS)")
    parser.add_argument('--cert', type=str, help="Path to the client certificate (only for mTLS)")
    parser.add_argument('--key', type=str, help="Path to the client private key (only for mTLS)")
    parser.add_argument('--tls', action='store_true', help="Use TLS for the connection")
    parser.add_argument('--m-tls', action='store_true', help="Use mTLS for the connection")
    args = parser.parse_args()

    # Start the client with the provided host, port number, CA certificate, and TLS/mTLS enabling
    run(args.host, args.port, ca_cert=args.ca_cert, cert_file=args.cert, key_file=args.key, tls_enabled=args.tls, m_tls_enabled=args.m_tls)
