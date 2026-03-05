# Roadmap

This roadmap is focused on turning the repository into a strong educational and engineering reference project.

## v1.1 - Reliability and Reproducibility

- Add deterministic smoke tests for the generation pipeline using fixed seeds.
- Add a config-driven inference script for repeatable experiments.
- Add pinned benchmark prompts and output gallery metadata.

## v1.2 - Sampler Expansion

- Add `pndm`, `lms`, and `heun` samplers.
- Add sampler comparison table (speed vs visual quality).
- Add tests for sampler scheduling and timestep behavior.

## v1.3 - Packaging and CLI

- Move code to a package layout (`src/` style).
- Add `python -m` CLI entrypoints for text-to-image and image-to-image.
- Add typed public interfaces and improved module docs.

## v1.4 - Demo and Documentation

- Add a hosted Gradio demo (Hugging Face Spaces).
- Publish architecture diagrams and a model-flow walkthrough.
- Add a reproducible tutorial from prompt to generated artifact.

## Stretch Goals

- Add lightweight evaluation tooling (prompt adherence proxy metrics).
- Add optional mixed-precision and memory-optimized inference paths.
- Add model card and release notes for each tagged version.
