import os
import requests
import shutil
import xml.etree.ElementTree as ET
import zipfile

url = 'https://cwe.mitre.org/data/xml/cwec_latest.xml.zip'
dir = "dev_data"
cwec_zip = os.path.join(dir, "cwec.zip")
cwec_xml = os.path.join(dir, "cwec.xml")

def download_cwec_zip(url):
    response = requests.get(url)
    with open(cwec_zip, 'wb') as file:
        file.write(response.content)

def extract_cwec_xml():
    with zipfile.ZipFile(cwec_zip, 'r') as zip_ref:
        temp_dir = os.path.join(dir, "temp")
        zip_ref.extractall(temp_dir)
        extracted_file = os.path.join(temp_dir, zip_ref.namelist()[0])
        shutil.move(extracted_file, cwec_xml)
        shutil.rmtree(temp_dir)

def assure_file():
    if not os.path.exists(dir):
        os.makedirs(dir)
    if not os.path.exists(cwec_zip):    
        download_cwec_zip(url)
    if not os.path.exists(cwec_xml):
        extract_cwec_xml()

def parse_cwec_xml():
    tree = ET.parse(cwec_xml)
    root = tree.getroot()
    cwe_list = []
    
    for weakness in root.findall('.//Weakness'):
        cwe_id = weakness.get('ID')
        cwe_name = weakness.get('Name')
        cwe_list.append({'ID': cwe_id, 'Name': cwe_name})
    
    return cwe_list

def main():
    assure_file()

    cwec = parse_cwec_xml()
    
    for cwe in cwec:
        print(f"CWE-{cwe['ID']}: {cwe['Name']}")

if __name__ == "__main__":
    main()
