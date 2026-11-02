# GenAI-Powered Product Description Generator (Module 06)

**Course:** ITAI - Artificial Intelligence Applications  
**Module:** AI in Retail & E-Commerce  
**Author:** Kamron Robinson  

---

## 1. Project Overview & Retail Use Case
This project implements a generative AI retail web application built with Flask that takes product titles, key attributes, and customer audience tones to synthesize tailored e-commerce copy. By automating product description authoring, retailers can accelerate catalog time-to-market, improve SEO rankings, and deliver segmented copy suited for specific shopper cohorts (e.g., humorous, young adults, or enterprise professionals).

---

## 2. Technical Reflection & Design Decisions (Assignment Deliverables)

### Architecture & LLM Selection
I selected **Option C (Local Small LLM via Ollama / LM Studio with Fallback Engine)**. Local execution allows rapid prompt iteration without vendor API token charges or rate limit delays. To guarantee 100% operational reliability, the system features a heuristic fallback engine so evaluation and testing proceed seamlessly even when local daemons are offline.

### Implementation Challenges
The primary challenge was balancing prompt constraints: retail product descriptions must remain persuasive without becoming repetitive or "hallucinating" unverified product claims. Adding persona-based tone conditioning required fine-tuning the prompt to adjust sentence cadence and vocabulary without losing focus on the essential feature keywords.

### Real-World Retail Extensions & Ethics
In an enterprise retail deployment, this application could integrate with inventory catalogs (ERP) and clickstream tracking systems to dynamically adapt copy tone based on individual shopper browsing history (collaborative filtering). Ethically, retailers using GenAI must guard against deceptive marketing practices, ensuring descriptions do not exaggerate durability, material purity, or performance metrics, and disclose generative assistance where required by consumer protection standards.

---

## 3. How to Run Locally

```bash
# Clone or download the repository
cd retail-product-description-genai

# Install dependencies
pip install flask requests

# Launch the application
python app.py
