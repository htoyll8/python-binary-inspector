import os 
import subprocess
import PyInstaller.__main__

def compile_script(script_path):
    """
    Compile a script into a standalone executable using PyInstaller.

    Args:
        script_path (str): The path to the script file.

    Returns:
         str: The path to the compiled binary file.
    """
    PyInstaller.__main__.run([
        script_path,
        '--onefile',
        '--windowed'
    ])

    # Exract the base name of the script file and remove the .py extension
    script_base_name = os.path.basename(script_path).rsplit('.', 1)[0]

    # Construct the path to the compiled binary file 
    binary_path = os.path.join(os.path.dirname(script_path), 'dist', script_base_name)

    if os.path.isfile(binary_path): 
        return binary_path
    else: 
        raise FileNotFoundError("Compiled binary not found at expected path: {}".format(binary_path))

def create_binary_file():
    """
    Creates a binary file named 'test.py' and writes the string "print('Hello World!')" to it.

    Returns:
        str: The path to the created 'test.py' file.

    Raises:
        FileNotFoundError: If the directory of the current script cannot be found.
        IOError: If there is an error writing to the file.
    """
    # Get the directory of the current script
    current_script_dir = os.path.dirname(os.path.abspath(__file__))

    # Create the 'test.py' file in the same directory as the current script
    test_py_path = os.path.join(current_script_dir, 'test.py')

    # Write the string "print('Hello World!')" to the 'test.py' file
    try:
        with open(test_py_path, 'w') as file:
            file.write("print('Hello World!')")
    except IOError as e:
        raise IOError("Error writing to file: {}".format(e))

    # Compile the 'test.py' script and return the compiled script object
    return compile_script('test.py')

# Use the strings command to extract readable ASCII strings from the binary
def extract_strings_from_binary(file_path):
    try: 
        result = subprocess.check_output(['strings', file_path])
        return result.decode('utf-8')
    except Exception as e:
        raise f"Error extracting strings from binary: {e}"

def run_objdump(binary_path):
    """
    Runs objdump on a binary file and returns the output.

    Args:
        binary_path (str): The path to the binary file.

    Returns:
        str: The output of objdump.
    """
    command = ['objdump', '-d', binary_path]

    # Run the command and store the output
    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    if result.returncode != 0:
        raise Exception("Error running objdump: {}".format(result.stderr))

    return result.stdout

def main(): 
    file_path = create_binary_file()
    print(extract_strings_from_binary(file_path))
    print(run_objdump(file_path))

if __name__ == '__main__':
    main()