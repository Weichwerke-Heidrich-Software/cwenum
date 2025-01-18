#!/bin/bash

print_filesize() {
  size=$(ls -ahl target/release/libcwenum.rlib | awk '{print $5}')
  echo "Filesize: $size"
}

echo Building without features
cargo build --release > /dev/null 2>&1
print_filesize

echo Building with iterable feature
cargo build --release --features "iterable" > /dev/null 2>&1
print_filesize

echo Building with serde feature
cargo build --release --features "serde" > /dev/null 2>&1
print_filesize

echo Building with str feature
cargo build --release --features "str" > /dev/null 2>&1
print_filesize

echo Building with all features
cargo build --release --all-features > /dev/null 2>&1
print_filesize

cargo test --all-features
