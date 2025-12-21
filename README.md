# BoxingHub

## Website: [https://www.boxinghub.org](https://www.boxinghub.org)

### MSc Artificial Intelligence Project Article: [Read Here](https://drive.google.com/file/d/1RFivyClzNFjEYS6Nbf7paTYIHEUnCM14/view?usp=drive_link)

### Complete PDF demo of the project: [Project Demo](https://drive.google.com/file/d/1RCXj8eFnj7AJ7g_S6-cP1TJ7YWzh98CX/view?usp=sharing)

### Video demo for the static website: [Watch Here](https://youtu.be/9yuzUpK1MCM)

#### Description

**_BoxingHub_** is an end-to-end MSc Artificial Intelligence project and full-stack prototype that assists boxing training by combining computer vision, rule-based dialogue, speech processing, and LLM-enabled personalization.

#### Author

**Hongbo Wei**  
AI/ML Engineer and boxer.

### Quick project summary

- Prototype components: YOLOv8-based punch detection & classification, a rule-based BoxingChatbot for defensive/counterattack suggestions, a speech-to-text + speaker-diarisation accessibility pipeline, and LLM-generated personalized motivational prompts.
- Model training summary: CPT on Microsoft COCO followed by SFT on several hundred manually annotated boxing frames. Training data was augmented (blurring, flipping, cropping, rotation, grayscale conversion, noise injection) to expand the dataset to thousands of frames.
- Evaluation highlights: object detection mAP = 94.1%, F1 = 90.4% on the held-out boxing test set. STT WER = 6.9%; speaker diarisation DER = 8.33%.
- LLM stack: experiments with Claude 3 (AWS Bedrock) and adaptation to DeepSeek‑V3.1 for local inference via Ollama.

### Core components & where to find them

- Computer vision (punch detection/classification)
  - YOLOv8-based detector, training and inference code in `computer_vision/` (see `computer_vision/views.py` for the inference endpoint and drawing utilities).
  - Training recipe: CPT on COCO → SFT on boxing frames (augmentation pipeline included in `computer_vision` scripts).

- Rule-based BoxingChatbot
  - Deterministic trainer recommending defenses and counterattacks. Implementation in `chatbot/bot.py` and web wiring in `chatbot/views.py`.

- Accessibility (STT + speaker diarisation)
  - Pipeline implemented in `nlp_app/speech_transcription_diarization.py`; upload UI available at `nlp_app/templates/nlp_app/nlp_app.html`.

- LLM integration
  - Prompting and LLM client code for Ollama and Bedrock experiments included under the LLMs/ folder and integration scripts referenced from `affirmations/`.

### Architecture & deployment notes

- Full-stack prototype built with Django, HTML/CSS/JavaScript and SQLite.
- Static frontend export and example static site available in `back-up/v0-boxinghub/` (see management command for exporting static files).
- Current hosted static site: Google Cloud Platform; active AI model inference is prototyped in the repo and not hosted in production.
- CI/CD: GitHub Actions workflows (check `.github/workflows/`).

### Installation (short)

Prereqs: Python 3.11, poetry recommended.

1. Install dependencies:

    ```bash
    poetry install
    ```

2. Activate the virtual environment (copy the printed command):

    ```bash
    poetry env activate
    ```

3. Add secrets (create a `.env` with API keys):

    **needed**
    - [Roboflow](https://roboflow.com/) / inference API = G5Ul0oVW1OgePLnFiYLU
    - [Ollama](https://ollama.com/)  / local LLM configuration if used

    **not needed**
    - Access Tokens from [Hugging Face](https://huggingface.co/)
    - Access Key and Access Key ID from [AWS](https://aws.amazon.com/)

4. Run the server:

    ```bash
    python manage.py runserver
    ```

### LLM affirmations (local Ollama)

The affirmations page uses the local Ollama server by default. Ensure Ollama is running on your machine (e.g. `ollama serve`) and the model is pulled (e.g. `ollama pull deepseek-v3.1:671b-cloud`) before opening `/affirmations/my-affirmations/`.

### Reproducible training & evaluation notes

- Pretraining/fine-tuning: CPT on Microsoft COCO followed by SFT using manually labelled boxing frames.
- Augmentations used: random blur, horizontal flip, random crop, rotation, grayscale conversion, and Gaussian/salt-and-pepper noise injection to increase robustness to real-world capture conditions.
- Reported metrics (held-out test set used for evaluation):
  - mAP: 94.1%
  - F1: 90.4%

Accessibility metrics:

- STT WER: 6.9%
- Speaker diarisation DER: 8.33%

### Files & pointers

- `computer_vision/views.py` — CV inference endpoint and visualization helpers.
- `chatbot/bot.py` — BoxingChatbot implementation.
- `nlp_app/speech_transcription_diarization.py` — STT + diarisation prototype.
- `back-up/v0-boxinghub/main/management/commands/export_static.py` — static export command and example static site.
- Templates: `templates/computer-vision.html`, `chatbot/templates/chatbot.html`, `nlp_app/templates/nlp_app/nlp_app.html`.

---

😁 Thank you for your interest in BoxingHub!

---

© 2023-2025 Hongbo Wei — [github.com/hongbo-wei](https://github.com/hongbo-wei)

[![CC BY 4.0][cc-by-image]][cc-by]

This work is licensed under a [Creative Commons Attribution 4.0 International License][cc-by].

[cc-by]: http://creativecommons.org/licenses/by/4.0/
[cc-by-image]: https://i.creativecommons.org/l/by/4.0/88x31.png
