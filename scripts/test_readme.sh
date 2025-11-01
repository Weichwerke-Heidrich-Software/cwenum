#!/bin/bash
set -e

repo_root=$(git rev-parse --show-toplevel)

mapfile -t matches < <(grep -n '^```' "$repo_root/README.md")
toml_include_start_line_number=${matches[0]%%:*}
toml_include_end_line_number=${matches[1]%%:*}
rust_code_start_line_number=${matches[2]%%:*}
rust_code_end_line_number=${matches[3]%%:*}

fence_line=$(sed -n "${rust_code_start_line_number}p" "$repo_root/README.md")
if [[ "${fence_line}" != *rs ]]; then
    echo "Assertion failed: line ${rust_code_start_line_number} does not end with 'rs': ${fence_line}" >&2
    exit 1
fi

toml_code=$(sed -n "$((toml_include_start_line_number + 1)),$((toml_include_end_line_number - 1))p" "$repo_root/README.md")
test_code=$(sed -n "$((rust_code_start_line_number + 1)),$((rust_code_end_line_number - 1))p" "$repo_root/README.md")

echo "$toml_code"

tmp_repo=$(mktemp -d)
cd "$tmp_repo"

cargo init --name readme_test --bin

echo "$toml_code" >> Cargo.toml
echo "serde_json = \"*\"" >> Cargo.toml

echo "fn main() {" > src/main.rs
echo "$test_code" >> src/main.rs
echo "}" >> src/main.rs

cargo check
cargo clippy -- -D warnings

rm -rf "$tmp_repo"
