resume_prompt1 = """
###Instruction###

Act as an expert in the field of ATS (Applicant Tracking Systems).
Your Task is to Saprate every thing from the resume 
you have to saprate these sections 
# points should be saprerated by (,)

1. skills.
3. projects.
4. courses.
5. education.

###FORMAT###

Please return the extracted data in the correct JSON format:
# points should be saprerated by (,)

Json should be under (```)
```
{
"skills": "{only return the section of Skills of the Candidate}",
"projects": "{only return the section of Projects of the Candidate}",
"courses": "{only return the course of the Candidate }"
"role_user_candidate": "{only return the Roles (which position in company) for the Candidate}"
"education": "{only return the section of Education of the Candidate}",
}
```
# this includes His Graduation , Education, Certification, Courses.
#remember json should be closed properly
#if there is something which is not present just give the "__":"Not present" in json
#you are in a process so do not give anything else  and json should be between ``` quotes
#remember json output should be correctly into json because it will be used in the code further
###Resume###

"""

resume_prompt2 = """
###Instruction###

Act as an expert in the field of ATS (Applicant Tracking Systems).
Your Task is to Saprate experience from the resume 
you have to saprate ONLY experience 
2. experience.

###FORMAT###

Please return the extracted data in the correct JSON format do not put any points add comma insted of points :
Json should be under (```)
```
{

"experience": "{only return the section of Experience of the Candidate saprated with (,) every point will be saprated by , and if exprence is not present give None in this value }",

}
```
#remember json output should be correctly into json because it will be used in the code further
#you are in a process so do not give anything else  and json should be between ``` quotes
###Resume###

"""

score_card_prompt1 = """
###Instruction###

You are an expert in the field of ATS (Applicant Tracking Systems) and job descriptions. Your task is to evaluate a user's resume against a provided job description. You will provide genuine scores based on the resume.
Conduct a deep-dive review of the existing resume and job description.
Your goal is to help improve the resume, making it exceptional and removing any vulnerabilities.
so do not give the random scores 
you are the part of process so do not give any thing else it do not give any value to that project 
###FORMAT###
The output should be in the following format:
Json should be under (```)
```
{
"ranking": 
{
    "score": "What is the Resume Ranking Score of this resume compared to job description (Score Number ex- 30, 40, 50)",
    "description": "Example -> Moderate ATS compatibility potential (will be change according to the score)", 
    "reason": "Reasion under 12 words",
    "improvementTip": "Small tip on Ranking under 12 words"
},
"keywords":
{
    "score": "What is the Keywords Score of this resume compared to job description (Score Number ex- 30, 40, 50)",
    "description": "Example -> Moderate ATS compatibility potential (will be change according to the score)", 
    "reason": "Reasion under 12 words",
    "improvementTip": "Small tip on keywords under 12 words"
}

}


```
#remember json should be closed properly
#you are in a process so do not give anything else  and json should be between ``` quotes
"""

score_card_prompt2 = """
###Instruction###

You are an expert in the field of ATS (Applicant Tracking Systems) and job descriptions. Your task is to evaluate a user's resume against a provided job description. You will provide genuine scores based on the resume.
Conduct a deep-dive review of the existing resume and job description.
Your goal is to help improve the resume, making it exceptional and removing any vulnerabilities.
so do not give the random scores 
you are the part of process so do not give any thing else it do not give any value to that project 
###FORMAT###
The output should be in the following format:
Json should be under (```)
```
{

"ats":
{
    "score":" What is the ATS Score of this resume compared to job description (Score Number ex- 30, 40, 50)",
    "description": " Example -> Moderate ATS compatibility potential (will be change according to the score)", 
    "reason": "Reasion under 12 words",
    "improvementTip": "Small tip under 12 words"
},
"jd": 
{
    "score": "What is the Job Description match Score of this resume compared to job description (Score Number ex- 30, 40, 50)",
    "description": " Example -> Moderate ATS compatibility potential (will be change according to the score)", 
    "reason": "Reasion under 12 words",
    "improvementTip": "Small tip on aligning resume with jd under 12 words"
},
"overall": 
{
    "score": "What is the Overall Score of this resume compared to job description (Score Number ex- 30, 40, 50)",
    "description": "Example -> Moderate ATS compatibility potential (will be change according to the score)", 
    "reason": "Reasion under 12 words",
    "improvementTip": "Small tip on aligning everything under 12 words"
}

}
```
#remember json should be closed properly
#you are in a process so do not give anything else  and json should be between ``` quotes and do not give anything else i want only this
"""




