import subprocess
import os
import configparser

def get_blender_path():
    config = configparser.ConfigParser()
    config_path = os.path.join(os.path.dirname(__file__), "blender_path.ini")
    config.read(config_path)
    return config.get("Blender", "executable_path")

def open_stl_in_blender(file_paths):
    blender_path = get_blender_path()
    if not os.path.isfile(blender_path):
        print(f"Error: Blender executable not found at '{blender_path}'.")
        print("Please update the executable_path in the blender_path.ini file.")
        return

    python_script = ""
    with open(os.path.join(os.path.dirname(__file__), "blender_script.py"), "r") as f:
        python_script = f.read()

    python_script = python_script.replace("{file_paths}", str(file_paths))

    temp_script_path = "temp_import_script.py"
    try:
        with open(temp_script_path, "w") as f:
            f.write(python_script)

        cmd = [blender_path, "--python", temp_script_path]
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print(result.stdout)
        print(f"Blender has processed the STL files: {file_paths}")
    except subprocess.CalledProcessError as e:
        print(f"Error: Failed to open STL files in Blender. {e}")
        print(e.stdout)
        print(e.stderr)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    finally:
        if os.path.exists(temp_script_path):
            os.remove(temp_script_path)

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        open_stl_in_blender(sys.argv[1:])
    else:
        print("Please provide the paths to STL files as arguments.")