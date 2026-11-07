# Python Log File Analyzer

A small command-line log analyzer made with Python's standard library. It counts
common log levels, reports total lines, and shows the most frequent messages.

## Run

```bash
python log_analyzer.py path/to/app.log
```

Choose how many repeated messages to show:

```bash
python log_analyzer.py app.log --top 10
```

Lines without a recognized `CRITICAL`, `ERROR`, `WARNING`, `WARN`, `INFO`, or
`DEBUG` level are counted as `OTHER`. No third-party packages are needed.

## Project QR Code

Scan to open this GitHub repository:

![QR code linking to this repository](qr-code.png)
