import os
from unittest import result
from altair import Time
from dotenv import load_dotenv
from openai import OpenAI
import subprocess
import re
import time

load_dotenv(override=True)
api_key = os.getenv("KILOCODE_API_KEY")
base_url = "https://api.kilo.ai/api/gateway"


client = OpenAI(api_key=api_key, base_url=base_url)

SYSTEM_PROMPT = """You are a Python unit test generator.
Your task is to generate valid pytest unit tests for the provided Python source code.
Rules:
- Generate only the test code.
- Do not explain your answer.
- Do not reproduce, redefine, or modify any function or class from the source code.
- The source code is located in the Python module specified by the user. Import the required functions or classes from that module.
- Use pytest.
- Generate tests that can be executed directly with pytest.
- Cover normal cases, boundary cases, and important error cases when applicable.
- Test behavior that is directly implied by the source code.
- Do not invent requirements or behavior that are not supported by the source code.
- Use pytest.raises() when testing expected exceptions.
- Do not add `if __name__ == "__main__": pytest.main()`.
- Keep the tests clear, focused, and reasonably concise.
"""


def generate_tests(code, module_name, model):
    try:
        start = time.perf_counter()
        print("sending..")
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {
                    "role": "user",
                    "content": f"Generate unit tests for this Python code:\n\nmodule_name: {module_name}\ncode:{code}",
                },
            ],
        )
        end = time.perf_counter()
        print(f"received : {end - start}")
        content = response.choices[0].message.content

        if content is None:
            raise ValueError("The model returned an empty response.")

        return content

    except Exception as e:
        print(f"Model error: {e}")
        return None


def run_tests(test_file):
    result = subprocess.run(["pytest", test_file], capture_output=True, text=True)

    return result.stdout + result.stderr


def parse_test_result(output):
    passed = 0
    failed = 0

    passed_match = re.search(r"(\d+) passed", output)
    failed_match = re.search(r"(\d+) failed", output)

    if passed_match:
        passed = int(passed_match.group(1))

    if failed_match:
        failed = int(failed_match.group(1))

    total = passed + failed

    error = (
        passed == 0
        and failed == 0
        and (
            "ERROR" in output
            or "error during collection" in output
            or "Interrupted" in output
        )
    )
    return {"total": total, "passed": passed, "failed": failed, "error": error}


def clean_generated_code(content):
    if content.startswith("```python"):
        content = content[len("```python") :]

    if content.endswith("```"):
        content = content[:-3]

    return content.strip()


def generate_and_run(code, module_name, model):
    test = generate_tests(code, module_name, model)

    if test is None:
        return None, None, None

    test = clean_generated_code(test)

    test_file = f"test_{module_name}.py"

    with open(test_file, "w", encoding="utf-8") as f:
        f.write(test)

    result = run_tests(test_file)

    stats = parse_test_result(result)

    return test, result, stats

#script\terminal use for testing 
def main():
    model = "inclusionai/ling-3.0-flash-sante:free"

    code = """def divide(a, b):
        if b == 0:
            raise ValueError("Cannot divide by zero")
        return a / b

    def calculate_discount(price, discount):
        if price < 0 or discount < 0 or discount > 100:
            raise ValueError("Invalid input")
        return price * (1 - discount / 100)"""
    
    module_name = "calculator"

    test, result, stats = generate_and_run(code, module_name, model)

    if test is None:
        print("Test generation failed.")
    else:
        print(test)
        print(result)
        print(stats)


