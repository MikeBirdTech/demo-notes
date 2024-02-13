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
  - relocate `conversation_history_path`
  - relocate `conversation_history`
- Update `interpreter/core/computer/utils/html_to_png_base64.py`

## Questions

Why would a user want to set `interpreter.conversation_history = True` in a python app?

- seems like the type of thing that should be handled within the script

For React/HTML, can we just base64 the code directly? Does the assistant need to see an image or can it make good decisions from simply knowing the code?

- If the base64 encoding of an image is needed, can it be accomplised without saving to disk?

## Notes

OpenInterpreter class has a field `conversation_history_path` which shouldn't exist

- highly confident this should be removed

OpenInterpreter class has a boolean field `conversation_history`

- this should be removed from core, but added to TUI
- in `core.py: _streaming_chat()`
  - if user has enabled conversation history, it writes to a file on disk
  - this should be moved to TUI because the python library should not be interfacing with a user's storage

html_to_png_base64.py

- The purpose of this file is to take an image of code and convert it to base64 and return the base64 string.
- Uses Html2Image library - [link](https://pypi.org/project/html2image/) 
- If we can base64 encode the image without needing to save the image, we can remove all mentions of `get_storage_path`
- Can we just base64 the code directly? Why do we need an image?

  - Is it required for vision/os mode?

- `interpreter/core/computer/terminal/languages/react.py` uses it to yield content from `run()`
- The base64 of the html allows "Assistant to see image"

  - Is this just for OS mode?
  - Can we validate by seeing where it checks for "type == image"?

- `interpreter/core/computer/terminal/languages/html.py` uses it to yield content from `run()`
- how can we maintain functionality of `html_to_png_base64` with the removal of `get_storage_path()`
- The default of `hti.output_path` is to use the current working directory, but we overwrite it with `get_storage_path()`

  - Does this need to be overwritten?
  -

- In the Python library, users can set this to be true or false. However, in that situation, it makes sense that the user will want to set the method and the path for how conversation history is saved.

In `local_storage_path.py` - appdirs [repo](https://github.com/ActiveState/appdirs) This project has been officially deprecated. You may want to check out https://pypi.org/project/platformdirs/ which is a more active fork of appdirs. Thanks to everyone who has used appdirs. Shout out to ActiveState for the time they gave their employees to work on this over the years.
