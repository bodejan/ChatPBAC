# Master Thesis: PBAC in retrieval augmented LLMs

## Requirements

Create a ```.env``` file in the root directory.

### OpenAI

Create a OpenAI account and create a API key. Add the key to the ```.env``` file.

```
OPENAI_API_KEY = "YOUR_OPENAI_API_KEY"
```

## Prerequisites

1. Python 3.9 or higher

## Setup

### Step 1: Create a Virtual Environment
Ensure you have Python installed on your system. Python 3 and later include the venv module, which is used to create virtual environments. Here's how you can create a virtual environment named venv:

```bash
python3 -m venv venv
```

### Step 2: Activate the Virtual Environment
Before you can start installing packages, you need to activate the virtual environment. The activation command differs depending on your operating system.

Linux/Mac
```bash
source venv/bin/activate
```

Windows
```bash
venv\Scripts\activate
```

### Step 3: Install Requirements
With the virtual environment activated, you can now install the project's dependencies. These dependencies are listed in a file called requirements.txt. To install them, run:

```bash
pip install --no-cache-dir -r requirements.txt
```

### Step 4: Install Additional Requirements

```bash
pip install --upgrade-strategy eager "optimum[openvino,nncf]"
```



# TODOs

2. Fix parallel memory issues
3. Add instructions to gradio
4. Add configs to gradio
6. Fix purpose classification with history