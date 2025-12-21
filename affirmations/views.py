import os

import requests
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_GET
from main.utils import get_likes_and_loves

OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434/api/generate")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "deepseek-v3.1:671b-cloud")
AFFIRMATION_PROMPT = os.getenv(
    "AFFIRMATION_PROMPT",
    "Call me Bruce. Give me an affirmation to boost my motivation today, "
    "referencing plants, animals, or flowers by adding emoji. "
    "Don't show the prompt, only the quote. "
    "Do not add anything like Here is an affirmation... just return the affirmation alone",
)


# Create your views here.
def my_affirmations(request):
    likes, loves = get_likes_and_loves()
    context = {
        'likes': likes,
        'loves': loves,
        'active': 'ai-boxing',
    }
    return render(request, 'affirmations.html', context=context)


@require_GET
def affirmation_api(request):
    payload = {
        "model": OLLAMA_MODEL,
        "prompt": AFFIRMATION_PROMPT,
        "stream": False,
        "options": {
            "temperature": 0.7,
            "num_predict": 120,
        },
    }
    try:
        response = requests.post(OLLAMA_URL, json=payload, timeout=30)
    except requests.RequestException as exc:
        return JsonResponse(
            {"error": "Failed to reach the local model server.", "details": str(exc)},
            status=502,
        )

    if not response.ok:
        return JsonResponse(
            {"error": "Model inference failed.", "details": response.text},
            status=502,
        )

    try:
        data = response.json()
    except ValueError:
        return JsonResponse(
            {"error": "Invalid response from model server.", "details": response.text},
            status=502,
        )

    text = data.get("response")
    if not text:
        return JsonResponse(
            {"error": "No affirmation returned by model.", "details": data},
            status=502,
        )

    return JsonResponse({"affirmation": text})
