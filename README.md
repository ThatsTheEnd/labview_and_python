# LabVIEW and Python Integration Examples

This repository demonstrates various integration patterns between LabVIEW and Python, showcasing three different approaches for bidirectional communication and collaboration between the two environments.

## 🎯 Overview

The repository contains practical examples of three integration modes:

1. **LabVIEW calls Python** - LabVIEW acts as the orchestrator, invoking Python code
2. **Python calls LabVIEW** - Python scripts control and execute LabVIEW VIs
3. **Equal Partnership** - Both systems work together through message-based architectures (RabbitMQ, gRPC)

## 📁 Repository Structure

```
.
├── LabVIEWtoPython/          # LabVIEW calling Python examples
│   └── PythonNode/
├── PythonToLabVIEW/          # Python calling LabVIEW examples
│   ├── PYtoLV_DLL/
│   ├── PYtoLV_HTTP/
│   ├── PYtoLV_TCP/
│   └── PYtoLV_VI-Server/
├── gRPC/                     # gRPC-based integration (equal partnership)
│   ├── calculator_client/
│   ├── calculator_server/
│   ├── calculator.proto
│   ├── Client.py
│   └── Server.py
└── rabbitMQ/                 # RabbitMQ-based integration (equal partnership)
    ├── src/
    │   ├── analysis/
    │   ├── simulator/
    │   ├── ui/
    │   └── shared/
    └── tests/
```

## 🔧 Integration Modes

### 1. LabVIEW → Python

Examples demonstrating how LabVIEW can call Python code directly.

**Location:** [`LabVIEWtoPython/`](LabVIEWtoPython/)

**Features:**
- Python Node integration in LabVIEW
- Image processing examples (coin counting)
- Video processing capabilities
- Coin analysis using Python computer vision libraries

### 2. Python → LabVIEW

Multiple approaches for Python to control and execute LabVIEW VIs:

#### **VI Server (ActiveX)**
Control LabVIEW VIs programmatically using the VI Server API via ActiveX.

**Location:** [`PythonToLabVIEW/PYtoLV_VI-Server/`](PythonToLabVIEW/PYtoLV_VI-Server/)

**Features:**
- Call LabVIEW VIs from Python using `vi.Call()` and `vi.Call2()` methods
- Set/get control values on VIs
- Works with both LabVIEW Development System and built executables
- Supports connector pane parameters and loose controls

**Quick Start:**
```bash
cd PythonToLabVIEW/PYtoLV_VI-Server
uv run python Call-Method.py
# or
uv run python Call2-Method.py
```

See [PYtoLV_VI-Server/readme.md](PythonToLabVIEW/PYtoLV_VI-Server/readme.md) for details.

#### **HTTP/Web Services**
Call LabVIEW web services via HTTP requests.

**Location:** [`PythonToLabVIEW/PYtoLV_HTTP/`](PythonToLabVIEW/PYtoLV_HTTP/)

**Quick Start:**
1. Run LabVIEW as Administrator
2. Open the LabVIEW project and start the web service
3. Run:
```bash
cd PythonToLabVIEW/PYtoLV_HTTP
uv run python CallLVWebservice.py
```

See [PYtoLV_HTTP/readme.md](PythonToLabVIEW/PYtoLV_HTTP/readme.md) for details.

#### **TCP/UDP**
Network-based communication using TCP sockets.

**Location:** [`PythonToLabVIEW/PYtoLV_TCP/`](PythonToLabVIEW/PYtoLV_TCP/)

**Quick Start:**
1. Open LabVIEW Example Finder: Networking > TCP & UDP > Simple TCP.lvproj
2. Run Simple TCP - Server.vi
3. Run:
```bash
cd PythonToLabVIEW/PYtoLV_TCP
uv run python python-client.py
```

See [PYtoLV_TCP/README.md](PythonToLabVIEW/PYtoLV_TCP/README.md) for details.

#### **DLL**
Direct library calls using LabVIEW-built DLLs (Windows-specific).

**Location:** [`PythonToLabVIEW/PYtoLV_DLL/`](PythonToLabVIEW/PYtoLV_DLL/)

**Features:**
- Call LabVIEW functionality compiled as DLL
- Low-latency integration
- Python code: [`call_labview.py`](PythonToLabVIEW/PYtoLV_DLL/python/call_labview.py)

### 3. Partnership Mode

