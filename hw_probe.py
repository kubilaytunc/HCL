import subprocess

def getProbe():
    try:
        result = subprocess.run(['/usr/bin/hw-probe', '--all'], check=True, text=True, capture_output=True)
        print("Command Output:", result.stdout)  # Output of the command
        print("Command Error (if any):", result.stderr)  # Errors, if any
    except subprocess.CalledProcessError as e:
        print(f"Error occurred: {e}")

