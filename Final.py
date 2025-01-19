import tkinter as tk
from tkinter import filedialog
import time
import subprocess
import os
#import ollama
from aider.coders import Coder
from aider.models import Model
from aider.io import InputOutput
from aider.commands import SwitchCoder

def select_folder():
    print("""=================================================================================
     _________ _______  _______  _______  _______  _______  _______ _________
     \__   __/(  ___  )(       )(  ____ \(  ____ )(  ___  )(  ___  )\__   __/
        ) (   | (   ) || () () || (    \/| (    )|| (   ) || (   ) |   ) (   
        | |   | (___) || || || || |      | (____)|| |   | || |   | |   | |   
        | |   |  ___  || |(_)| || | ____ |     __)| |   | || |   | |   | |   
        | |   | (   ) || |   | || | \_  )| (\ (   | |   | || |   | |   | |   
     ___) (___| )   ( || )   ( || (___) || ) \ \__| (___) || (___) |   | |   
     \_______/|/     \||/     \|(_______)|/   \__/(_______)(_______)   )_(   
=================================================================================

Hello, developer! 🚀  
This tool is designed to analyze your codebase, detect code smells, fix bugs,  
and provide you with clean, optimized code—all with minimal effort from you.  

Here's how it works:
1. Select a folder containing the codebase you want to analyze.  
2. Sit back while the tool scans and processes your files.  
3. Review changes and re-prompt the AI if needed.  

[INFO] A file selection window will open in 5 seconds.  
       Please select the root folder of your project or GitHub repository.  
       Ensure it contains the files you want analyzed.

(Press Ctrl+C to exit at any time.)

================================================================================
""")
    time.sleep(5)

    root = tk.Tk()
    root.withdraw() 

    folder_path = filedialog.askdirectory(title="Select a Folder")

    if folder_path:
        return folder_path
'''
def get_aider_prompt(pmd_file_path, pylint_file_path):
    if not isinstance(pmd_file_path, str) or not isinstance(pylint_file_path, str):
        return "Error: Both PMD and Pylint file paths must be valid strings."

    model = "llama3.2:latest"
    sys_prompt = """You are a precise static analysis assistant. Your job is to relay information from the analysis reports. Follow this format:

- File Path: [Path]
- Change: [Description of the change]
- Reason: [Explanation of why the change is needed]

Do not write any code directly. Do not skip or shorten any file paths at all. For example, for the following path:
"C:\\Users\\awais\\OneDrive\\Desktop\\Test\\project\\CCC\\DeltaHacks\\mysite\\app\\clean.py":13:0: C0301: Line too long (147/100) (line-too-long)
mention the location as "C:\\Users\\awais\\OneDrive\\Desktop\\Test\\project\\CCC\\DeltaHacks\\mysite\\app\\clean.py" and the line as 13.
Don't group changes that you think go together, suggest a change for every single line in the files given to you. Ensure you have the correct file extensions.
Do not assume all paths are Python files. Use the exact file paths provided in the report without alteration."""
    
    # Read the contents of the PMD and Pylint reports
    try:
        with open(pmd_file_path, 'r') as pmd_file:
            pmd_report = pmd_file.read()
    except FileNotFoundError:
        return f"Error: PMD report file '{pmd_file_path}' not found."
    except Exception as e:
        return f"Error reading PMD report file: {e}"

    try:
        with open(pylint_file_path, 'r') as pylint_file:
            pylint_report = pylint_file.read()
    except FileNotFoundError:
        return f"Error: Pylint report file '{pylint_file_path}' not found."
    except Exception as e:
        return f"Error reading Pylint report file: {e}"

    usr_prompt = f"Here are the reports:\nPMD Report:\n{pmd_report}\n\nPylint Report:\n{pylint_report}\nGenerate a prompt for Aider with all file paths and detailed suggestions. Aider is a code correction tool. Any prompt you give to Aider will be processed and used on the code."

    # Send the request to the model
    response = ollama.chat(model=model, messages=[{
        "role": "system",
        "content": sys_prompt
    }, {
        "role": "user",
        "content": usr_prompt
    }])

    aider_prompt = response.get('message', {}).get('content', 'No response from model.')

    return aider_prompt
'''
def write_errors_to_txt(line_generator, txt_path):
    try:
        with open(txt_path, 'w', encoding='utf-8') as f:
            for line in line_generator:
                f.write(line + '\n')
        print(f"Errors successfully written to {txt_path}")
    except Exception as e:
        print(f"Failed to write to text file: {e}")

