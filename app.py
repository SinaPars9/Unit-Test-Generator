import gradio as gr
from generate import generate_and_run

MODELS = [
    "nvidia/nemotron-3-ultra-550b-a55b:free",
    "nvidia/nemotron-3-super-120b-a12b:free",
    "nvidia/nemotron-3.5-lightning:free",
    "inclusionai/ling-3.1-flash",
    "inclusionai/ling-3.0-flash-sante:free",
    "cohere/north-mini-code:free",
]


def run_generator(code, module_name, model):
    test, result, stats = generate_and_run(code, module_name, model)

    if test is None:
        return "Test generation failed.", "", {}

    return test, result, stats


with gr.Blocks() as demo:

    gr.Markdown("## AI Unit Test Generator")

    # Input section
    with gr.Row():

        with gr.Column(scale=3):
            code_input = gr.Code(
                label="Python Source Code", language="python", lines=10
            )

        with gr.Column(scale=1):
            module_input = gr.Textbox(
                label="Module Name", placeholder="e.g. calculator"
            )

            model_input = gr.Dropdown(choices=MODELS, label="Model", value=MODELS[0])

    generate_button = gr.Button("Generate & Run", variant="primary")

    # Generated tests
    generated_tests = gr.Code(label="Generated Tests", language="python", lines=10)

    # Test result + statistics
    with gr.Row():

        with gr.Column(scale=3):
            test_result = gr.Textbox(label="Pytest Result", lines=6)

        with gr.Column(scale=1):
            stats_output = gr.JSON(label="Test Statistics")

    generate_button.click(
        fn=run_generator,
        inputs=[code_input, module_input, model_input],
        outputs=[generated_tests, test_result, stats_output],
    )


demo.launch()
