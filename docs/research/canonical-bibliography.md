# Canonical bibliography seed (Tier A)

This file is the **team bibliography seed** for reproducible ML/CV engineering, integration (MLOps), and vision-language (including action) agents. Prefer these sources for decisions that must be defensible; use blogs only with primary cross-checks.

**Scope:** dependency reproducibility, pipeline integration, VLMs/VLAs, CV/ML history anchors.

---

## Python packaging and reproducible installs

| Resource | URL |
| -------- | --- |
| PEP 517 — build backends | https://peps.python.org/pep-0517/ |
| PEP 518 — `pyproject.toml` build declaration | https://peps.python.org/pep-0518/ |
| PEP 621 — project metadata in `pyproject.toml` | https://peps.python.org/pep-0621/ |
| PEP 751 — standard format to record dependencies for installation reproducibility | https://peps.python.org/pep-0751/ |
| PEP 665 — withdrawn lockfile PEP (historical context) | https://peps.python.org/pep-0665/ |

---

## Reproducible research and study-level rigor

| Resource | URL |
| -------- | --- |
| National Academies — *Reproducibility and Replicability in Science* (2019); search the NAP catalog | https://www.nationalacademies.org/our-work/reproducibility-and-replicability-in-science |
| Ten simple rules for implementing open and reproducible research practices (PMC) | https://pmc.ncbi.nlm.nih.gov/articles/PMC9815586/ |

---

## MLOps and integration (CI/CD, CT, lineage)

| Resource | URL |
| -------- | --- |
| Google Cloud — MLOps: continuous delivery and automation pipelines in ML | https://docs.cloud.google.com/architecture/mlops-continuous-delivery-and-automation-pipelines-in-machine-learning |
| AWS — What is MLOps? | https://aws.amazon.com/what-is/mlops/ |
| MLOps principles (ml-ops.org) | https://ml-ops.org/content/mlops-principles |

---

## Vision-language models — surveys and systematic reviews

| Resource | URL |
| -------- | --- |
| Exploring the Frontier of Vision-Language Models (arXiv HTML) | https://arxiv.org/html/2404.07214v2 |
| A Comprehensive Survey and Guide to Multimodal Large Language Models in Vision-Language Tasks (arXiv HTML) | https://arxiv.org/html/2411.06284v3 |
| A systematic review of vision language models (ScienceDirect) | https://www.sciencedirect.com/science/article/pii/S2590005626000627 |
| Vision Language Models: A Survey of 26K Papers (arXiv PDF; bibliometric lens) | https://arxiv.org/pdf/2510.09586 |

---

## Vision-language-action (embodied / robotics)

| Resource | URL |
| -------- | --- |
| Pure Vision Language Action (VLA) Models: A Comprehensive Survey (arXiv HTML) | https://arxiv.org/html/2509.19012v1 |
| A Survey on Efficient Vision-Language-Action Models (arXiv HTML) | https://arxiv.org/html/2510.24795v1 |

---

## Computer vision / deep learning history (anchor references)

| Resource | URL |
| -------- | --- |
| Annotated History of Modern AI and Deep Learning (Schmidhuber) | https://people.idsia.ch/~juergen/deep-learning-history.html |
| History of artificial neural networks (Wikipedia) | https://en.wikipedia.org/wiki/History_of_artificial_neural_networks |

---

## Minimum reading set (time-boxed)

1. PEP 751 + your toolchain’s lockfile documentation (`uv`, Poetry, or `pip-tools`).
2. Google Cloud MLOps pipeline architecture doc (linked above).
3. One VLM survey + one VLA survey from the tables above.
4. One history anchor: Wikipedia ANN history and/or Schmidhuber’s annotated history, plus primary papers for any milestone you cite formally.

---

## Hugging Face — model card discipline (for quarterly VLM tracking)

| Resource | URL |
| -------- | --- |
| Model Cards (Hub documentation) | https://huggingface.co/docs/hub/model-cards |
