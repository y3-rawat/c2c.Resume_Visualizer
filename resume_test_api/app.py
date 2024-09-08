import time 
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from concurrent.futures import ThreadPoolExecutor
import calculations
import concurrent.futures
import json
import fetchPeoples
app = Flask(__name__)
cors = CORS(app, resources={r"/submit": {"origins": "*"}})
api = None
executor = ThreadPoolExecutor(max_workers=5)
@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

def run_parallel_tasks(final_resume, job_description, extracted_text):
    tasks = {
        'skills': lambda: calculations.skills_taken(final_resume, job_description),
        'projects': lambda: calculations.projects_done(final_resume, job_description),
        'courses1': lambda: calculations.courses_done1(final_resume, job_description),
        'courses2': lambda: calculations.courses_done2(final_resume, job_description),
        'experience': lambda: calculations.experience_done(final_resume, job_description),
        'experience2': lambda: calculations.experience_done2(final_resume, job_description),
        'score1': lambda: calculations.Score_cards1(extracted_text, job_description),
        'score2': lambda: calculations.Score_cards2(extracted_text, job_description),
        'strengths': lambda: calculations.Strenths(extracted_text, job_description),
        'weakness': lambda: calculations.Worst_point(extracted_text, job_description),
    }
    
    results = {}
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=len(tasks)) as executor:
        future_to_key = {executor.submit(task): key for key, task in tasks.items()}
        for future in concurrent.futures.as_completed(future_to_key):
            key = future_to_key[future]
            try:
                results[key] = future.result()
                print(f"Completed: {key}")
            except Exception as exc:
                results[key] = None
                print(f"Error in {key}: {exc}")
    
    return results

def get_data(job_description, additional_information, extracted_text,company,position):
    final_resume = calculations.resume_final(extracted_text, additional_information)
    results = run_parallel_tasks(final_resume, job_description, extracted_text)
    error_response = {
        "error": "An error occurred while processing the data",
        "details": {}
    }
    def safe_get(dict_obj, *keys):
        for key in keys:
            if dict_obj is not None and isinstance(dict_obj, dict) and key in dict_obj:
                dict_obj = dict_obj[key]
            else:
                return None
        return dict_obj
    
    sc2 = results["score1"]
    sc1 = results["score2"]
    merged_score = {
            "score_card": {
                **sc1["score_card2"],
                **sc2["score_card1"]
                }
            }
    co1 = results["courses1"]
    co2 = results["courses2"]

    merged_cours = f"""{{
        "output": {{
            "course_impact": {json.dumps(co1["course_impact"])},
            "suggestion1":{json.dumps(co2["s1"])},
            "suggestion2": {json.dumps(co2["s2"])},
            "suggestion3": {json.dumps(co2["s3"])}
            
        }}
        }}"""
    
    merged_course = json.loads(merged_cours)
    print(results["experience2"],",xe")
    # Populate the response, using error messages for any missing data
    response = {
        "score_card":merged_score["score_card"],

        "project_impact": safe_get(results, 'projects', "output", "project_impact") or error_response["details"].setdefault("project_impact", "Failed to analyze projects"),
        "skill_Score": safe_get(results, 'skills', "output", "skill_Score") or error_response["details"].setdefault("skill_Score", "Failed to analyze skills"),
        "recommendations": safe_get(results, 'skills', "output", "recommendations") or error_response["details"].setdefault("recommendations", "No recommendations available"),
        "course_impact": merged_course["output"],
        "experience_relevance": safe_get(results, 'experience', "output", "experience_relevance") or error_response["details"].setdefault("experience_relevance", "Failed to analyze experience"),
        "Actionable Recommendations": results["experience2"]["Actionable Recommendations"],
        "Strengths": safe_get(results, 'strengths', "output") or error_response["details"].setdefault("Strengths", "Failed to identify strengths"),
        "Weaknesses": safe_get(results, 'weakness', "output") or error_response["details"].setdefault("Weaknesses", "Failed to identify weaknesses"),
        # "recommended_People_linkdin": [
        #     {
        #         "name": "Doe",
        #         "title": "Senior Soft... ",
        #         "link": f"""site:linkedin.com "microsoft" "Software Engineer" -jobs -job"""
        #     },
        # https://cr.linkedin.com/in/c4rlosgs
        # ],
        # "recommendedPeople_twitter": [
        #     {
        #         "name": "John Doe",
        #         "title": "Senior Soft... ",
        #         "link": f"""site:twitter.com "Software Engineer" "Microsoft" in bio"""
        #     }
        # ],
        # "recommendedPeople_instagram": [
        #     {
        #         "name": "John",
        #         "title": "Senior Soft... ",
        #         "link": """site:instagram.com "Software Engineer" "@Microsoft" -reel -p/"""
        #     }       
        # ],

        'recommended_People_linkdin': fetchPeoples.linkedin(company,position),
        'recommendedPeople_twitter': fetchPeoples.twitter(company,position),
        'recommendedPeople_instagram': fetchPeoples.instagram(company,position)
    
    }
    
    # If any errors occurred, include them in the response
    if error_response["details"]:
        response["errors"] = error_response["details"]

    return response

import apis



@app.route('/submit', methods=['POST'])
def submit():
    data = request.json
    job_description = data.get('job_description', '')
    additional_information = data.get('additional_information', '')
    extracted_text = data.get('extractedText', '')
    api_key = data.get('api', '')
    company = data.get('company', '')
    position = data.get('position', '')
    print("----------------------   -------------",company,position,api_key,"-----------------------------------")
    apis.API_func(api_key)
    
    output = get_data(job_description, additional_information, extracted_text,company,position)
    return jsonify(output)
 
if __name__ == '__main__':
    app.run(debug=True, port=5000)