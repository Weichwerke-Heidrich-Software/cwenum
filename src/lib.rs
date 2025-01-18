#![warn(missing_docs)]
#![warn(clippy::unwrap_used)]
#![cfg_attr(not(feature = "std"), no_std)] // Enable `no_std` when the `std` feature is disabled
#![no_std]
#![doc = include_str!("../README.md")]

mod cwe;

pub use cwe::*;
