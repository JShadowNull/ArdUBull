# ArdUBull 🐂

MAVLink RC channel forwarder written in Rust. Listens for MAVLink RC_CHANNELS messages and forwards specific channels via UDP.

## Features

- ✅ Receives MAVLink RC_CHANNELS messages on UDP port 14551
- ✅ Extracts RC channels 9 and 10 (azimuth and elevation)
- ✅ Validates PWM values (1000-2000 μs range)
- ✅ Forwards as big-endian signed integers via UDP
- ✅ Single binary with no dependencies
- ✅ Fast, safe, and efficient Rust implementation

## Quick Start

### Download Pre-built Binary

```bash
# Download the latest release
wget https://github.com/JShadowNull/RC_to_PWM/releases/latest/download/ardubull-linux-x86_64

# Make it executable
chmod +x ardubull-linux-x86_64

# Run it
./ardubull-linux-x86_64
```

### Build from Source

```bash
# Clone the repository
git clone https://github.com/JShadowNull/RC_to_PWM.git
cd RC_to_PWM

# Build release binary
cargo build --release

# Run
./target/release/ardubull
```

## Configuration

Edit `src/main.rs` to customize:

```rust
// MAVLink input port
const MAVLINK_UDP_PORT: u16 = 14551;

// PWM output destination
const UDP_IP: &str = "192.168.1.14";
const UDP_PORT: u16 = 5050;

// RC channels to forward
const RC_CH_AZIMUTH: u8 = 9;
const RC_CH_ELEVATION: u8 = 10;

// Valid PWM range
const PWM_MIN: u16 = 1000;
const PWM_MAX: u16 = 2000;
```

## Running as a System Service

To run ArdUBull automatically on boot:

```bash
# 1. Edit the service file with your paths
nano ardubull.service
# Update YOUR_USERNAME and /path/to/ardubull

# 2. Copy service file to systemd
sudo cp ardubull.service /etc/systemd/system/

# 3. Enable and start the service
sudo systemctl daemon-reload
sudo systemctl enable ardubull
sudo systemctl start ardubull

# 4. Check status
sudo systemctl status ardubull

# 5. View logs
sudo journalctl -u ardubull -f
```

## Usage with ArduPilot SITL

```bash
# Start ArduPilot SITL with MAVProxy
sim_vehicle.py -v ArduCopter --out=127.0.0.1:14551

# In another terminal, run ArdUBull
./ardubull-linux-x86_64

# Set RC channels in MAVProxy
rc 9 1500
rc 10 1600
```

## UDP Packet Format

ArdUBull sends 8-byte packets in big-endian format:

```
[Azimuth PWM (4 bytes)][Elevation PWM (4 bytes)]
```

Both values are signed 32-bit integers representing PWM values in microseconds (1000-2000).