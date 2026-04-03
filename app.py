import sys
import gradio as gr

# Path hack to appease gradio builds and keep src/ layout
sys.path.insert(0, 'src')

from ai_ready_data.parse import parse
from ai_ready_data.constants import DataManagementMode
from ai_ready_data.answer import get_answer


def run_pipeline(mode: str) -> str:
    parse(mode=DataManagementMode[mode])
    return f"Pipeline complete (mode: {mode})"


def ask(query: str, answering_mode: str) -> str:
    answer = get_answer(query)
    return answer


mode_choices = [m.value for m in DataManagementMode]
answering_modes = ["no data", "basic", "advanced"]

with gr.Blocks() as demo:
    gr.Markdown("## AI-Ready Data")

    gr.Markdown("### 1. Process data")
    mode_dropdown = gr.Dropdown(choices=mode_choices, value=mode_choices[0], label="Pipeline mode")
    run_button = gr.Button("Run pipeline")
    pipeline_output = gr.Textbox(label="Output", interactive=False)
    run_button.click(fn=run_pipeline, inputs=mode_dropdown, outputs=pipeline_output)

    gr.Markdown("### 2. Ask a question")
    answering_mode_radio = gr.Radio(choices=answering_modes, value="no data", label="Data made available to LLM")
    ask_input = gr.Textbox(label="Query")
    ask_button = gr.Button("Ask")
    ask_output = gr.Textbox(label="Answer", interactive=False)
    ask_button.click(fn=ask, inputs=[ask_input, answering_mode_radio], outputs=ask_output)


if __name__ == "__main__":
    demo.launch()
