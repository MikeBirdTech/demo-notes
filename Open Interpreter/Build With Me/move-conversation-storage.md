# Move conversation storage to TUI

## Mission

Decouple Core from Terminal Interface

## Goal

Remove `get_storage_path` from Core

## Justification

- Core should be stateless
- TUI should be responsible for storing to disk
- Core should not have knowledge of conversation history path

## Objectives

- Update `interpreter/core/core.py`
  - remove `conversation_history_path`
- Update `interpreter/core/computer/utils/html_to_png_base64.py`

## Notes

OpenInterpreter class has a field `conversation_history_path` which shouldn't exist

html_to_png_base64

- `interpreter/core/computer/terminal/languages/react.py` uses it to yield content from `run()`
- `interpreter/core/computer/terminal/languages/html.py` uses it to yield content from `run()`
- how can we maintain functionality of `html_to_png_base64` with the removal of `get_storage_path()`

Does `conversation_history` boolean need to exist?

- In the Python library, users can set this to be true or false. However, in that situation, it makes sense that the user will want to set the method and the path for how conversation history is saved.
