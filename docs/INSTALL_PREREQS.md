# Install Prerequisites

Use this before running QCHI on a new machine.

## Required
- git
- python3
- LyX

## Recommended
- Rust toolchain (`rustc`, `cargo`) for local `qchi-lint` runs

## Ubuntu / Debian
```bash
sudo apt update
sudo apt install -y git python3 lyx curl build-essential pkg-config
curl https://sh.rustup.rs -sSf | sh -s -- -y
source "$HOME/.cargo/env"
```

## macOS (Homebrew)
```bash
brew update
brew install git python lyx rust
```

## Verify
From repo root
```bash
bash tools/check_env.sh
```

## Notes
- If Rust is missing, local lint build is skipped but CI can still run it.
- Direct LyX workflow requires `lyx` installed on the machine running the task.
