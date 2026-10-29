import json
import re

def check_devanagari_purity(text):
    devanagari_chars = re.findall(r'[\u0900-\u097F]', text)
    alpha_chars = re.findall(r'[\u0900-\u097Fa-zA-Z]', text)
    if not alpha_chars:
        return 0.0
    return round(len(devanagari_chars) / len(alpha_chars), 4)

def evaluate_bilingual_response(response_text, required_terms, forbidden_terms, min_devanagari_ratio=0.85):
    purity = check_devanagari_purity(response_text)
    missing_terms = [t for t in required_terms if t not in response_text]
    violated_terms = [t for t in forbidden_terms if t in response_text]
    passed = (purity >= min_devanagari_ratio) and (len(missing_terms) == 0) and (len(violated_terms) == 0)
    return {
        "passed": passed,
        "devanagari_ratio": purity,
        "missing_required_terms": missing_terms,
        "violated_negative_constraints": violated_terms
    }

def compute_sxs_rubric_score(ratings):
    weights = {"instruction_following": 0.35, "hindi_fluency": 0.30, "factual_accuracy": 0.25, "tone_register": 0.10}
    return round(sum(ratings.get(k, 0) * w for k, w in weights.items()), 2)

if __name__ == "__main__":
    sample = "\u0915\u0943\u0924\u094d\u0930\u093f\u092e \u092c\u0941\u0926\u094d\u0920\u093f\u092e\u0924\u094d\u0924\u093e (AI) \u0915\u093e \u0909\u092a\u092f\u094b\u0917 \u0938\u094d\u0935\u093e\u0938\u094d\u0925\u094d\u092f \u0914\u0930 \u0936\u093f\u0915\u094d\u0937\u093e \u0915\u0947 \u0915\u094d\u0937\u0947\u0924\u094d\u0930 \u092e\u0947\u0902 \u0924\u0947\u091c\u0940 \u0938\u0947 \u092c\u0922\u093c \u0930\u0939\u093e \u0939\u0942\u0964"
    print(json.dumps(evaluate_bilingual_response(sample, ["\u0915\u0943\u0924\u094d\u0930\u093f\u092e \u092c\u0941\u0926\u094d\u0920\u093f\u092e\u0924\u094d\u0924\u093e", "\u0936\u093f\u0915\u094d\u0937\u093e"], ["\u0905\u0902\u0917\u094d\u0930\u0947\u091c\u0940 \u0905\u0928\u0941\u0935\u093e\u0926"]), ensure_ascii=False))
