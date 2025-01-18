import os
import requests
import shutil
import xml.etree.ElementTree as ET
import zipfile

URL = 'https://cwe.mitre.org/data/xml/cwec_latest.xml.zip'
DIR = "dev_data"
CWEC_ZIP = os.path.join(DIR, "cwec.zip")
CWEC_XML = os.path.join(DIR, "cwec.xml")
RUSTFILE = os.path.join("src", "cwe.rs")

FILE_TEMPLATE = """
// This code is generated by generate_code.py, do not modify it manually.

/// The Common Weakness Enumeration (CWE) is a list of software weaknesses maintained by MITRE.
/// 
/// # Example
///
/// ```
/// use cwenum::Cwe;
///
/// let cwe = Cwe::Cwe89;
/// // The enum is cloneable...
/// let _cwe_clone = cwe.clone();
/// // ...copyable...
/// let _cwe_copy = cwe;
/// // ...comparable...
/// assert_eq!(cwe, Cwe::Cwe89);
/// // ...and hashable.
/// let mut map = std::collections::HashMap::new();
/// map.insert(cwe, "CWE-89");
///
/// // If the crate is compiled with the `str` feature, it offers more functionality:
/// println!("{{}}", cwe.id());
/// println!("{{}}", cwe.name());
/// println!("{{}}", cwe.description());
/// let cwe_79: Cwe = "CWE-79".try_into().unwrap();
/// assert_eq!(cwe_79, Cwe::Cwe79);
/// // If the `std` feature flag is left active, the conversion is not case sensitive
/// let cwe_80: Cwe = "cwe-80".try_into().unwrap();
/// assert_eq!(cwe_80, Cwe::Cwe80);
///
/// // If the crate is compiled with the `iterable` feature, the enum offers an iterator:
/// for cwe in Cwe::iterator().take(3) {{
///     println!("{{}}", cwe.id())
/// }}
/// ```
#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash)]
pub enum Cwe {{
    {variants}
}}

#[cfg(any(feature = "str", test))]
pub(crate) mod str {{
    use super::*;

    #[cfg(feature = "std")]
    type TryFromError = String;
    #[cfg(not(feature = "std"))]
    type TryFromError = &'static str;

    impl Cwe {{
        /// Returns the CWE ID.
        ///
        /// # Example
        ///
        /// ```
        /// use cwenum::Cwe;
        ///
        /// let id = Cwe::Cwe89.id();
        /// assert_eq!(id, "CWE-89");
        /// ```
        pub fn id(&self) -> &'static str {{
            match self {{
                {str_ids}
            }}
        }}

        /// Returns the CWE name.
        ///
        /// # Example
        ///
        /// ```
        /// use cwenum::Cwe;
        ///
        /// let name = Cwe::Cwe89.name();
        /// assert_eq!(name, "Improper Neutralization of Special Elements used in an SQL Command ('SQL Injection')");
        /// ```
        pub fn name(&self) -> &'static str {{
            match self {{
                {str_names}
            }}
        }}

        /// Returns the (short) CWE description.
        ///
        /// # Example
        ///
        /// ```
        /// use cwenum::Cwe;
        ///
        /// let description = Cwe::Cwe87.description();
        /// assert_eq!(description, "The product does not neutralize or incorrectly neutralizes user-controlled input for alternate script syntax.");
        /// ```
        pub fn description(&self) -> &'static str {{
            match self {{
                {str_descriptions}
            }}
        }}

        fn try_from_str(value: &str) -> Result<Self, TryFromError> {{
            let result = match value {{
                {try_from_str}
                _ => Err(())
            }};
            if let Ok(cwe) = result {{
                return Ok(cwe);
            }}
            #[cfg(feature = "std")]
            return Err(format!("Unknown CWE: {{}}", value));
            #[cfg(not(feature = "std"))]
            return Err("Unknown CWE");
        }}

    }}

    impl TryFrom<&str> for Cwe {{
        #[cfg(feature = "std")]
        type Error = String;
        #[cfg(not(feature = "std"))]
        type Error = &'static str;
    
        fn try_from(value: &str) -> Result<Self, Self::Error> {{
            let result = Cwe::try_from_str(value);
            if let Ok(cwe) = result {{
                return Ok(cwe);
            }}
            #[cfg(feature = "std")]
            return Cwe::try_from_str(&value.to_uppercase());
            #[cfg(not(feature = "std"))]
            return result;
        }}
    }}
}}

#[cfg(any(feature = "iterable", test))]
pub(crate) mod iterable {{
    use super::*;

    impl Cwe {{
        /// Returns a sorted iterator over all CWE variants.
        ///
        /// # Example
        ///
        /// ```
        /// use cwenum::Cwe;
        ///
        /// let mut count = 0;
        /// for _ in Cwe::iterator() {{
        ///     count += 1;
        /// }}
        /// assert!(count > 500);
        /// ```
        pub fn iterator() -> impl Iterator<Item = Cwe> {{
            [
                {iter_variants}
            ].into_iter()
        }}
    }}
}}

#[cfg(any(feature = "serde", test))]
pub(crate) mod serde {{
    use serde_crate::{{Serialize, Serializer, Deserialize, Deserializer}};

    use super::*;

    impl Serialize for Cwe {{
        fn serialize<S>(&self, serializer: S) -> Result<S::Ok, S::Error>
        where
            S: Serializer,
        {{
            serializer.serialize_str(self.id())
        }}
    }}

    impl<'de> Deserialize<'de> for Cwe {{
        fn deserialize<D>(deserializer: D) -> Result<Self, D::Error>
        where
            D: Deserializer<'de>,
        {{
            let value = String::deserialize(deserializer)?;
            Cwe::try_from(value.as_str()).map_err(serde_crate::de::Error::custom)
        }}
    }}
}}

#[cfg(test)]
mod tests {{
    use super::*;

    #[test]
    fn serde_roundtrip() {{
        for cwe in Cwe::iterator() {{
            let serialized = serde_json::to_string(&cwe).unwrap();
            let deserialized: Cwe = serde_json::from_str(&serialized).unwrap();
            assert_eq!(cwe, deserialized);
        }}
    }}
}}
"""

