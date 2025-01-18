# cwenum

A tiny crate to access a strongly typed common weakness enumeration (cwe) object. Everything is ready to use at compile time, no further setup or network calls at runtime are required.

# Usage

Include
```toml
cwenum = { version = "1.0", default-features = false, features = [] }
```
in your Cargo.toml. You now have access to the `cwenum::Cwe` enum.

Feature flags:
* `iterable`: Offers `Cwe::iterator()`, which can be used to loop through all CWEs.
* `str`: Offers some conversion functionality to and from `&str`. Roughly doubles artifact size to about 1.5 MB.
* `serde`: Implements `Deserialize` and `Serialize` for `Cwe`, using the functions behind the `str` flag.

# Example

```rs
use cwenum::Cwe;

let cwe = Cwe::Cwe89;
// The enum is cloneable...
let _cwe_clone = cwe.clone();
// ...copyable...
let _cwe_copy = cwe;
// ...comparable...
assert_eq!(cwe, Cwe::Cwe89);
// ...and hashable.
let mut map = std::collections::HashMap::new();
map.insert(cwe, "CWE-89");

// If the crate is compiled with the `str` feature, it offers more functionality:
println!("{}", cwe.id());
println!("{}", cwe.name());
println!("{}", cwe.description());
let cwe_79: Cwe = "CWE-79".try_into().unwrap();
assert_eq!(cwe_79, Cwe::Cwe79);
// The conversion is not case sensitive
let cwe_80: Cwe = "cwe-80".try_into().unwrap();
assert_eq!(cwe_80, Cwe::Cwe80);

// If the crate is compiled with the `iterable` feature, the enum offers an iterator:
for cwe in Cwe::iterator().take(3) {
    println!("{}", cwe.id())
}
```

## License

This software is distributed under the [MIT](https://choosealicense.com/licenses/mit/) license. In a nutshell this means that all code is made public, and you are free to use it without any charge.