def run_pylint_on_folder(folder_path):
    if not folder_path:
        print("No folder was selected. Exiting...")
        return

    print(f"Running pylint on the selected folder: {folder_path}")
    error_log_path = os.path.join(folder_path, "pylint_errors_f.txt")

    def pylint_errors():
        yield f"Pylint Errors for folder: {folder_path}\n"
        try:
            result = subprocess.run(['pylint', folder_path, '--disable=C0303', '--msg-template="{abspath}\t{line}:{column}:{msg}"'], capture_output=True, text=True)
            if result.stdout:
                for line in result.stdout.splitlines():
                    yield line
            if result.stderr:
                yield "STDERR:"
                for line in result.stderr.splitlines():
                    yield line
        except FileNotFoundError:
            yield "Pylint is not installed. Please install it with `pip install pylint`."
        except Exception as e:
            yield f"An error occurred: {e}"

    pe = pylint_errors()
    #write_errors_to_txt(pe, error_log_path)
    #print(list(pe))
    return list(pe)
    

def run_pmd(folder_path):
    pmd_dir = 'C:\\Users\\Matthew\\Downloads\\SAR\\SAR\\dist\\pmd-bin-7.9.0\\bin'
    command = [
        "pmd.bat", 
        "check", 
        "-d", folder_path, 
        "-f", "text", 
        "-R", "rulesets/java/quickstart.xml"
    ]
    error_log_path = os.path.join(folder_path, "pmd_errors_f.txt")

    def pmd_errors():
        yield f"PMD Errors for folder: {folder_path}\n"
        try:
            result = subprocess.run(command, capture_output=True, text=True, shell=True, cwd=pmd_dir)
            if result.stdout:
                for line in result.stdout.splitlines():
                    yield line
            if result.stderr:
                yield "STDERR:"
                for line in result.stderr.splitlines():
                    yield line
        except Exception as e:
            yield f"An error occurred: {e}"

    pe = pmd_errors()
    #write_errors_to_txt(pe, error_log_path)
    return list(pe)


def compile_and_run_all_code(folder_path):
    if not folder_path:
        print("No folder was selected. Exiting...")
        return

    # Recursively walk through the directory to find all files
    files_to_compile = []
    
    for dirpath, _, filenames in os.walk(folder_path):
        for filename in filenames:
            if filename.endswith(('.c', '.cpp', '.java', '.py')):
                files_to_compile.append(os.path.join(dirpath, filename))

    if not files_to_compile:
        print("No compilable source files found in the folder.")
        return

    print("Compiling and running the following files:")
    for file_path in files_to_compile:
        print(file_path)
        # Pass the file name (extracted from the path) as the second argument
        compile_and_run_code(folder_path, os.path.basename(file_path))

def compile_and_run_code(folder_path, code_file_name):
    if not folder_path:
        print("No folder was selected. Exiting...")
        return

    # Compile the source file (if it's C, C++, or Java)
    for root, dirs, files in os.walk(folder_path):
        if code_file_name in files:
            code_file_path = os.path.join(root, code_file_name)
            file_extension = os.path.splitext(code_file_name)[1]
            print(f'Int: {code_file_path}, {file_extension}')
            print(os.path.exists(code_file_path))  # This should now be True if the file exists
            if os.path.exists(code_file_path):
                print(f"Found the code file: {code_file_path}") 

    # Dr. Memory path
    drmemory_path = r"C:\Program Files (x86)\Dr. Memory\bin\drmemory.exe"

    if file_extension == '.c' or file_extension == '.cpp':
        # For C/C++ files: Use gcc/g++ to compile
        compiled_executable = os.path.splitext(code_file_name)[0]  # Remove file extension for executable name
        compile_command = f"gcc {code_file_path} -o {compiled_executable}" if file_extension == '.c' else f"g++ {code_file_path} -o {compiled_executable}"

        try:
            subprocess.run(compile_command, shell=True, check=True, cwd=folder_path)
            print(f"Compiled {code_file_name} successfully.")
            run_drmemory_on_executable(folder_path, compiled_executable)
        except subprocess.CalledProcessError as e:
            print(f"Error compiling {code_file_name}: {e}")

    elif file_extension == '.java':
        # For Java files: Use javac to compile and java to run
        compiled_class = os.path.splitext(code_file_name)[0]  # Remove file extension for class name
        compile_command = f"javac {code_file_path}"

        try:
            subprocess.run(compile_command, shell=True, check=True, cwd=folder_path)
            print(f"Compiled {code_file_name} successfully.")
            run_drmemory_on_java(folder_path, compiled_class)
        except subprocess.CalledProcessError as e:
            print(f"Error compiling {code_file_name}: {e}")

    elif file_extension == '.py':
        # For Python files: Directly run using python interpreter
        print(f"Running Python script {code_file_name} through Dr. Memory...")
        run_drmemory_on_python(folder_path, code_file_name)

def run_drmemory_on_executable(folder_path, compiled_executable):
    drmemory_path = r"C:\Program Files (x86)\Dr. Memory\bin\drmemory.exe"
    command = [drmemory_path, '--', os.path.join(folder_path, compiled_executable)]

    try:
        result = subprocess.run(command, capture_output=True, text=True)
        print("Dr. Memory Output:")
        print(result.stdout)
        if result.stderr:
            print("Error Output:")
            print(result.stderr)
    except Exception as e:
        print(f"Error running Dr. Memory on {compiled_executable}: {e}")