VARIANT_TEMPLATE = """
    /// ### {name}
    ///
    /// {description}
    Cwe{id},
"""

def download_cwec_zip(url):
    response = requests.get(url)
    with open(CWEC_ZIP, 'wb') as file:
        file.write(response.content)

def extract_cwec_xml():
    with zipfile.ZipFile(CWEC_ZIP, 'r') as zip_ref:
        temp_dir = os.path.join(DIR, "temp")
        zip_ref.extractall(temp_dir)
        extracted_file = os.path.join(temp_dir, zip_ref.namelist()[0])
        shutil.move(extracted_file, CWEC_XML)
        shutil.rmtree(temp_dir)

def assure_file():
    if not os.path.exists(DIR):
        os.makedirs(DIR)
    if not os.path.exists(CWEC_ZIP):    
        download_cwec_zip(URL)
    if not os.path.exists(CWEC_XML):
        extract_cwec_xml()

def parse_cwec_xml():
    tree = ET.parse(CWEC_XML)
    root = tree.getroot()
    cwec = []
    namespace = {'cwe': 'http://cwe.mitre.org/cwe-7'}
    
    for weakness in root.findall('.//cwe:Weakness', namespace):
        cwe_id = weakness.get('ID')
        cwe_name = weakness.get('Name')
        cwe_description = weakness.find('cwe:Description', namespace).text
        cwe_description = cwe_description.replace('\n', ' ').replace('\r', ' ').replace('\t', ' ')
        while '  ' in cwe_description:
            cwe_description = cwe_description.replace('  ', ' ')
        cwec.append({'ID': cwe_id,
                     'Name': cwe_name,
                     'Description': cwe_description})
    
    cwec.sort(key=lambda x: int(x['ID']))

    return cwec

def sanitize(string):
    return string.replace('\\', '\\\\').replace('"', '\\"')

def write_to_file(cwec):
    variants = []
    str_ids = []
    str_names = []
    str_descriptions = []
    try_from_str = []
    iter_variants = []
    for cwe in cwec:
        variants.append(VARIANT_TEMPLATE.format(id=cwe['ID'],
                                                name=cwe['Name'],
                                                description=cwe['Description']))
        str_ids.append(f"Cwe::Cwe{cwe['ID']} => \"CWE-{cwe['ID']}\",")
        sanitized_name = sanitize(cwe['Name'])
        str_names.append(f"Cwe::Cwe{cwe['ID']} => \"{sanitized_name}\",")
        sanitized_description = sanitize(cwe['Description'])
        str_descriptions.append(f"Cwe::Cwe{cwe['ID']} => \"{sanitized_description}\",")
        try_from_str.append(f"\"CWE-{cwe['ID']}\" => Ok(Cwe::Cwe{cwe['ID']}),")
        iter_variants.append(f"Cwe::Cwe{cwe['ID']},")



    with open(RUSTFILE, 'w') as file:
        file.write(FILE_TEMPLATE.format(variants="\n".join(variants),
                                        str_ids="\n".join(str_ids),
                                        str_names="\n".join(str_names),
                                        str_descriptions="\n".join(str_descriptions),
                                        try_from_str="\n".join(try_from_str),
                                        iter_variants="\n".join(iter_variants)))

def main():
    assure_file()
    cwec = parse_cwec_xml()
    write_to_file(cwec)

if __name__ == "__main__":
    main()
