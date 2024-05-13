import torch
from langchain_core.prompts import PromptTemplate
from langchain_community.llms.huggingface_pipeline import HuggingFacePipeline

device = torch.device("mps" if torch.backends.mps.is_available() else "cpu")
print("Using device:", device)


gpu_llm = HuggingFacePipeline.from_model_id(
    model_id="microsoft/Phi-3-mini-128k-instruct",
    task="text-generation",
    device_map="cuda",  # Use GPU acceleration if available
    pipeline_kwargs={"max_new_tokens": 100},
    model_kwargs={"trust_remote_code": True}
)

template = """Question: {question}

Answer: Let's think step by step."""
prompt = PromptTemplate.from_template(template)

gpu_chain = prompt | gpu_llm

question = "What is electroencephalography?"

print(gpu_chain.invoke({"question": question}))
