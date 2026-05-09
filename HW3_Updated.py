import os
import subprocess

src_path = r"C:\Users\puppa\Desktop\Shashank\Shashank\Shashank_Masters\UMBC\IS_698_2\coreutils-8.13\src"
output_file = r"C:\Users\puppa\Desktop\Shashank\Shashank\Shashank_Masters\UMBC\IS_698_2\ollama_functions_sample.txt"

# Sample of 20 representative .c files
sample_files = [
    'base64.c', 'basename.c', 'cat.c', 'chmod.c', 'chown.c',
    'cp.c', 'cut.c', 'date.c', 'df.c', 'du.c',
    'echo.c', 'head.c', 'ls.c', 'mkdir.c', 'mv.c',
    'pwd.c', 'rm.c', 'sort.c', 'tail.c', 'wc.c'
]

all_functions = []

print(f"Processing {len(sample_files)} sample files...")
print("="*50)

for i, c_file in enumerate(sample_files):
    file_path = os.path.join(src_path, c_file)

    if not os.path.exists(file_path):
        print(f"Skipping {c_file} - file not found")
        continue

    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
        code = f.read(5000)

    prompt = f"List ONLY the C function names defined in this code, one per line, no explanations, no numbers, no extra text:\n\n{code}"

    print(f"Processing {i+1}/{len(sample_files)}: {c_file}")

    result = subprocess.run(
        ["ollama", "run", "llama3.2:3b", prompt],
        capture_output=True,
        text=True,
        timeout=300
    )

    if result.returncode == 0 and result.stdout.strip():
        functions = [line.strip() for line in result.stdout.strip().split('\n')
                    if line.strip() and not line.strip().startswith('#')]
        for func in functions:
            all_functions.append(f"{c_file}: {func}")
        print(f"  Found {len(functions)} functions")
    else:
        print(f"  Skipped or error: {result.stderr.strip()}")

with open(output_file, 'w') as f:
    f.write("FUNCTION NAMES FOUND BY OLLAMA (llama3.2:3b)\n")
    f.write("Method: Sample of 20 raw .c files fed directly to Ollama\n")
    f.write("Note: Full coreutils has 130+ files. Sample used due to local hardware limitations.\n")
    f.write("="*50 + "\n\n")
    for func in all_functions:
        f.write(func + "\n")
    f.write("\n" + "="*50 + "\n")
    f.write(f"Total Number of Functions in Sample: {len(all_functions)}\n")
    f.write(f"Files Processed: {len(sample_files)}\n")

print(f"\nDone! Total functions found: {len(all_functions)}")
print(f"Results saved to: {output_file}")