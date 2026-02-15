# NI Days Demo

RabbitMQ demo with UI, simulator, and analysis modules showcasing LabVIEW-Python integration.

## Quick Start

### 1. Start RabbitMQ

Using Docker:
```bash
docker run -d --name rabbitmq -p 5672:5672 -p 15672:15672 rabbitmq:3-management
```

Or using Homebrew (macOS):
```bash
brew install rabbitmq
brew services start rabbitmq
```

### 2. Install Dependencies

```bash
uv sync --extra dev
```

### 3. Run the Demo

**Option A: Launch all modules at once**

```bash
uv run poe run-all
```

**Option B: Run modules separately** (in separate terminals)

```bash
# Terminal 1: Simulator (LabVIEW stub)
uv run poe run-simulator

# Terminal 2: Analysis
uv run poe run-analysis

# Terminal 3: UI (opens browser at http://localhost:8080)
uv run poe run-ui
```

Open http://localhost:8080 in your browser and click "Start Measurement" to begin the demo flow.

## Architecture

### Message Topology

**Exchange:** `demo.topic` (type: topic)

**Queues & Bindings:**
- `lv.queue` ← `cmd.*` (all commands)
- `analysis.queue` ← `meas.raw`, `cmd.shutdown`
- `ui.queue` ← `meas.raw`, `meas.result`, `status.*`, `cmd.shutdown`

**Routing Keys:**
- `cmd.start` – Start measurement with parameters
- `cmd.stop` – Stop current measurement
- `cmd.shutdown` – Graceful shutdown of module
- `meas.raw` – Raw time-series measurement data
- `meas.result` – FFT analysis results
- `status.heartbeat` – Module health (optional)

### Modules

1. **Simulator** (Python stub for LabVIEW)
   - Consumes `cmd.start`, `cmd.stop`, `cmd.shutdown`
   - Generates deterministic vibration signal with optional fault injection
   - Publishes `meas.raw`

2. **Analysis** (Python)
   - Consumes `meas.raw`, `cmd.shutdown`
   - Performs FFT, peak detection, health scoring
   - Publishes `meas.result`

3. **UI** (NiceGUI web dashboard)
   - Sends `cmd.start`, `cmd.stop`, `cmd.shutdown`
   - Displays raw data and analysis results
   - Web interface at http://localhost:8080

## Development

### TDD Workflow

Run tests after each module:
```bash
uv run poe test
```

Run type checker:
```bash
uv run poe typecheck
```

### Module Entrypoints


Or run all modules together:
```bash
uv run poe run-all
```

Press Ctrl+C to stop all modules when using `run-all`.
Run individual modules:
```bash
uv run poe run-simulator
uv run poe run-analysis
uv run poe run-ui
```

## Configuration

Set RabbitMQ URL via environment variable (default: `amqp://guest:guest@localhost/`):

```bash
export RABBITMQ_URL="amqp://user:pass@hostname:5672/"
```

## Demo Features

- **Fault Injection:** Toggle "Enable Fault" to inject a high-frequency burst
- **Real-time Flow:** Raw data and analysis results update automatically
- **Health Scoring:** Green (healthy) or red (fault detected) based on frequency spectrum
- **Remote Shutdown:** "Shutdown All" button stops all modules via RabbitMQ message
- **Correlation IDs:** End-to-end message tracing for debugging