project_prompt = """
###Instruction###

You are an expert in the field of ATS (Applicant Tracking Systems) and job descriptions. Your task is to evaluate a user's resume against a provided job description. You will provide excellent advice and genuine scores based on the resume, focusing on the impacts on the project as outlined in the job description.
Conduct a deep-dive review of the existing resume and job description.
Provide feedback that balances solving the immediate problem with long-term improvement.
Discuss trade-offs and implementation options if there are choices to be made.
Ensure that all feedback accurately reflects the job description.
Your goal is to help improve the resume, making it exceptional and removing any vulnerabilities.
you are the part of process so do not give any thing else it do not give any value to that project 
#if project is not present in the resume you have to say "Project Not preset":0 and at the section of suggestion = No Suggestions for project 
do not give any sign into the name insted give the full name (example - C++ to CPP Programing)
###FORMAT###
The output should be in the following format:
Json should be under (```)
```
{
"imp1": {
    "project_name1": (Score Number ex- 34),
    "project_name2": (Score Number ex- 27),
    "project_name3": (Score Number ex- 71),
    "project_name4": (Score Number ex- 52),
    ....
    "project n": (Score Number ex- 99)
    },
    "s1": "What needs to be done to get selected for this job description? Highlight the business impact of specific projects.",
    "s2": "Which project is not making any sense for this job description? Highlight the business impact of specific projects.",
    "s3": "What keywords should be added in these projects to enhance their relevance? Highlight the business impact of specific projects."
}      
    ```
    points to be remember 
    do not change s1,s2,s3 keys you have do change values
    #suggestions should be very short and clear try to put that into 15-20 words do not repeat things this part should be strongly focus on projects
    #suggestion should be seem like candidate get know something new and valueable
        #only give the name of project and number nothting  and those which are less relevent to the job description give them less values and which are not giving any value give them 0 you can apply negetive too
    #remember json should be closed properly
"""


skills_prompt = """
###Instruction###
You are an expert in the field of ATS (Applicant Tracking Systems) and job descriptions. Your task is to evaluate a user's resume against a provided job description.
You will provide excellent advice and genuine scores based on the resume, focusing on the impacts on the skills as outlined in the job description.

Conduct a deep-dive review of the existing resume and job description.
Provide feedback that balances solving the immediate problem with long-term improvement.

Discuss trade-offs and implementation options if there are choices to be made.
Ensure that all feedback related to skills should accurately reflects the job description.
Your goal is to help improve the resume, making it exceptional and removing any vulnerabilities.
you are the part of process so do not give any thing else it do not give any value to that project 
#if you didn't find any skill on resume just tell in json that "No skill found":0 
###FORMAT###
The result should be in the following format:
Json should be under (```)
```
{ "sr": {
    "skill1": (Score Number ex- 71),
    "skill2": (Score Number ex- 21),
    "skill3": (Score Number ex- 34),
    "skill4": (Score Number ex- 36),
    "skill n": (Score Number ex- 23)
},
"rec": [
    "recommendation1 on the Skills  ( with the telling about market demand under 10-15 words)",
    "recommendation2 on the Skills  ( with the telling about market demand under 10-15 words)",
    "recommendation3 on the Skills  ( with the telling about market demand under 10-15 words)"
]    
}
```
#list every skills which user has presented in resume 
#do not add any skill which is not present in resume 
#do not involve the skills which is present in Job description but not in the resume
#recommendations should be very short and clear try to put that into 15-20 words it should be focused on skills
#remember json should be closed properly
#do not give any kind of signs into the json output answer insted give the full name (example -> C++ to CPP Programing)
        """


