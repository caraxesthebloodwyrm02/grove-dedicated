# Quarterly VLM / VLA tracking sheet

**Purpose:** Revisit this table each quarter (license changes, new checkpoints, deprecations). Prefer **official model cards**, **LICENSE files in repos**, and **arXiv / vendor system cards** over blog leaderboards.

**Discipline:** When updating a row, paste the **exact Hub revision** or **git tag** you used for evaluation, and the **date** you read the model card.

---

## Tracking table (seed set of five)

| Model / checkpoint | Class | Modalities (from card) | License (source) | Benchmarks / evals named on official card or primary paper | Primary official links |
| -------------------- | ----- | ------------------------ | ---------------- | ------------------------------------------------------------- | ----------------------- |
| **CLIP ViT-L/14** (`openai/clip-vit-large-patch14`) | Dual-encoder VLM (contrastive) | Image + text; `zero-shot-image-classification` | See OpenAI CLIP **model card** on Hub (research use framing; not a generic OSS license tag—read card + [CLIP GitHub `model-card.md`](https://github.com/openai/CLIP/blob/main/model-card.md)) | Long list in Hub card / paper: ImageNet variants, CIFAR, OCR-related sets, retrieval, etc. ([arXiv:2103.00020](https://arxiv.org/abs/2103.00020)) | https://huggingface.co/openai/clip-vit-large-patch14 · https://arxiv.org/abs/2103.00020 · https://openai.com/blog/clip/ |
| **LLaVA-1.5-7B** (`llava-hf/llava-1.5-7b-hf`) | Instruction-tuned VLM | Image + text; `image-text-to-text`, conversational | **LLAMA 2 Community License** (stated in Hub README license section) | Project site + paper for task coverage; card documents `transformers` usage and training dataset `liuhaotian/LLaVA-Instruct-150K` | https://huggingface.co/llava-hf/llava-1.5-7b-hf · https://llava-vl.github.io/ |
| **Qwen2-VL-7B-Instruct** (`Qwen/Qwen2-VL-7B-Instruct`) | General multimodal VLM | Image, video, text; multilingual text-in-image | **Apache-2.0** (Hub metadata `license:apache-2.0`; repo includes `LICENSE`) | Card tables: MMMU, DocVQA, ChartQA, TextVQA, MathVista, video suites (MVBench, Video-MME, etc.) | https://huggingface.co/Qwen/Qwen2-VL-7B-Instruct · https://arxiv.org/abs/2409.12191 · https://github.com/QwenLM/Qwen2-VL · https://qwenlm.github.io/blog/qwen2-vl/ |
| **OpenVLA-7B** (`openvla/openvla-7b`) | Vision-language-action (robotics) | Camera image + language instruction → **7-DoF action** | **MIT** (Hub metadata; card states checkpoints + training code under MIT) | Open X-Embodiment pretraining; zero-shot / fine-tune guidance for BridgeV2-style setups in card; full numbers in [arXiv:2406.09246](https://arxiv.org/abs/2406.09246) | https://huggingface.co/openvla/openvla-7b · https://arxiv.org/abs/2406.09246 · https://github.com/openvla/openvla · https://openvla.github.io/ |
| **RT-2 (Robotics Transformer 2)** | Google DeepMind VLA-style vision-language-action | Vision + language → discrete actions (tokenized) | **Google / DeepMind terms** (not an open Hub weight drop; use vendor terms for any API or released artifacts) | Paper reports simulation and real-robot metrics (e.g. emergent skills, generalization experiments)—read [arXiv:2307.15818](https://arxiv.org/abs/2307.15818) for authoritative numbers | https://arxiv.org/abs/2307.15818 · https://www.deepmind.com/publications/rt-2-vision-language-action-models |

**Note:** The Qwen2-VL Hub page flags a successor family ([Qwen2.5-VL-7B-Instruct](https://huggingface.co/Qwen/Qwen2.5-VL-7B-Instruct)); on your next review, decide whether to **migrate the row** or track both.

---

## Optional proprietary API baselines (system cards, not weights)

If you compare against closed APIs, store **product system-card URLs** and **policy version dates** instead of pretending there is a single static “model card” like on Hugging Face. Examples to bookmark in your org wiki (URLs change; verify live):

- OpenAI: platform documentation and safety/system materials for GPT-4 class multimodal models.
- Google: Gemini / Google DeepMind documentation for multimodal capabilities and terms.
- Anthropic: Claude product documentation and policy pages.

These are **not** duplicated here to avoid stale links; assign an owner to refresh quarterly.

---

## Related

- [canonical-bibliography.md](canonical-bibliography.md) — surveys and standards.
- [reproducibility-stack-map.md](reproducibility-stack-map.md) — how this repo pins Python deps today.
- Hugging Face model card guide: https://huggingface.co/docs/hub/model-cards
