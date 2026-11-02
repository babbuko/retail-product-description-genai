"""
Module 06: AI in Retail - GenAI-Powered Product Description Generator
ITAI - Artificial Intelligence Applications
Author: Kamron Robinson
"""

from flask import Flask, render_template, request
import requests
import json

app = Flask(__name__)

# Local LLM Endpoints
OLLAMA_API_URL = "http://localhost:11434/api/generate"
LM_STUDIO_API_URL = "http://localhost:1234/v1/chat/completions"


def generate_retail_fallback(product_name: str, keywords: list, tone: str) -> str:
    """Deterministic fallback copywriter ensuring 100% application uptime."""
    kw_str = ", ".join(keywords)
    tone_lower = tone.lower()

    if "humorous" in tone_lower:
        return (
            f"Let’s be honest: life is too short for mediocre gear. Meet {product_name}—"
            f"engineered with {kw_str} so you can conquer your routine without losing your mind. "
            f"Warning: Excessive satisfaction and jealous side-eyes from friends may occur."
        )
    elif "formal" in tone_lower or "professionals" in tone_lower:
        return (
            f"Introducing the {product_name}, a premier enterprise-grade solution characterized by "
            f"{kw_str}. Meticulously designed for demanding operational standards, this product "
            f"ensures sustained reliability, unmatched performance, and seamless workflow integration."
        )
    elif "young adults" in tone_lower or "casual" in tone_lower:
        return (
            f"Upgrade your daily setup with {product_name}! Packed with {kw_str}, it’s built to keep up "
            f"with your fast-paced lifestyle without missing a beat. Sleek, dependable, and always ready "
            f"to elevate your everyday vibe."
        )
    else:  # Neutral / Standard Retail
        return (
            f"Discover superior quality and everyday convenience with the {product_name}. "
            f"Featuring industry-leading craftsmanship with {kw_str}, this product delivers dependable "
            f"results tailored for modern consumer expectations."
        )


def query_llm_product_description(product_name: str, keywords: list, tone: str) -> str:
    """Routes the prompt to Ollama or LM Studio, falling back smoothly if inactive."""
    kw_str = ", ".join(keywords)
    prompt = (
        f"You are an expert retail e-commerce copywriter. Write a high-converting, compelling, "
        f"and engaging product description for: '{product_name}'.\n"
        f"Key Features & Benefits to include: {kw_str}.\n"
        f"Target Audience Tone: {tone}.\n\n"
        f"Guidelines:\n"
        f"- Highlight the features naturally.\n"
        f"- Maintain the requested '{tone}' tone throughout the copy.\n"
        f"- Length: 2 to 4 concise, impactful sentences.\n"
        f"- Do not include meta commentary or introductory remarks.\n\n"
        f"Product Description:"
    )

    # 1. Attempt Ollama (port 11434)
    try:
        payload = {
            "model": "gemma",  # or llama3, mistral, phi
            "prompt": prompt,
            "stream": False
        }
        res = requests.post(OLLAMA_API_URL, json=payload, timeout=5)
        if res.status_code == 200:
            return res.json().get("response", "").strip()
    except Exception:
        pass

    # 2. Attempt LM Studio (port 1234)
    try:
        payload = {
            "messages": [
                {"role": "system", "content": "You are a professional retail product description writer."},
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.7
        }
        res = requests.post(LM_STUDIO_API_URL, json=payload, timeout=5)
        if res.status_code == 200:
            return res.json()["choices"][0]["message"]["content"].strip()
    except Exception:
        pass

    # 3. Rule-based Fallback
    return generate_retail_fallback(product_name, keywords, tone)


@app.route("/", methods=["GET", "POST"])
def index():
    product_name = ""
    keywords_raw = ""
    selected_tone = "neutral"
    description = None

    if request.method == "POST":
        product_name = request.form.get("product_name", "").strip()
        keywords_raw = request.form.get("keywords", "").strip()
        selected_tone = request.form.get("tone", "neutral")

        if product_name and keywords_raw:
            keywords_list = [k.strip() for k in keywords_raw.split(",") if k.strip()]
            description = query_llm_product_description(product_name, keywords_list, selected_tone)

    return render_template(
        "index.html",
        product_name=product_name,
        keywords=keywords_raw,
        selected_tone=selected_tone,
        description=description
    )


if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=5000)