def run_drmemory_on_java(folder_path, compiled_class):
    drmemory_path = r"C:\Program Files (x86)\Dr. Memory\bin\drmemory.exe"
    command = [drmemory_path, '--', 'java', compiled_class]

    try:
        result = subprocess.run(command, capture_output=True, text=True, cwd=folder_path)
        print("Dr. Memory Output:")
        print(result.stdout)
        if result.stderr:
            print("Error Output:")
            print(result.stderr)
    except Exception as e:
        print(f"Error running Dr. Memory on {compiled_class}: {e}")

def run_drmemory_on_python(folder_path, python_file):
    drmemory_path = r"C:\Program Files (x86)\Dr. Memory\bin\drmemory.exe"
    command = [drmemory_path, '--', 'python', os.path.join(folder_path, python_file)]

    try:
        result = subprocess.run(command, capture_output=True, text=True)
        print("Dr. Memory Output:")
        print(result.stdout)
        if result.stderr:
            print("Error Output:")
            print(result.stderr)
    except Exception as e:
        print(f"Error running Dr. Memory on {python_file}: {e}")

def parse_instructions(report1, report2):
    #lines = report1.split("\n")
    instructions = {}
    for line in report1:
        if "\t" in line:
            temp = line.split("\t")
            fdir = ':'.join(temp[0].split(":")[:-2])
            if fdir not in instructions:
                instructions[fdir] = [' '.join(temp[1:])]
            else:
                instructions[fdir].append(' '.join(temp[1:]))
    
    #lines = report2.split("\n")
    #print(report2)
    for line in report2:
        #print(line)
        if '\t' in line:
            temp = line.split("\t")
            fdir = temp[0]
            if fdir not in instructions:
                instructions[fdir] = [temp[1]]
            else:
                instructions[fdir].append(temp[1])

    return instructions

def run_aider(bruh, fname, filepath, auto_continue=False):
    print(filepath)
    print("making change to", fname)
    os.chdir(filepath)
    model = Model("gemini/gemini-1.5-pro-latest")
    coder = Coder.create(main_model=model, fnames=[fname], io=InputOutput(yes=True))
    #coder.include_file(fname)
    try:
        coder.run(f"/code Fix the following issues. Make sure you do not change what the code does, just correct the bugs / code smells detected. You are not to create any additional files, only edit the file located at {fname}:\n{bruh}")
    except SwitchCoder:
        pass

    prompt = ""
    
    if not auto_continue:
        prompt = input("Continue prompting Groot (Enter /continue to continue to next file. Enter /auto to skip all future Groot prompts): ")
        while prompt.strip() == "":
            prompt = input("Please enter a valid response: ")
        while prompt != "/continue" and prompt != '/auto':
            try:
                coder.run(prompt)
            except SwitchCoder:
                pass
            prompt = input("Continue prompting Groot (Enter /continue to continue to next file. Enter /auto to skip all future Groot prompts): ")
            while prompt.strip() == "":
                prompt = input("Please enter a valid response: ")
    
    if prompt == "/auto" or auto_continue:
        return True
    return False

def prompt_git(path):
    try:
        # Navigate to the repo directory
        subprocess.run(["git", "-C", path, "add", "."], check=True)
        
        # Commit changes
        subprocess.run(["git", "-C", path, "commit", "-m", "Groot auto commit"], check=True)
        
        # Push to the remote repository
        subprocess.run(["git", "-C", path, "push"], check=True)
        
        print("Changes successfully committed and pushed.")
    
    except subprocess.CalledProcessError as e:
        print(f"Error during Git operation: {e}")


def main():
    selected_folder = select_folder()
    print(selected_folder)
    pmd_file_path = os.path.join(selected_folder, "pmd_errors_f.txt")
    pylint_file_path = os.path.join(selected_folder, "pylint_errors_f.txt")

    # Now you can use these paths
    #print(f"PMD file path: {pmd_file_path}")
    #print(f"Pylint file path: {pylint_file_path}")
    print("scanning files...")
    c = run_pylint_on_folder(selected_folder)
    #print(c)
    d = run_pmd(selected_folder)
    print("processing files...")
    instructions = parse_instructions(d, c)
    print("thinking...")

    #print(instructions)
    
    #print(f"Error logs have been saved in the folder: {selected_folder}")
    #print(get_aider_prompt(pmd_file_path, pylint_file_path))
    auto_continue = False
    for key in instructions:
        auto_continue = run_aider('\n'.join(instructions[key]), key, selected_folder, auto_continue)
    
    #compile_and_run_all_code(selected_folder)
    git = input("Would you like to push the changes to the repository? (y/n) ")
    if git.lower() == "y":
        prompt_git(selected_folder)

    input("\nPress Enter to exit...")  # Keeps the terminal open until the user presses Enter'''

if __name__ == "__main__":
    main()
