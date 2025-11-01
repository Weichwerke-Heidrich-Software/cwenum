#!/bin/bash

set -e

print_filesize() {
  size=$(ls -ahl target/release/libcwenum.rlib | awk '{print $5}')
  echo "Filesize: $size"
}

echo
echo Building with default features
cargo build --release
print_filesize
echo
echo Building with iterable feature
cargo build --release --features "iterable"
print_filesize
echo
echo Building with serde feature
cargo build --release --features "serde"
print_filesize
echo
echo Building with str feature
cargo build --release --features "str"
print_filesize
echo
echo Building with all features
cargo build --release --all-features
print_filesize
echo
echo Building without std feature
cargo build --release --no-default-features
print_filesize
echo
echo Building with iterable without std feature
cargo build --release --no-default-features --features "iterable"
print_filesize
echo
echo Building with str without std feature
cargo build --release --no-default-features --features "str"
print_filesize

cargo test --all-features

cargo clippy --all-features

if [ "$(uname -s)" = "Linux" ]; then
  repo_root=$(git rev-parse --show-toplevel)
  "$repo_root/scripts/test_readme.sh"
fi
