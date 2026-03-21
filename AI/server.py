from flask import Flask, request, jsonify
import torch
import json
import re
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig
from thefuzz import process, fuzz
import pandas as pd

app = Flask(__name__)

MODEL_ID = "mistralai/Mistral-7B-Instruct-v0.2"
PATH = "./cleaneddata"

print("[SYSTEM] Warming up the GPU...")
quant_config = BitsAndBytesConfig(load_in_4bit=True, bnb_4bit_compute_dtype=torch.float16, bnb_4bit_quant_type="nf4", bnb_4bit_use_double_quant=True)
tokenizer = AutoTokenizer.from_pretrained(MODEL_ID)
model = AutoModelForCausalLM.from_pretrained(MODEL_ID, device_map="auto", quantization_config=quant_config)


df_tech = pd.read_csv(f"{PATH}/techskills.csv")
df_skills = pd.read_csv(f"{PATH}/skills.csv")
df_alt = pd.read_excel(f"{PATH}/Alternate Titles.xlsx")

tech_lookup = df_tech.groupby('O*NET-SOC Code')['Example'].apply(list).to_dict()
soft_skill_lookup = df_skills.groupby('O*NET-SOC Code')['Element Name'].apply(list).to_dict()
alt_title_map = dict(zip(df_alt['Alternate Title'], df_alt['O*NET-SOC Code']))
soc_to_formal_title = dict(zip(df_alt['O*NET-SOC Code'], df_alt['Title']))

def extract_resume_skills(resume_text):
    """Extract professional technical and soft skills from resume using Mistral."""
    prompt = f"""<s>[INST] Extract a flat JSON list of professional technical and soft skills from this resume.
    Resume: {resume_text[:2000]} [/INST] {{"candidate_skills": ["""

    inputs = tokenizer(prompt, return_tensors="pt").to("cuda")
    outputs = model.generate(**inputs, max_new_tokens=400, temperature=0.1, pad_token_id=tokenizer.eos_token_id)
    res_text = tokenizer.decode(outputs[0], skip_special_tokens=True)

    try:
        match = re.search(r'\{.*\}', res_text, re.DOTALL)
        if match:
            return json.loads(match.group(0))['candidate_skills']
    except Exception:
        return []
    return []

def get_formal_soc_code(input_text):
    """Identify job title and map to O*NET SOC code via fuzzy matching."""
    # 1. Mistral identifies the "vibe"
    prompt = f"<s>[INST] What is the most logical professional job title for this person? Output ONLY the title. \nText: {input_text[:1000]} [/INST]"
    inputs = tokenizer(prompt, return_tensors="pt").to("cuda")
    outputs = model.generate(**inputs, max_new_tokens=10, temperature=0.1)
    vibe_title = tokenizer.decode(outputs[0], skip_special_tokens=True).split('[/INST]')[-1].strip()

    # 2. Fuzzy match vibe_title against the Alternate Titles database
    best_match, score = process.extractOne(vibe_title, alt_title_map.keys(), scorer=fuzz.token_set_ratio)

    soc_code = alt_title_map[best_match]
    formal_name = soc_to_formal_title[soc_code]

    return soc_code, formal_name, score

def run_live_inference(resume_str, jd_str=None):
    """Main orchestration: get candidate skills, identify role, compute gap against O*NET ground truth."""

    can_skills = extract_resume_skills(resume_str)

    anchor_text = jd_str if jd_str else resume_str
    soc_code, formal_title, confidence = get_formal_soc_code(anchor_text)

    req_tech = tech_lookup.get(soc_code, [])
    req_soft = soft_skill_lookup.get(soc_code, [])
    total_required = set(req_tech + req_soft)

    current = set([str(s).lower().strip() for s in can_skills])
    gap = [str(s) for s in total_required if str(s).lower() not in current]

    return {
        "soc_code": soc_code,
        "formal_role": formal_title,
        "match_confidence": confidence,
        "candidate_skills_found": (current),
        "gap": gap[:15],  # Hard cap at 15 for the UI graph
        "trace": f"Grounded via O*NET SOC {soc_code} ({formal_title})"
    }

@app.route('/analyze_live', methods=['POST'])
def analyze():
    data = request.json
    resume_str = data.get('resume', '')
    jd_str = data.get('jd', None)
    
    if not resume_str:
        return jsonify({"error": "No resume text provided"}), 400
        
    result = run_live_inference(resume_str, jd_str)
    return jsonify(result)

if __name__ == '__main__':
    app.run( host ="0.0.0.0", port=5000)