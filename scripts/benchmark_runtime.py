import argparse
import sys
import time
from pathlib import Path

import torch
from transformers import CLIPTokenizer


ROOT = Path(__file__).resolve().parents[1]
SD_PATH = ROOT / "sd"
if str(SD_PATH) not in sys.path:
    sys.path.append(str(SD_PATH))

import model_loader  # noqa: E402
import pipeline  # noqa: E402


SHOWCASE_PROMPTS = [
    (
        "P1",
        "Cinematic Character",
        "a cinematic portrait of a tiger astronaut in a detailed space suit, rim lighting, volumetric fog, ultra detailed, sharp focus, 8k",
        "assets/showcase/prompt-1-cinematic-tiger-astronaut.png",
    ),
    (
        "P2",
        "Atmosphere and Lighting",
        "a neon-lit rainy cyberpunk street in tokyo at night, reflections on wet asphalt, people with umbrellas, depth of field, highly detailed concept art",
        "assets/showcase/prompt-2-neon-rainy-street.png",
    ),
    (
        "P3",
        "Composition and Detail",
        "an ancient mountain temple at golden hour, dramatic clouds, god rays, intricate stone carvings, wide angle composition, photorealistic, high detail",
        "assets/showcase/prompt-3-golden-hour-temple.png",
    ),
]


def resolve_device() -> str:
    if torch.cuda.is_available():
        return "cuda"
    if hasattr(torch.backends, "mps") and torch.backends.mps.is_available():
        return "mps"
    return "cpu"


def run_once(models, tokenizer, device: str, prompt: str, steps: int, cfg: float, seed: int):
    t0 = time.perf_counter()
    _ = pipeline.generate(
        prompt=prompt,
        uncond_prompt="",
        input_image=None,
        strength=0.9,
        do_cfg=True,
        cfg_scale=cfg,
        sampler_name="ddpm",
        n_inference_steps=steps,
        seed=seed,
        models=models,
        device=device,
        idle_device="cpu",
        tokenizer=tokenizer,
    )
    return time.perf_counter() - t0


def avg_runtime(models, tokenizer, device: str, prompt: str, steps: int, cfg: float, seed: int, repeats: int) -> float:
    values = [run_once(models, tokenizer, device, prompt, steps, cfg, seed) for _ in range(repeats)]
    return sum(values) / len(values)


def main() -> None:
    parser = argparse.ArgumentParser(description="Measure runtime tables for README.")
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--cfg", type=float, default=8.0)
    parser.add_argument("--repeats", type=int, default=2)
    args = parser.parse_args()

    data_dir = ROOT / "data"
    ckpt_path = data_dir / "v1-5-pruned-emaonly.ckpt"
    if not ckpt_path.exists():
        raise FileNotFoundError(f"Checkpoint missing: {ckpt_path}")

    device = resolve_device()
    tokenizer = CLIPTokenizer.from_pretrained(str(data_dir), local_files_only=True)
    models = model_loader.preload_models_from_standard_weights(str(ckpt_path), device)

    print("Device:", device)
    print("Tokenizer vocab size:", tokenizer.vocab_size)

    # Warmup (excluded from averages)
    print("Running warmup pass...")
    _ = run_once(models, tokenizer, device, SHOWCASE_PROMPTS[0][2], 20, args.cfg, args.seed)

    print("\nREADME Evaluation Snapshot rows:")
    print("| Prompt ID | Prompt Theme | Seed | Steps | CFG | Device | Runtime (s) | Output |")
    print("|---|---|---:|---:|---:|---|---:|---|")
    for pid, theme, prompt, output_path in SHOWCASE_PROMPTS:
        rt = avg_runtime(models, tokenizer, device, prompt, 50, args.cfg, args.seed, args.repeats)
        print(f"| {pid} | {theme} | {args.seed} | 50 | {args.cfg:.1f} | {device.upper()} | {rt:.2f} | `{output_path}` |")

    print("\nREADME Performance Benchmark rows:")
    print("| Resolution | Steps | CFG | Seed | Avg Runtime (s) | Notes |")
    print("|---|---:|---:|---:|---:|---|")
    for steps, note in [(20, "Fast preview mode"), (30, "Balanced quality/speed"), (50, "Showcase quality mode")]:
        rt = avg_runtime(models, tokenizer, device, SHOWCASE_PROMPTS[0][2], steps, args.cfg, args.seed, args.repeats)
        print(f"| 512x512 | {steps} | {args.cfg:.1f} | {args.seed} | {rt:.2f} | {note} |")


if __name__ == "__main__":
    main()
