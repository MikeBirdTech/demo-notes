Okay, here's a draft for your README in Markdown:

# Ollama Thinking Model Demo

## Purpose

This demo showcases the new "thinking" feature available in Ollama in version 0.9.0 for select models. It illustrates how users can enable or disable the model's explicit reasoning process and access this "thinking" output separately from the final response.

## Demo Video

[![Ollama Thinking Model Demo](https://img.youtube.com/vi/Wh9N6BKy39Q/0.jpg)](https://youtu.be/Wh9N6BKy39Q)

## Code Overview

This repository contains examples in both Python and JavaScript that demonstrate how to interact with Ollama models that support the thinking feature.

The code examples show how to:
*   Instantiate the Ollama client.
*   Send prompts to a supported model (e.g., `deepseek-r1`).
*   Enable the `think` parameter in API calls/client methods.
*   Retrieve and display both the model's "thinking" process and its final "content" or answer.
*   (If applicable, add if your demo shows this: Handle streaming responses where thinking and content might be interleaved.)

## Benefits of Thinking Models

Being able to access a model's thinking process locally via Ollama offers several advantages:

*   **Transparency:** Understand *how* a model arrives at an answer, not just *what* the answer is. This is great for debugging and building trust.
*   **Improved Accuracy:** For complex queries, allowing the model to "think through" steps can lead to more accurate and well-reasoned outputs.
*   **Control & Flexibility:** Choose to enable thinking for detailed analysis or disable it for faster, direct answers.
*   **Novel Applications:** Enables new user experiences like visualizing the AI's thought process, or creating more interactive and "aware" AI agents.
*   **Privacy:** All processing, including the "thinking," happens locally, keeping your data secure.

## Getting Started

1.  Ensure you have the latest version of [Ollama](https://ollama.com/) installed.
2. Go to the [models page](https://ollama.com/search?c=thinking)
3.  Pull a model that supports thinking (e.g., `ollama run deepseek-r1`).
4.  **For Python:**
    *   Make sure you have the latest `ollama` Python library: `pip install ollama --upgrade`
    *   Run the Python script: `python your_python_script_name.py`
4.  **For JavaScript:**
    *   Make sure you have the latest `ollama` JavaScript library: `npm i ollama` (or `yarn add ollama`)
    *   Run the JavaScript script: `node your_javascript_script_name.js`
