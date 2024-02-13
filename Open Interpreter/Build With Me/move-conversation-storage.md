# Move conversation storage to TUI

## Mission

Decouple Core from Terminal Interface

## Goal

Remove uses of `get_storage_path` by Core

## Justification

- Core should be stateless
- Core should not have knowledge of conversation history path
- TUI should be responsible for storing to disk

## Objectives

- Update `interpreter/core/core.py`
- Update `interpreter/core/computer/utils/html_to_png_base64.py`

## Notes
