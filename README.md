# asprom - Assault Profile Monitor

asprom is a network security compliance scanner that monitors Layer 4 firewall configurations. It allows you to define service profiles for your networks and automatically scans them using nmap to detect any deviations from the established baseline.

This tool helps ensure compliance with security standards such as PCI-DSS, BSI-Grundschutz, and ISO/IEC 27001.

## Quick Start with Docker

The easiest way to get started is using Docker, which includes all dependencies:

```bash
cp env.example .env
docker-compose up -d
```

Once running, access the GUI at [http://localhost:8080](http://localhost:8080).

## Getting Started

1. Navigate to the "Schedule" tab
2. Configure a scan target:
   - Enter a hostname, IP address, or IP range
   - Leave "port range" and "extra parameters" empty initially
3. Click "Add Job" to create the scan
4. Click the magnifying glass icon to execute the scan immediately
5. Wait for the scan completion notification

## Managing Alerts

After scanning, you'll find detected services under the "Alerts: Exposed" tab. For each alert, you can:

- Click the "star" icon to mark for mitigation
- Click the "approve" icon to accept it as part of your baseline (requires business justification)

Once you've processed alerts for all your IP ranges, your initial configuration is complete. asprom will now monitor these ranges and alert you to any new services that appear.

## Monitoring Integration

### Prometheus Metrics
Access metrics about open ports and baseline deviations at:
[http://localhost:5000/metrics](http://localhost:5000/metrics)

### Nagios Integration
Use `aspromNagiosCheck.py` as a standard Nagios plugin to receive active alerts. The plugin will return CRITICAL status when unauthorized services are detected.

