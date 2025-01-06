---

# gRPC Client-Server Example with TLS Support

This repository provides a simple example of a gRPC client and server in Python, with support for TLS encryption. The server generates random numbers and sends them to the client, which continuously sends numbers and receives the server's response.

## Table of Contents
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Running the Server](#running-the-server)
- [Running the Client](#running-the-client)
- [Creating the CA and Server Certificates](#creating-the-ca-and-server-certificates)
- [Requirements](#requirements)

---

## Prerequisites

Before running the server and client, make sure you have the following installed:

- Python 3.6 or higher
- `pip` (Python package installer)

## Installation

1. Clone this repository:
   ```bash
   git clone <repository_url>
   cd <repository_directory>
   ```

2. Create and activate a virtual environment (optional but recommended):
   ```bash
   python3 -m venv venv
   source venv/bin/activate   # On Windows use `venv\Scripts\activate`
   ```

3. Install the dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Running the Server

The server listens for incoming gRPC requests and generates random numbers in response. You can run the server with or without TLS encryption.

### Running the Server without TLS:
To start the server without TLS (insecure connection):
```bash
python server.py --port 50051
```

### Running the Server with TLS:
To start the server with TLS, you must provide the certificate (`.crt`) and key (`.key`) files.

```bash
python server.py --port 50051 --cert server.crt --key server.key --tls
```

### Server Arguments:
- `--port`: The port number for the server to listen on. Default is `50051`.
- `--cert`: Path to the server certificate (only for TLS).
- `--key`: Path to the server private key (only for TLS).
- `--tls`: Enable TLS encryption for the server.

## Running the Client

The client connects to the server, sends a random number, and receives a response. Like the server, it can also use TLS encryption.

### Running the Client without TLS:
To start the client without TLS (insecure connection):
```bash
python client.py --host <server_host> --port 50051
```

### Running the Client with TLS:
To start the client with TLS, you must provide the CA certificate that the server uses for validation.

```bash
python client.py --host <server_host> --port 50051 --ca-cert ca.crt --tls
```

### Client Arguments:
- `--host`: The server address to connect to. Default is `localhost`.
- `--port`: The server port number. Default is `50051`.
- `--ca-cert`: Path to the CA certificate (only for TLS).
- `--tls`: Enable TLS encryption for the client.

## Creating the CA and Server Certificates

To run the server and client with TLS, you need a server certificate (`server.crt`), a server private key (`server.key`), and a CA certificate (`ca.crt`). You can generate these certificates using `openssl`.

### Step 1: Create a Certificate Authority (CA)
First, generate a private key and self-signed certificate for the CA:
```bash
# Generate the CA private key
openssl genpkey -algorithm RSA -out ca.key

# Generate the CA certificate (self-signed)
openssl req -x509 -new -nodes -key ca.key -sha256 -days 365 -out ca.crt
```

### Step 2: Create the Server Certificate
Next, generate the server's private key and certificate signed by the CA:

1. Generate the server's private key:
   ```bash
   openssl genpkey -algorithm RSA -out server.key
   ```

2. Create a certificate signing request (CSR) for the server:
   ```bash
   openssl req -new -key server.key -out server.csr
   ```

3. Sign the server CSR with the CA's private key to generate the server's certificate:
   ```bash
   openssl x509 -req -in server.csr -CA ca.crt -CAkey ca.key -CAcreateserial -out server.crt -days 365 -sha256
   ```

### Step 3: Verify the Certificates
You can verify the server certificate with the following command:
```bash
openssl verify -CAfile ca.crt server.crt
```

---

## Requirements

Here’s the `requirements.txt` that includes all the necessary dependencies:

```txt
grpcio==1.56.0
grpcio-tools==1.56.0
```

To install the dependencies, use:
```bash
pip install -r requirements.txt
```

---

## File Structure

```
.
├── ca.crt            # Certificate Authority Certificate
├── ca.key            # Certificate Authority Private Key
├── client.py         # gRPC Client
├── requirements.txt  # Dependencies for the project
├── server.py         # gRPC Server
├── server.crt        # Server Certificate (Signed by CA)
├── server.key        # Server Private Key
└── README.md         # Documentation
```

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

Let me know if you need any further changes or adjustments!