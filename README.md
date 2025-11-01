# cwenum

![cwenum crate logo](https://raw.githubusercontent.com/Weichwerke-Heidrich-Software/cwenum/refs/heads/main/img/logo.svg)

A tiny crate to access a strongly typed common weakness enumeration (cwe) object. Everything is ready to use at compile time, no further setup or network calls at runtime are required.

# Usage

Include something along the lines of
```toml
cwenum = { version = "1.0", features = ["std", "iterable", "str", "serde"] }
```
in your `Cargo.toml`. You now have access to the `cwenum::Cwe` enum.

Available feature flags:
* `std`: Link against the standard library. Enabled by default. Omit this and compile without default features if you are building `no_std` applications.
* `iterable`: Offers `Cwe::iterator()`, which can be used to loop through all CWEs.
* `str`: Offers some conversion functionality to and from `&str`. Roughly doubles artifact size to about 1.5 MB.
* `serde`: Implements `Deserialize` and `Serialize` for `Cwe`. Requires the `std` and `str` flags.

# Example

```rs
use cwenum::Cwe;

let cwe = Cwe::Cwe89;
// The enum is copyable...
let _cwe_copy = cwe;
// ...comparable...
assert_eq!(cwe, Cwe::Cwe89);
// ...and hashable.
let mut map = std::collections::HashMap::new();
map.insert(cwe, "I like this CWE best!");

// If the crate is compiled with the `str` feature, it offers more functionality:
println!("{}", cwe.id());
println!("{}", cwe.name());
println!("{}", cwe.description());
let cwe_79: Cwe = "CWE-79".try_into().unwrap();
assert_eq!(cwe_79, Cwe::Cwe79);
// If the `std` feature flag is left active, the conversion is not case sensitive:
let cwe_80: Cwe = "cwe-80".try_into().unwrap();
assert_eq!(cwe_80, Cwe::Cwe80);

// If the crate is compiled with the `iterable` feature, the enum offers an iterator:
for cwe in Cwe::iterator().take(3) {
    println!("{}", cwe.id())
}

// With the `serde` feature, CWEs can be (de)serialized:
let serialized = serde_json::to_string(&Cwe::Cwe89).unwrap();
assert_eq!(serialized, "CWE-89");
let deserialized: Cwe = serde_json::from_str("CWE-90").unwrap();
assert_eq!(deserialized, Cwe::Cwe90);
```

## License

This software is distributed under the [MIT](https://choosealicense.com/licenses/mit/) license. In a nutshell this means that all code is made public, and you are free to use it without any charge.
