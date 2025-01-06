```markdown
# gRPC Server and Client with TLS and mTLS Support

This project implements a gRPC server and client that supports **insecure**, **TLS**, and **mTLS** (mutual TLS) connections. The server provides a simple service that returns a random number when a client sends a request.

## Contents
- [Installation](#installation)
- [Server Configuration](#server-configuration)
- [Client Configuration](#client-configuration)
- [Example Usage](#example-usage)
- [License](#license)

## Installation

1. Clone the repository

2. Install the required Python packages:
   ```bash
   pip install -r requirements.txt
   ```

3. Generate the required certificates (if needed):
   - Use OpenSSL to generate the server certificate, client certificate, and CA certificate (see the "Certificate Generation" section).

## Server Configuration

The server supports three types of connections:
- **Insecure connection** (no TLS).
- **TLS** (Transport Layer Security) for encrypted connections.
- **mTLS** (mutual TLS) where both the server and client are verified using certificates.

### Start the Server without TLS

Start the server without TLS (insecure connection):
```bash
python server.py --port 50051
```

### Start the Server with TLS

Start the server with only TLS (server certificate is required, client does not need a certificate):
```bash
python server.py --port 50051 --cert server.crt --key server.key --tls
```

### Start the Server with mTLS

Start the server with mTLS (both server and client certificates are required):
```bash
python server.py --port 50051 --cert server.crt --key server.key --ca-cert ca.crt --tls --m-tls
```

## Client Configuration

The client can connect to the server using any of the three connection types: insecure, TLS, or mTLS.

### Run the Client without TLS

Start the client without TLS:
```bash
python client.py --host <server_host> --port 50051
```

### Run the Client with TLS

Start the client with TLS (only the CA certificate is required to verify the server's certificate):
```bash
python client.py --host <server_host> --port 50051 --ca-cert ca.crt --tls
```

### Run the Client with mTLS

Start the client with mTLS (both client certificate and CA certificate are required):
```bash
python client.py --host <server_host> --port 50051 --ca-cert ca.crt --client-cert client.crt --client-key client.key --tls --m-tls
```

## Example Usage

### Server (TLS Enabled):
```bash
python server.py --cert server.crt --key server.key --port 50051 --tls
```

### Client (mTLS Enabled):
```bash
python client.py --host localhost --port 50051 --ca-cert ca.crt --client-cert client.crt --client-key client.key --tls --m-tls
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
```