course_prompt1 = """
###Instruction###
You are an expert in the field of ATS (Applicant Tracking Systems) and job descriptions.
 Your task is to evaluate a user's resume courses against a provided job description.
   You will provide excellent advice and genuine scores based on the resume course, focusing on the impacts on the courses as outlined in the job description.

Conduct a deep-dive review of the existing courses of resume and job description.
Provide feedback that balances solving the immediate problem with long-term improvement.

Discuss trade-offs and implementation options if there are choices to be made.
Ensure that all feedback accurately reflects the job description.
Your goal is to help improve the resume, making it exceptional and removing any vulnerabilities.


###FORMAT###
The output should be in the correct json  format which follow this format:
Json should be under (```)
```
{
"course_impact": {
    "impt": {
    "course1": (Score Number ex- 11),
    "course2": (Score Number ex- 72),
    "course3": (Score Number ex- 19),
    "couse n ": (Score Number ex- 14)
}
}
}
```
you are the part of process so do not give any thing else it do not give any value and it will increase the output time
#if you didn't find any courses on resume just give in json "No courses found" : 0 
do not give any sign into the name insted give the full name (example - C++ to CPP Programing)
        """

course_prompt2 = """
###Instruction###
You are an expert in the field of ATS (Applicant Tracking Systems) and job descriptions.
 Your task is to evaluate a user's resume courses against a provided job description.
   You will provide excellent advice and genuine scores based on the resume course, focusing on the impacts on the courses as outlined in the job description.

Conduct a deep-dive review of the existing courses of resume and job description.
Provide feedback that balances solving the immediate problem with long-term improvement.

Discuss trade-offs and implementation options if there are choices to be made.
Ensure that all feedback accurately reflects the job description.
Your goal is to help improve the resume, making it exceptional and removing any vulnerabilities.


###FORMAT###
The output should be in the correct json  format which follow this format:
Json should be under (```)
```

{
"s1": "what needs to be done to get selected for this job description ",
"s2": "which project is not making any sense for this job description",
"s3": "what keywords you should add in this projects "
}

```
#suggestions should be very short and clear try to put that into 15-20 words and it should be focused on what can be achive in short period nothing should sound ideal and only give 3-4 suggestions
you are the part of process so do not give any thing else it do not give any value and it will increase the output time
#if you didn't find any courses on resume just give in json "No courses found" : 0 
do not give any sign into the name insted give the full name (example - C++ to CPP Programing)
        """


exp_prompt = """
###Instruction###
Act as an expert in the field of ATS (Applicant Tracking Systems) and job descriptions. Your task is to evaluate a user's work experience section of the resume against a provided job description. You will provide genuine scores based on the work experience, focusing solely on the professional experience as outlined in the job description.

Conduct a deep-dive review of the existing work experience and job description.
Ensure that all feedback accurately reflects the job description requirements.
Your goal is to help improve the work experience section of the resume, making it exceptional and relevant to the job.

You are part of a process, so do not provide any additional information that doesn't add value to the evaluation.
If you don't find any work experience on the resume, just return "No experience found": 0 in the JSON.
Do not use abbreviations in experience names; instead, use full names (example: use "CPP Programming" instead of "C++").

###FORMAT###
The output should be in the following format:
Json should be under (```)
```
{
    "output":{
    "experience_relevance":{"imp": {
        "expeience name 1": (Score Number ex- 11),
        "expeience name 2":  (Score Number ex- 32),
        ...
        "expeience name  n":  (Score Number ex- 39)
    }
    }
    }
}



```
Only give the Experience present in the resume Not any other experience
Work experience is a work done in the company Not on the college or any other place or projects

"""



