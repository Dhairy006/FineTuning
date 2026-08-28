# ZemaxGPT: Fine-Tuned Llama 3.2 for Optical Engineering

ZemaxGPT is a domain-adapted language model for answering technical questions about **Zemax OpticStudio**. It was fine-tuned from Llama 3.2 3B Instruct on a curated instruction dataset spanning sequential and non-sequential optical design, analysis, optimization, tolerancing, and ZOS-API programming.

## Highlights

- **Base model:** Llama 3.2 3B Instruct
- **Fine-tuning:** 4-bit QLoRA / LoRA with Unsloth and TRL
- **Adapter:** rank 16, alpha 32, 97 MB Safetensors checkpoint
- **Training data:** 763 instruction-response examples across seven technical categories
- **Deployment:** designed for private local inference through Ollama

## Repository layout

| Path | Purpose |
| --- | --- |
| `Finetuned_Model/` | Final LoRA adapter, metadata, chat template, and Ollama Modelfile |
| `zemax_opticstudio_finetune_dataset.jsonl` | Consolidated supervised fine-tuning dataset |
| `dataset_parts/` | Source datasets and Python scripts used to generate/assemble training data |
| `notebooks/` | Google Colab notebooks for training and GGUF conversion |
| `requirements.txt` | Core packages used for model training and inference workflows |

The large model artifact is versioned with **Git LFS**. Checkpoint folders and the exported 2 GB GGUF are deliberately excluded to keep this repository focused on the reproducible fine-tuning deliverable.

## Training configuration

The model was trained as a PEFT LoRA adapter on:

```text
unsloth/llama-3.2-3b-instruct-unsloth-bnb-4bit
```

| Setting | Value |
| --- | --- |
| LoRA rank | 16 |
| LoRA alpha | 32 |
| LoRA dropout | 0.05 |
| Target modules | Attention and MLP projections |
| Epochs | 3 |
| Training steps | 288 |

## Run locally with Ollama

Install [Ollama](https://ollama.com), clone this repository with Git LFS, then run:

```powershell
git lfs install
git clone https://github.com/Dhairy006/zemaxgpt-llama-finetuning.git
cd zemaxgpt-llama-finetuning\Finetuned_Model

ollama pull llama3.2:3b
ollama create zemaxgpt:3b -f .\Modelfile
ollama run zemaxgpt:3b
```

> The adapter was trained on an Unsloth 4-bit base. For best portability, merge the adapter and export a GGUF from the original training environment. The included Modelfile provides a direct-adapter route for local evaluation with Ollama.

## Example prompt

```text
How do I enable Robust Ray Aiming in Zemax OpticStudio, and when should I use it?
```

## Tech stack

Python, PyTorch, Hugging Face Transformers, Datasets, TRL, Unsloth, LoRA/QLoRA, Safetensors, JSONL, Google Colab, Ollama, and Git LFS.

## Notes

This project is intended as a technical demonstration of domain-specific LLM fine-tuning. Model outputs should be validated against the applicable Zemax OpticStudio documentation and the installed ZOS-API version before use in production optical-design workflows.
