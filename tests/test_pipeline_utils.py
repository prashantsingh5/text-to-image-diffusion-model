import sys
from pathlib import Path

import torch

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SD_PATH = PROJECT_ROOT / "sd"
if str(SD_PATH) not in sys.path:
    sys.path.append(str(SD_PATH))

import pipeline  # noqa: E402


def test_get_time_embedding_shape():
    emb = pipeline.get_time_embedding(0)
    assert emb.shape == (1, 320)


def test_rescale_maps_and_clamps_values():
    x = torch.tensor([-1.0, 0.0, 1.0])
    out = pipeline.rescale(x.clone(), (-1, 1), (0, 255), clamp=True)

    assert torch.isclose(out[0], torch.tensor(0.0))
    assert torch.isclose(out[-1], torch.tensor(255.0))
    assert out.min() >= 0
    assert out.max() <= 255
