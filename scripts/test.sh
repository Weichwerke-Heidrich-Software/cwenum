#!/bin/bash

cargo build
ls -ahl target/debug/libcwenum.rlib
cargo build --features "str"
ls -ahl target/debug/libcwenum.rlib

cargo test --all-features
