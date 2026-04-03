import gradio as gr

from ai_ready_data.parse import parse
from ai_ready_data.constants import DataManagementMode


def run_pipeline(mode: str) -> str:
    parse(mode=DataManagementMode[mode])
    return f"Pipeline complete (mode: {mode})"


def search(query: str) -> str:
    # stub — wire up search logic here
    return f"Search not yet implemented (query: {query!r})"


mode_choices = [m.value for m in DataManagementMode]

with gr.Blocks() as demo:
    gr.Markdown("## AI-Ready Data")

    with gr.Tab("Process"):
        mode_dropdown = gr.Dropdown(choices=mode_choices, value=mode_choices[0], label="DataManagementMode")
        run_button = gr.Button("Run pipeline")
        pipeline_output = gr.Textbox(label="Output", interactive=False)
        run_button.click(fn=run_pipeline, inputs=mode_dropdown, outputs=pipeline_output)

    with gr.Tab("Search"):
        search_input = gr.Textbox(label="Query")
        search_button = gr.Button("Search")
        search_output = gr.Textbox(label="Results", interactive=False)
        search_button.click(fn=search, inputs=search_input, outputs=search_output)


if __name__ == "__main__":
    demo.launch()
