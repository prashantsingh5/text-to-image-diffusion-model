from pathlib import Path

import gradio as gr
import torch
from PIL import Image
from transformers import CLIPTokenizer

import model_loader
import pipeline


def resolve_device(allow_cuda: bool = True, allow_mps: bool = False) -> str:
    device = "cpu"
    if torch.cuda.is_available() and allow_cuda:
        device = "cuda"
    elif (torch.has_mps or torch.backends.mps.is_available()) and allow_mps:
        device = "mps"
    return device


def load_runtime() -> tuple[dict, CLIPTokenizer, str]:
    base_dir = Path(__file__).resolve().parents[1]
    data_dir = base_dir / "data"

    vocab_path = data_dir / "vocab.json"
    merges_path = data_dir / "merges.txt"
    expected_model_path = data_dir / "v1-5-pruned-emaonly.ckpt"

    # Prefer canonical filename, but fall back to any single .ckpt in data/.
    if expected_model_path.exists():
        model_path = expected_model_path
    else:
        ckpt_files = sorted(data_dir.glob("*.ckpt"))
        if len(ckpt_files) == 1:
            model_path = ckpt_files[0]
        else:
            discovered = ", ".join(p.name for p in ckpt_files) if ckpt_files else "none"
            raise FileNotFoundError(
                f"Model checkpoint not found. Expected: {expected_model_path}. "
                f"Detected .ckpt files in data/: {discovered}. "
                "Place exactly one checkpoint in data/ or rename it to v1-5-pruned-emaonly.ckpt."
            )

    device = resolve_device()
    # Load tokenizer assets from local directory; this correctly initializes full CLIP vocab.
    tokenizer = CLIPTokenizer.from_pretrained(str(data_dir), local_files_only=True)

    if tokenizer.vocab_size < 10000:
        raise RuntimeError(
            f"Tokenizer loaded with unexpected vocab size {tokenizer.vocab_size}. "
            "Expected CLIP vocab around 49408. Check data/vocab.json and data/merges.txt."
        )
    models = model_loader.preload_models_from_standard_weights(str(model_path), device)
    return models, tokenizer, device


MODELS, TOKENIZER, DEVICE = load_runtime()


def generate_image(
    prompt: str,
    strength: float = 0.9,
    do_cfg: bool = True,
    cfg_scale: float = 8.0,
    sampler: str = "ddpm",
    num_inference_steps: int = 50,
    seed: int = 42,
):
    output_image = pipeline.generate(
        prompt=prompt,
        uncond_prompt="",
        input_image=None,
        strength=strength,
        do_cfg=do_cfg,
        cfg_scale=cfg_scale,
        sampler_name=sampler,
        n_inference_steps=int(num_inference_steps),
        seed=int(seed),
        models=MODELS,
        device=DEVICE,
        idle_device="cpu",
        tokenizer=TOKENIZER,
    )

    return Image.fromarray(output_image)


if __name__ == "__main__":
    iface = gr.Interface(
        fn=generate_image,
        inputs=[
            gr.Textbox(label="Prompt", placeholder="Describe the image you want"),
            gr.Slider(label="Strength", minimum=0.0, maximum=1.0, value=0.9),
            gr.Checkbox(label="Do CFG", value=True),
            gr.Slider(label="CFG Scale", minimum=1, maximum=14, value=8),
            gr.Dropdown(label="Sampler", choices=["ddpm"], value="ddpm"),
            gr.Slider(label="Inference Steps", minimum=1, maximum=100, value=50),
            gr.Number(label="Seed", value=42),
        ],
        outputs="image",
        title="PromptVision Diffusion",
        description="Generate images from text prompts using a from-scratch Stable Diffusion style pipeline.",
    )
    iface.launch()
