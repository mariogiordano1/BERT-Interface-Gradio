import gradio as gr
from utils import get_predictions, save_correction, get_first_key

"""
demo = gr.Interface(
    fn = get_predictions,
    inputs=gr.components.Textbox(label='Inserisci qui la tua frase!', placeholder="Scrivi qui la tua frase."),
    outputs=gr.components.Label(label="L'emozione predominante è:", num_top_classes=7),
    allow_flagging='never',
    title="Emotion Recognition 😄😟😡😧🤭😖😔"
)
"""

#uvicorn run:app --reload


with gr.Blocks(theme=gr.themes.Soft()) as demo:
        gr.Markdown(
            """
            <h1 style="text-align: center">Emotion Recognition 😄😟😡😧🤭😖😔</h1>
            """)
        inp = gr.Textbox(label='Inserisci qui la tua frase emotiva', placeholder="Scrivi qui la tua frase.")
        btn = gr.Button(value="Calcola")
        out=gr.components.Label(label="L'emozione predominante è:", num_top_classes=7)
        num = gr.State(value=0)
        btn.click(fn=get_predictions, inputs=inp, outputs=out)
        btn.click(fn=get_first_key, inputs=inp, outputs=num)
        gr.Markdown(
            """
            <h2>Pensi che l'emozione predetta non sia l'emozione corretta?</h1>
            """)
        gr.Markdown(
            """
            <h6>Se pensi che l'emozione riconosciuta dal sistema non sia quella corretta, seleziona qui quella che pensi sia adatta.</h6>
            """)
        #emo = gr.Textbox(label="Inserisci l'emozione corretta!", placeholder="Scrivi qui l'emozione.")
        emo = gr.Radio(["Gioia", "Tristezza", "Rabbia", "Paura", "Vergogna", "Disgusto", "Colpevolezza"],  label="Seleziona l'emozione adatta alla frase")
        btn2 = gr.Button(value="Salva")
        btn2.click(fn=save_correction, inputs=[inp,num,emo], outputs=None)



