#!/bin/bash

cargo build --release
ls -ahl target/release/libcwenum.rlib
cargo build --release --features "str"
ls -ahl target/release/libcwenum.rlib

cargo test --all-features
