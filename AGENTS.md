# AGENTS.md

## Cursor Cloud specific instructions

This is **pydub**, a Python library for audio manipulation (not a web service). There are no running servers or databases.

### Key commands

| Task | Command |
|------|---------|
| Tests | `python test/test.py` |
| Lint | `python -m pylama -i W,E501 pydub/` |
| Install (dev) | `pip install -e . scipy pylama` |

### Known issues

- **Python 3.12+ compat**: 2 tests (`test_from_file_clean_fail`, `test_split_on_silence_complete_silence`) fail because `assertEquals` was removed in Python 3.12. This is a pre-existing issue—use `assertEqual` if adding new tests.
- **Lint is advisory**: CI runs `pylama || true`; lint warnings are informational and do not block.

### System dependencies

- `ffmpeg` is required for non-WAV format support (pre-installed in the VM).
- `libopus-dev` is required for Opus codec tests (pre-installed in the VM).
- `scipy` is needed for `pydub.scipy_effects` (high/low pass filters).

### Project structure

- `pydub/` — main package (AudioSegment, effects, generators, silence detection, playback)
- `test/test.py` — full test suite (unittest)
- `test/data/` — audio fixtures (WAV, MP3, OGG, MP4, FLAC, etc.)
- See `README.markdown` for usage docs and `API.markdown` for full API reference.
