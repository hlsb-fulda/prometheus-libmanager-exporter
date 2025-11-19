# Prometheus exporter for LibManager
A prometheus exporter to scrape the failure state from LibManager by mk Solutions.

The exporter scrapes the LibManager dashboard and exposes metrics for the failure state of stations.

## Usage
```shell
uv run prometheus-libmanager-exporter
```

## Options and settings
- `<URL>` - The URL of the LibManager installation (i.e. `https://example.com/libmanager/`)
- `--username <USERNAME>` - The username to authenticate with
- `--password <PASSWORD>` - The password to authenticate with
- `--inscure` - Disables TLS verification
- `--port <PORT>` - The port to listen on (default: `10386`)`