Both LabVIEW and Python work as equal partners, communicating through message-based architectures.

#### **gRPC Integration**

Remote procedure call framework for high-performance, language-agnostic communication.

**Location:** [`gRPC/`](gRPC/)

**Architecture:**
- Protocol Buffers definition: [`calculator.proto`](gRPC/calculator.proto)
- LabVIEW Server: [`calculator_server/`](gRPC/calculator_server/)
  - RPC service implementation
  - Message handlers for AddRequest/AddResponse
  - Server lifecycle management in `Run Service.vi`
- LabVIEW Client: [`calculator_client/`](gRPC/calculator_client/)
  - Client API for unary calls
  - Calculator Add operation for RPC calls
- Python implementations: [`Client.py`](gRPC/Client.py), [`Server.py`](gRPC/Server.py)

**Generated Code:**
- Python: [`calculator_pb2.py`](gRPC/calculator_pb2.py), [`calculator_pb2_grpc.py`](gRPC/calculator_pb2_grpc.py)
- LabVIEW: Message registration and RPC method bindings
- Protocol file: [`calculator.proto`](gRPC/calculator.proto)

**Quick Start:**
```bash
cd gRPC

# To run Python gRPC server:
uv run python Server.py

# In another terminal, run Python gRPC client:
uv run python Client.py
```

**Code Generation:**
```bash
# To regenerate Python stubs:
cd gRPC
uv run python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. calculator.proto
```

**Demo:**
Contains a [`Python demo/`](gRPC/Python%20demo/) folder with Python-only reference implementation.

#### **RabbitMQ Integration**

Full-featured demo showcasing asynchronous message-based communication with UI, simulator, and analysis modules.

**Location:** [`rabbitMQ/`](rabbitMQ/)

**Architecture:**
- **Exchange:** `demo.topic` (topic exchange)
- **Queues:**
  - `queue.lv` - Simulator/LabVIEW stub
  - `queue.analysis` - Analysis service
  - `queue.ui` - User interface
- **Message Flow:**
  - UI sends `cmd.start` → Simulator generates `meas.raw` → Analysis produces `meas.result` → UI displays results
  - Health scoring and fault detection
  - Status heartbeats from all services

**Modules:**
- **Simulator** ([`src/simulator/`](rabbitMQ/src/simulator/)) - Generates synthetic measurement data with optional fault injection
- **Analysis** ([`src/analysis/`](rabbitMQ/src/analysis/)) - FFT-based frequency analysis and health scoring
- **UI** ([`src/ui/`](rabbitMQ/src/ui/)) - NiceGUI web dashboard for control and visualization
- **Shared** ([`src/shared/`](rabbitMQ/src/shared/)) - Common RabbitMQ infrastructure and message contracts

**Quick Start:**

1. **Start RabbitMQ:**
   ```bash
   docker run -d --name rabbitmq -p 5672:5672 -p 15672:15672 rabbitmq:3-management
   ```

2. **Install Dependencies:**
   ```bash
   cd rabbitMQ
   uv sync --extra dev
   ```

3. **Run Demo:**
   ```bash
   # Option A: All modules at once
   uv run poe run-all
   
   # Option B: Individual modules (separate terminals)
   uv run poe run-simulator
   uv run poe run-analysis
   uv run poe run-ui
   ```

4. **Open Browser:** http://localhost:8080

**Features:**
- Real-time measurement flow visualization
- Fault injection toggle
- Health score monitoring with color coding
- Remote shutdown via message bus
- End-to-end correlation IDs for debugging
- Frequency spectrum analysis with peak detection

**Testing:**
```bash
uv run poe test        # Run pytest suite
uv run poe typecheck   # Type checking
```

See [`rabbitMQ/README.md`](rabbitMQ/README.md) for complete documentation.

## 🛠️ Requirements

### Python
- Python 3.11+
- Common libraries: `aio-pika`, `nicegui`, `numpy`, `plotly`, `grpcio`, `grpcio-tools`, `win32com` (Windows only)

### LabVIEW
- LabVIEW 2020 or later recommended
- gRPC support library ([gRPC LabVIEW](https://github.com/ni/grpc-labview))
- VI Server enabled for ActiveX examples
- Administrator rights for web service examples

### Services
- **RabbitMQ:** Docker or local installation
- **gRPC:** Protocol Buffers compiler for regenerating stubs
