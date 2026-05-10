import os
import xml.etree.ElementTree as ET
import subprocess

# Automatically uses the directory where the script is located
base_dir = os.path.dirname(os.path.abspath(__file__))
xml_file = os.path.join(base_dir, "coreutils.xml")
output_file = os.path.join(base_dir, "ollama_function_names.txt")

# Check if XML file exists or is there any error
if not os.path.exists(xml_file):
    print(f"ERROR: coreutils.xml not found in {base_dir}")
    print("Please place coreutils.xml in the same folder as this script.")
    exit()

print(f"Reading XML from: {xml_file}")

tree = ET.parse(xml_file)
root = tree.getroot()

ns = {'src': 'http://www.srcML.org/srcML/src'}

functions = root.findall('.//src:function/src:name', ns)
function_names = [f.text for f in functions if f.text]

print(f"Extracted {len(function_names)} function names from XML")

sample = function_names[:50]
prompt = f"Here are C function names from coreutils source code. These are from different files so duplicate names like main and usage are valid and intentional. Do not remove duplicates. List all these function names exactly as given, one per line:\n\n" + "\n".join(sample)

print("Sending sample to Ollama for verification...")

result = subprocess.run(
    ["ollama", "run", "llama3.2:3b", prompt],
    capture_output=True,
    text=True,
    timeout=120
)

print("Ollama Response:")
print(result.stdout)

if result.stderr:
    print("Errors:")
    print(result.stderr)

with open(output_file, 'w') as f:
    f.write("FUNCTION NAMES EXTRACTED FROM XML AND VERIFIED BY OLLAMA (Llama3.2 3b)\n")
    f.write("Tool: Ollama (llama3.2:3b)\n")
    f.write("="*50 + "\n\n")
    for func in function_names:
        f.write(func + "\n")
    f.write("\n" + "="*50 + "\n")
    f.write(f"Total Number of Functions: {len(function_names)}\n")

print(f"\nDone! Total functions found: {len(function_names)}")
print(f"Results saved to: {output_file}")