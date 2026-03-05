# Changelog

All notable changes to this project will be documented in this file.

## [Unreleased]

### Added

- Repository rebrand to PromptVision Diffusion.
- Gradio app entrypoint for text-to-image generation.
- Test suite for DDPM sampler and pipeline utilities.
- CI workflow for automated test execution.
- Showcase prompt gallery and Mermaid architecture diagram in README.

### Changed

- Flattened repository structure to root-level `sd/`, `data/`, `images/`, and `notebooks/`.
- Tokenizer and pipeline compatibility fixes for newer `transformers` versions.

### Fixed

- Robust checkpoint detection in `sd/app.py`.
- Prompt-tokenization issue that caused poor generation quality.
- Missing dependency handling for `pytorch-lightning`.

## [1.0.0] - TBD

### Planned

- Final showcase assets and benchmark metrics.
- Release notes and tagged stable release.
