#!/usr/bin/env bash
set -euo pipefail

echo "[1/6] Install system packages"
sudo apt update
sudo apt install -y git python3 python3-pip lyx curl build-essential pkg-config ca-certificates

echo "[2/6] Install Rust toolchain (cargo/rustc) if missing"
if ! command -v cargo >/dev/null 2>&1; then
  curl https://sh.rustup.rs -sSf | sh -s -- -y
fi
source "$HOME/.cargo/env" || true

echo "[3/6] Clone or update QCHI repo"
if [[ ! -d "$HOME/QCHI/.git" ]]; then
  git clone git@github.com:qchi2023/QCHI.git "$HOME/QCHI"
else
  git -C "$HOME/QCHI" pull --ff-only
fi

cd "$HOME/QCHI"

echo "[4/6] Run environment check"
bash tools/check_env.sh || true

echo "[5/6] Run project learning layout validator"
python3 tools/validate_project_learning.py

echo "[6/6] Build qchi-lint (optional but recommended)"
if command -v cargo >/dev/null 2>&1; then
  cargo build --manifest-path tools/qchi-lint/Cargo.toml --release
fi

cat <<'EOF'

Bootstrap complete.

Next in OpenCode:
1) Load skills/qchi/SKILL.md as core instruction context.
2) Load skills/qchi/adapters/opencode.md for host-specific behavior.
3) Keep learning logs under skills/qchi/learning/projects/<project-id>/.

EOF
