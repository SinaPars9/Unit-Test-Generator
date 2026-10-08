# AI Unit Test Generator

An AI-powered Python tool that generates `pytest` unit tests from existing Python source code and automatically runs them to evaluate the generated tests.

The project uses LLMs to generate tests and `pytest` to verify whether those tests actually work against the provided source code.

## Features

* Generate Python unit tests using LLMs
* Supports multiple AI models
* Uses `pytest` for real test execution
* Detects passed, failed, and error states
* Shows generated tests and test results
* Simple Gradio interface
* Supports OpenAI-compatible APIs

## How It Works

```text
Python Source Code
        │
        ▼
   Selected LLM
        │
        ▼
 Generated Tests
        │
        ▼
      pytest
        │
        ▼
 Test Results & Statistics
```

The model is responsible for generating the tests, while `pytest` actually executes them. This allows the project to evaluate whether the generated tests are valid instead of simply trusting the model's output.

## Project Structure

```text
Unit-Test-Generator/
│
├── app.py
├── generate.py
├── examples/
│   ├── calculator.py
│   └── test_calculator.py
├── .gitignore
└── README.md
```

## Requirements

* Python 3.10+
* pytest
* Gradio
* OpenAI Python SDK
* python-dotenv

Install the dependencies:

```bash
pip install gradio pytest openai python-dotenv
```

## Configuration

The project uses the Kilo Code API through its OpenAI-compatible API.

Create a `.env` file in the project root:

```env
KILOCODE_API_KEY=your_api_key_here
```

Do not commit your `.env` file to GitHub.

## Running the Project

Run the Gradio application:

```bash
python app.py
```

Then open the local Gradio interface in your browser.

## Usage

1. Enter your Python source code.
2. Enter the module name.
3. Select an AI model.
4. Click **Generate & Run**.
5. The selected model generates `pytest` tests.
6. The generated tests are saved and executed automatically.
7. The interface displays:

   * Generated tests
   * Pytest output
   * Test statistics
   
**Important:** The specified module must actually exist and be importable. Providing only the module name is not sufficient.

## Example

The `examples/` directory contains a simple calculator example demonstrating the workflow.

Example source code:

```python
def divide(a, b):
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b
```

The AI generates tests for the functions and the project then executes those tests using `pytest`.

## Models

The project currently supports several models available through the Kilo Code API, including:

* NVIDIA Nemotron
* NVIDIA Nemotron Lightning
* InclusionAI Ling
* Cohere North Mini Code

The model can be selected directly from the Gradio interface.

## Learning Project

This project was built as part of my learning journey in **LLM Engineering and AI Engineering**, with a focus on:

* LLM APIs
* Prompt Engineering
* Code Generation
* Automated Testing
* Model Evaluation
* Gradio

The goal is not only to generate code with an LLM, but to verify the generated code through actual execution.
