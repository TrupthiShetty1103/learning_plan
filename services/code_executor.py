import subprocess

def execute_user_code(code: str, test_input: str):
    try:
        completed = subprocess.run(
            ['python3', '-c', code],
            input=test_input.encode(),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=5
        )
        return {
            "output": completed.stdout.decode().strip(),
            "error": completed.stderr.decode().strip()
        }
    except Exception as e:
        return {"output": "", "error": str(e)}
