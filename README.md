---
title: pbac-rag
app_file: ui.py
sdk: gradio
sdk_version: 4.41.0
---
# Master Thesis: PBAC in retrieval augmented LLMs


## Prerequisites

Python 3.9 or higher

## Setup
1. Execute the [install.py](install.py) script.

    ```bash
    python3 install.py
    ```
2. Create a ```.env``` file in the root directory.

    ```
    cp .env.example .env
    ```

3. Connect an LLM inference provider.

    a.) Add an OpenAI API key, or

    b.) add an API key for the inference provider of your choice $^{1}$

4. Setup the DB.

    a.) Request access to the demo DB at [jan.bode@campus.tu-berlin.de](jan.bode@campus.tu-berlin.de), or

    b.) follow the [instructions](https://github.com/bodejan/california-imr-pii) to setup your own DB.

5. Run the gradio app.

    ```
    python ui.py
    ```

$^1$ To change the LLM inference provider install the langchain-*provider* package and adjust the llm declarations in [1](backend/query_generation/llm.py#78), [2](backend/retrieval_decision/llm.py#L62), and [3](backend/chat/llm.py#52).