exp_prompt2 = """
###Instruction###
act as an expert in the field of ATS (Applicant Tracking Systems) and job descriptions. 
Your task is to evaluate a user's resume against a provided job description. You will provide excellent advice based on the resume,
 focusing on the impacts on the work Experience as outlined in the job description.

Conduct a deep-dive review of the existing resume and job description.
Provide feedback that balances solving the immediate problem with long-term improvement.

Discuss trade-offs and implementation options if there are choices to be made.
Ensure that all feedback accurately reflects the job description.
Your goal is to help improve the resume, making it exceptional and removing any vulnerabilities.

you are the part of process so do not give any thing else it do not give any value to that project 

###FORMAT###
The output should be in the following format:
Json should be under (```)
```
{ 
 "Actionable Recommendations": [
    "Recommendation1  to  the person what will make the resume stand out from others on the job at future ( with the telling about market demand on future).",
    "Recommendation2  to  the person what will make the resume stand out from others on the job at future ( with the telling about market demand on future).",
    "Recommendation3  to  the person what will make the resume stand out from others on the job at future ( with the telling about market demand on future)."
]
}
```
#json format should be valid json
#experience is a work done in the company 
#suggestions should be very short and clear try to put that into 15-20 words and it should be focused on what can be achive in short period nothing should sound ideal
#only give 3-4 points
"""



Strengths = """
###Instruction###
You are an expert in the field of ATS (Applicant Tracking Systems) and job descriptions.
Your task is to evaluate a user's resume against a provided job description. 
You will provide excellent advice based on the resume, 
focusing on the impacts on the Strengths of resume as outlined in the job description.

Conduct a deep-dive review of the resume and job description.
Provide feedback that balances solving the immediate problem with long-term improvement.

Discuss trade-offs and implementation options if there are choices to be made.
Ensure that all feedback accurately reflects the job description.
Your goal is to give the best part of resume for the job desciption.
you are the part of process so do not give any thing else it do not give any value to that project 
do not give any sign into the name insted give the full name (example - C++ to CPP Programing)
###FORMAT###
The output should be in the following format:
Json should be under (```)
```
{
    "output": {
        "Strenght point 1": "Brief on Strenght point 1 (it should be very clear, Sort ,Valid).",
        "Strenght point 2": "Brief on Strenght point 2 (it should be very clear, Sort ,Valid).",
        "Strenght point 3": "Brief on Strenght point 3 (it should be very clear, Sort ,Valid)."
    }
}
#suggestions should be very short and clear try to put that into 10-15 words and it should be focused on what can be achive in short period nothing should sound ideal

#remember json should be closed properly

            ```
"""



Weekness = """
###Instruction###
You are an expert in the field of ATS (Applicant Tracking Systems) and job descriptions.
Your task is to evaluate a user's resume against a provided job description. 
You will provide excellent advice based on the resume, 
focusing on the impacts on the Strengths of resume as outlined in the job description.

Conduct a deep-dive review of the resume and job description.
Provide feedback that balances solving the immediate problem with long-term improvement.

Discuss trade-offs and implementation options if there are choices to be made.
Ensure that all feedback accurately reflects the job description.
Your goal is to give the Worst part of resume for the job desciption.
you are the part of process so do not give any thing else it do not give any value to that project 
do not give any sign into the name insted give the full name (example - C++ to CPP Programing)
###FORMAT###
The output should be in the following format:
Json should be under (```)
```
{
    "output": {
        "Worst point 1": "Brief on Worst point 1 (it should be very clear, Sort ,Valid).",
        "Worst point 2": "Brief on Worst point 2 (it should be very clear, Sort ,Valid).",
        "Worst point 3": "Brief on Worst point 3 (it should be very clear, Sort ,Valid)."
    }
}
```
#it should be very short and clear try to put every point into 12-15 words not more then that
#remember json should be closed properly
#only give 3-4 points 
"""
