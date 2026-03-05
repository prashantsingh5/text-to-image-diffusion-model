import sys
from pathlib import Path

import torch

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SD_PATH = PROJECT_ROOT / "sd"
if str(SD_PATH) not in sys.path:
    sys.path.append(str(SD_PATH))

from ddpm import DDPMSampler  # noqa: E402


def test_inference_timesteps_count():
    sampler = DDPMSampler(torch.Generator(device="cpu"))
    sampler.set_inference_timesteps(25)
    assert len(sampler.timesteps) == 25


def test_add_noise_preserves_shape():
    generator = torch.Generator(device="cpu")
    generator.manual_seed(123)

    sampler = DDPMSampler(generator)
    samples = torch.zeros((1, 4, 8, 8), dtype=torch.float32)
    timestep = torch.tensor(10, dtype=torch.int64)

    noisy = sampler.add_noise(samples, timestep)
    assert noisy.shape == samples.shape


def test_set_strength_reduces_timesteps():
    sampler = DDPMSampler(torch.Generator(device="cpu"))
    sampler.set_inference_timesteps(50)
    original = len(sampler.timesteps)
    sampler.set_strength(0.5)

    assert len(sampler.timesteps) < original
    assert len(sampler.timesteps) == 25
