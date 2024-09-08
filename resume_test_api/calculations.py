from langchain_groq import ChatGroq
import json
import apis
import prompts
import threading
import concurrent.futures
import time
from datetime import datetime
from dotenv import load_dotenv


'''
ChatGroq -> model library with integrated functionality of langchain
json-> to convert text into json 
apis -> where my model is calling
prompts -> All of my prompts for conversation 
threading -> for the parallel processing
concurrent.futures -> part of parallel processing 
time -> for time calculation
datetime -> for mongo db insertion timeing status
load_dotenv -> taking env file
os -> to get env
uuid -> used for mongo db unique key identifire
'''


'''
----------Timout Seconds----------
why -> sometimes model is running for more then 1 minutes which is not possible for lambda function that's why using custom time constrant to ensure model do not exceed lambda funciton
'''
TIMEOUT_SECONDS = 200  # it is a model running time 




'''
--------- threading.Lock()----------
why -> So that while adding data into the list called all_output  
every data did not append at the same time during the parallel processing 
that's why threading.Lock() lock the resourses and only allow one thread to access the code at a time 
'''
results_lock = threading.Lock()  # Lock to ensure thread-safe access to results

# Maximum retry attempts
MAX_RETRIES = 1 # so that it stop after 8 seconds

'''
-------- Mongo DB insertion Code ------
Below Code is a part where i want to insert data into mongo db without any problem 
'''
results = [None, None]

def fetch_data_with_retry(prompt, index, retry_count):
    for attempt in range(retry_count):
        try:
            response = apis.final(prompt,"resume")
            data = response.split("```")[1]
            with results_lock:
                results[index] = data
            return True
        except Exception as e:
            print(f"Attempt from resume {attempt + 1} failed with error: {e}")
    return False


"""
----resume_input1----
this fucntion is creating a final prompt
and taking data from the function 
(Why not return)
becuase i have put data into the list so i don't need to return anything 
-----Why Need to make it too much complex in nature--------
-> This is the primary Part in the Flow if it will not give me any result then every thing will be corrupted.
-> there are ways to do it more efficiently but now it is a main part of the process any small error will lead to problem ( that's why didn't try to change from the Biggning)

-- Detail about the Code --

- resume_final() is a Main Function which is doing multitasking resume_input1 and resume_input2 are other fucntions which are giving me 
the output

resume_input1 ->  give me all of the things including projects, skills, courses etc.
resume_input2 -> only giving me experience 

Why -> 
1. sometimes experience was very large which cause the trouble of time on the serverless function 
2. by doing this time get reduced 

Future Thoughts -

1. there will be another api which will tell me the count of sections on the resume 
for ex-
skills : 30,
experience : 300,
courses: 10,

then which has too much thing to extract will get on the resume2 other will be on the resume1 which will lead to reduce the time with more optimization

----Start of Resume Extraction----

"""
def resume_input1(resume_text1, additional_information, index):
    resume_content_prompt1 = f"""{prompts.resume_prompt1}
    {resume_text1}
    #Additional information of candidate
    {additional_information}"""
    
    success = fetch_data_with_retry(resume_content_prompt1, index, MAX_RETRIES)
    if success:
        print("done1")
    else:
        print("Failed to process resume_text1")

def resume_input2(resume_text, additional_information, index):
    resume_content_prompt = f"""{prompts.resume_prompt2}
    {resume_text}
    #Additional information of candidate#
    {additional_information}
    ###Important Notice###
    #Do not Ignore Any thing which is present in resume includeing skills experience etc. you know every thing
    # Only add experience which user has taken from the company not from projects"""
    
    success = fetch_data_with_retry(resume_content_prompt, index, MAX_RETRIES)
    if success:
        print("done2")
    else:
        print("Failed to process resume_text")

def resume_final(resume_text, additional_information):
    start_time = time.time()
    thread1 = threading.Thread(target=resume_input1, args=(resume_text, additional_information, 0))
    thread2 = threading.Thread(target=resume_input2, args=(resume_text, additional_information, 1))

    thread1.start()
    thread2.start()

    thread1.join()
    thread2.join()

    res1 = results[0]
    res2 = results[1]

    try:
        
        res1 = json.loads(res1) if res1 else "non"
        res2 = json.loads(res2) if res2 else "non"
        if res1 and res2:
            res1["experience"] = res2["experience"]

        res1["skills"]
        res1["projects"]
        res1["courses"]
        res1["role_user_candidate"]
        res1["education"]
    except json.JSONDecodeError as e:
        print("getting problem in resume")
        print(f"JSON decoding error: {e}")
        res1 = None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        res1 = resume_text
    end_time = time.time()
    time_taken = end_time - start_time
    # Print the time taken
    print(f"Time taken by Final Resume: {time_taken:.2f} seconds")

    return res1

"""
--- End of features from Resume Extraction ---

"""

def skills_taken(resume_text, job_description):
    start_time = time.time()
    for attempt in range(MAX_RETRIES):
        try:
            if resume_text is None or "skills" not in resume_text:
                print("Invalid resume_text or missing skills")
                return None

            skill = f"""{prompts.skills_prompt}
                ###Job Description###
                {job_description}
                ###Resume###
                {resume_text["skills"]}
            """

            with concurrent.futures.ThreadPoolExecutor() as executor:
                future = executor.submit(apis.final, skill, "skills")
                try:
                    response = future.result(timeout=TIMEOUT_SECONDS)
                except concurrent.futures.TimeoutError:
                    print(f"Attempt from skills {attempt + 1} timed out")
                    # Return timeout-specific JSON response
                    return json.loads("""{
                        "output": {
                            "skill_Score": {
                                "skills_ratio": {
                                    "time out ": 5,
                                    "time out 1": 0,
                                    "Error Occured": 0
                                },
                                "advice": "An error Occurred At this function"
                            },
                            "recommendations": [
                                "Please Tell the author There is something wrong in this code",
                                "There is some problem from the code",
                                "Having trouble on Finding Recommendations"
                            ]
                        }
                    }""")

            skill_splited = response.split("```")[1]
            d = json.loads(skill_splited)
            d["sr"]
            d["rec"]
            merged = f"""{{
                    "output": {{
                        "skill_Score": {{
                            "skills_ratio": {json.dumps(d["sr"])}
                        }},
                        "recommendations": {json.dumps(d["rec"])}
                    }}
                }}"""
            end_time = time.time()
            time_taken = end_time - start_time
            
            # Print the time taken
            print(f"Time taken by skills Taken: {time_taken:.2f} seconds")

            return json.loads(merged)

        except Exception as e:
            print(f"Attempt from skills {attempt + 1} failed with error: {e}")
            # Return error-specific JSON response
            end_time = time.time()
            time_taken = end_time - start_time
            # Print the time taken
            print(f"Time taken by Final Resume: {time_taken:.2f} seconds")


            return json.loads("""{
                "output": {
                    "skill_Score": {
                        "skills_ratio": {
                            "Please Put the Complaint there is some error on this function. Skill function is not working correctly": 5,
                            "Error Continue": 0,
                            "Error Occured": 0
                        },
                        "advice": "An error Occurred At this function"
                    },
                    "recommendations": [
                        "Please Tell the author There is something wrong in this code",
                        "There is some problem from the code",
                        "Having trouble on Finding Recommendations"
                    ]
                }
            }""")

    # If all retries fail without specific timeout or exception handling
    skills_taken_error = """{
        "output": {
            "skill_Score": {
                "skills_ratio": {
                    "Error Occured": 5,
                    "Error Continue": 0,
                    "time out ": 0
                },
                "advice": "An error Occurred At this function"
            },
            "recommendations": [
                "Please Tell the author There is something wrong in this code",
                "There is some problem from the code",
                "Having trouble on Finding Recommendations"
            ]
        }
    }"""
    end_time = time.time()

    time_taken = end_time - start_time
    # Print the time taken
    print(f"Time taken by Final Resume: {time_taken:.2f} seconds")


    return json.loads(skills_taken_error)



def projects_done(resume_text, job_description):
    start_time = time.time()
    for attempt in range(MAX_RETRIES):
        try:
           
            project = f"""{prompts.project_prompt}
                ###Job Description###
                {job_description}
                ###Resume###
                {resume_text["projects"]}
            """

            with concurrent.futures.ThreadPoolExecutor() as executor:
                future = executor.submit(apis.final, project, "projects")
                try:
                    Projects = future.result(timeout=TIMEOUT_SECONDS)
                except concurrent.futures.TimeoutError:
                    print(f"Attempt from projects {attempt + 1} timed out")
                    # Return timeout-specific JSON response
                    return json.loads("""{
                        "output": {
                            "project_impact": {
                                "impact": {
                                    "time out ": 5,
                                    "time out 1": 0,
                                    "Error Occurred": 0
                                },
                                "advice": "An error occurred At this function",
                                "suggestion1": "Please Tell the author There is something wrong in this code",
                                "suggestion2": "There is some problem from the code",
                                "suggestion3": "Having trouble on Finding Recommendations"
                            }
                        }
                    }""")

            projects_splitted = Projects.split("```")[1]
            d = json.loads(projects_splitted)
            md = f"""{{
                "output": {{
                    "project_impact": {{
                        "impact":{json.dumps(d["imp1"])},                        
                        "suggestion1": {json.dumps(d["s1"])},
                        "suggestion2": {json.dumps(d["s2"])},
                        "suggestion3": {json.dumps(d["s3"])}
                    }}
                }}
            }}"""
            end_time = time.time()
            time_taken = end_time - start_time
            # Print the time taken
            print(f"Time taken by Projects_done: {time_taken:.2f} seconds")
            return json.loads(md)
        
        except Exception as e:
            print(f"Attempt from projects {attempt + 1} failed with error: {e}")
            # Return error-specific JSON response
            return json.loads("""{
                "output": {
                    "project_impact": {
                        "impact": {
                            "An Error Occurred": "5",
                            "Error Continue": 0,
                            "Error Continue1": 0
                        },
                        "advice": "An Error Occurred At this part.",
                        "suggestion1": "Something Went Wrong1!",
                        "suggestion2": "Something Went Wrong2!",
                        "suggestion3": "Something Went Wrong3!"
                    }
                }
            }""")

    # If all retries fail without specific timeout or exception handling
    project_error = """{
        "output": {
            "project_impact": {
                "impact": {
                    "Error Occurred": "5",
                    "Error Continue": 0,
                    "Error Continue1": 0
                },
                "advice": "An Error Occurred At this part.",
                "suggestion1": "Something Went Wrong1!",
                "suggestion2": "Something Went Wrong2!",
                "suggestion3": "Something Went Wrong3!"
            }
        }
    }"""
    end_time = time.time()

    time_taken = end_time - start_time
    # Print the time taken
    print(f"Time taken by Final Resume: {time_taken:.2f} seconds")


    return json.loads(project_error)



def courses_done1(resume_text, job_description):
    start_time = time.time()
    for attempt in range(MAX_RETRIES):
        try:
            course = f"""{prompts.course_prompt1}
                ###Job Description###
                {job_description}
                ###Course_Presented_In_Resume###
                {resume_text["courses"]}
            """

            with concurrent.futures.ThreadPoolExecutor() as executor:
                future = executor.submit(apis.final, course, "course1")
                try:
                    Courses = future.result(timeout=TIMEOUT_SECONDS)
                except concurrent.futures.TimeoutError:
                    print(f"Attempt course {attempt + 1} timed out")
                    # Return timeout-specific JSON response
                    return json.loads("""{
                        "course_impact": {
                            "impt": {
                                "time out ": 5,
                                "time out 1": 0,
                                "Error Occurred": 0
                            }
                        }
                    }""")

            course_splitted = Courses.split("```")[1]
            print(course_splitted,"course_splitted")
            d = json.loads(course_splitted)
            end_time = time.time()
            time_taken = end_time - start_time
            # Print the time taken
            print(f"Time taken by Course Done 1: {time_taken:.2f} seconds")
            
            return d

        except Exception as e:
            print(f"Attempt course {attempt + 1} failed with error: {e}")
            # Return error-specific JSON response
            return json.loads("""{
                "course_impact": {
                    "impt": {
                        "An Error Occurred": 5,
                        "An Error Occurred1": 0,
                        "An Error Occurred2": 4
                    }
                }
            }""")

    # If all retries fail without specific timeout or exception handling
    course_error = """{
        "course_impact": {
            "impt": {
                "An Error Occurred": 5,
                "An Error Occurred1": 0,
                "An Error Occurred2": 4
            }
        }
    }"""
    end_time = time.time()

    time_taken = end_time - start_time
    # Print the time taken
    print(f"Time taken by corses error: {time_taken:.2f} seconds")
    return json.loads(course_error)


def courses_done2(resume_text, job_description):
    start_time = time.time()

    for attempt in range(MAX_RETRIES):
        try:
            course = f"""{prompts.course_prompt2}
                ###Job Description###
                {job_description}
                ###Course_Presented_In_Resume###
                {resume_text["courses"]}
            """
            with concurrent.futures.ThreadPoolExecutor() as executor:
                future = executor.submit(apis.final, course, "course2")
                try:
                    Courses = future.result(timeout=TIMEOUT_SECONDS)
                except concurrent.futures.TimeoutError:
                    print(f"Attempt course {attempt + 1} timed out")
                    # Return timeout-specific JSON response
                    return json.loads("""{
                            "s1": "Time out occurred while processing.",
                            "s2": "Please try again later.",
                            "s3": "The system encountered a delay."
                    }""")

            course_splitted = Courses.split("```")[1]
            d = json.loads(course_splitted)
            
            end_time = time.time()
            time_taken = end_time - start_time
            # Print the time taken
            print(f"Time taken by course done2: {time_taken:.2f} seconds")
            
            return d

        except Exception as e:
            print(f"Attempt course {attempt + 1} failed with error: {e}")
            # Return error-specific JSON response
            return json.loads("""{
                
                    "s1": "Something Went Wrong1!",
                    "s2": "Something Went Wrong2!",
                    "s3": "Something Went Wrong3!"
                
            }""")

    # If all retries fail without specific timeout or exception handling
    course_error = """{
        
            "s1": "Something Went Wrong1!",
            "s2": "Something Went Wrong2!",
            "s3": "Something Went Wrong3!"
    }"""
    end_time = time.time()

    time_taken = end_time - start_time
    # Print the time taken
    print(f"Time taken by Final Resume: {time_taken:.2f} seconds")


    return json.loads(course_error)


def experience_done(resume_text, job_description):
    start_time = time.time()

    for attempt in range(MAX_RETRIES):
        try:
           
            experience = f"""{prompts.exp_prompt}
                ###Job Description###
                {job_description}
                ###Experience_Presented_In_Resume###
                {resume_text["experience"]}"""

            with concurrent.futures.ThreadPoolExecutor() as executor:
                future = executor.submit(apis.final, experience, "experience")
                try:
                    experience1 = future.result(timeout=TIMEOUT_SECONDS)
                except concurrent.futures.TimeoutError:
                    print(f"Attempt experience {attempt + 1} timed out")
                    return json.loads("""{
                        "output": {
                            "experience_relevance": {
                                "imp": {
                                    "time out ": 5,
                                    "time out 1": 0,
                                    "Error Occurred": 0
                                },
                                "advice": "An error occurred at the experience part. Please share the information with the developer."
                            }
                          
                        }
                    }""")

            exp = experience1.split("```")[1]
            print(exp,"checking calculations")
            d = json.loads(exp)
            
            end_time = time.time()
            time_taken = end_time - start_time
            # Print the time taken
            print(f"Time taken by experience_done: {time_taken:.2f} seconds")
            print("experience_done")
            
            return d

        except Exception as e:
            print(f"Attempt experience {attempt + 1} failed with error: {e}")
            return json.loads("""{
                "output": {
                    "experience_relevance": {
                        "imp": {
                            "An Error Occurred": 0,
                            "An Error Occurred1": 0,
                            "An Error Occurred2": 0
                        },
                        "advice": "An error occurred at the experience part. Please inform the author."
                    }
                }
            }""")

    # If all retries fail without specific timeout or exception handling
    experience_error = """{
        "output": {
            "experience_relevance": {
                "imp": {
                    "An Error Occurred": 0,
                    "An Error Occurred2": 0,
                    "An Error Occurred1": 0
                },
                "advice": "An error occurred at the experience part. Please share the information with the developer."
            }
        }
    }"""
    end_time = time.time()

    time_taken = end_time - start_time
    # Print the time taken
    print(f"Time taken by Final Resume: {time_taken:.2f} seconds")


    return json.loads(experience_error)




def experience_done2(resume_text, job_description):
    start_time = time.time()
    for attempt in range(MAX_RETRIES):
        try:
            experience = f"""{prompts.exp_prompt2}
                ###Job Description###
                {job_description}
                ###Experience_Presented_In_Resume###
                {resume_text["experience"]}"""

            with concurrent.futures.ThreadPoolExecutor() as executor:
                future = executor.submit(apis.final, experience, "experience")
                try:
                    experience1 = future.result(timeout=TIMEOUT_SECONDS)
                except concurrent.futures.TimeoutError:
                    print(f"Attempt experience {attempt + 1} timed out")
                    return json.loads("""{
                       "Actionable Recommendations": [
                                "Please inform the author that an error occurred.",
                                "An error occurred at the experience part. Share the information with the developer.",
                                "An error occurred at the experience part. Please provide details to the developer."
                            ]
                        }
                    """)

            exp = experience1.split("```")[1]
            d = json.loads(exp)
            end_time = time.time()
            time_taken = end_time - start_time
            # Print the time taken
            print(f"Time taken by experience_done: {time_taken:.2f} seconds")
            return d

        except Exception as e:
            print(f"Attempt experience {attempt + 1} failed with error: {e}")
            return json.loads("""{                
                    "Actionable Recommendations": [
                        "An error occurred at the experience part. Share the information with the developer.",
                        "An error occurred at the experience part. Please provide details to the developer.",
                        "An error occurred at the experience part. Please inform the author."
                    ]
                }""")

    # If all retries fail without specific timeout or exception handling
    experience_error = """{
        
            "Actionable Recommendations": [
                "An error occurred at the experience part. Share the information with the developer.",
                "An error occurred at the experience part. Please provide details to the developer.",
                "An error occurred at the experience part. Please inform the author."
            ]
        
    }"""
    end_time = time.time()

    time_taken = end_time - start_time
    # Print the time taken
    print(f"Time taken by Final Resume: {time_taken:.2f} seconds")


    return json.loads(experience_error)




def Score_cards1(resume_text, job_description):
    start_time = time.time()
    for attempt in range(MAX_RETRIES):
        try:
            if resume_text is None:
                print("Invalid resume_text")
                return None

            Score_card = f"""{prompts.score_card_prompt1}
                ###Job Description###
                {job_description}
                ###Resume###
                {resume_text}"""

            with concurrent.futures.ThreadPoolExecutor() as executor:
                future = executor.submit(apis.final, Score_card, "scores1")
                try:
                    score_cards_output = future.result(timeout=TIMEOUT_SECONDS)
                except concurrent.futures.TimeoutError:
                    print(f"Attempt score {attempt + 1} timed out")
                    return json.loads("""{
                        "score_card1": {
                            "ranking": {
                                "score": 505,
                                "description": "Time out occurred!",
                                "reason": "The process took too long.",
                                "improvementTip": "Please try again later."
                            },
                            "keywords": {
                                "score": 505,
                                "description": "Time out occurred!",
                                "reason": "The process took too long.",
                                "improvementTip": "Please try again later."
                            }
                        }
                    }""")

            exp = score_cards_output.split("```")[1]
            d = json.loads(exp)

            end_time = time.time()
            time_taken = end_time - start_time
            # Print the time taken
            print(f"Time taken by Score Card: {time_taken:.2f} seconds")
            
            merge_score = {
                "score_card1": 
                {
                "ranking": d["ranking"],
                "keywords":d["keywords"]
                }
                }
            return merge_score

        except Exception as e:
            print(f"Attempt score {attempt + 1} failed with error: {e}")
            return json.loads("""{
                "score_card1": {
                    "ranking": {
                        "score": 505,
                        "description": "Error Occurred!",
                        "reason": "An error occurred.",
                        "improvementTip": "Check the input or try again."
                    },
                    "keywords": {
                        "score": 505,
                        "description": "Error Occurred!",
                        "reason": "An error occurred.",
                        "improvementTip": "Check the input or try again."
                    }
                }
            }""")

    # If all retries fail without specific timeout or exception handling
    experience_error = """{
        "score_card1": {
            "ranking": {
                "score": 505,
                "description": "Error Occurred!",
                "reason": "An error occurred.",
                "improvementTip": "Check the input or try again."
            },
            "keywords": {
                "score": 505,
                "description": "Error Occurred!",
                "reason": "An error occurred.",
                "improvementTip": "Check the input or try again."
            }
        }
    }"""
    end_time = time.time()

    time_taken = end_time - start_time
    # Print the time taken
    print(f"Time taken by Final Resume: {time_taken:.2f} seconds")


    return json.loads(experience_error)


def Score_cards2(resume_text, job_description):
    start_time = time.time()
    for attempt in range(MAX_RETRIES):
        try:
            if resume_text is None:
                print("Invalid resume_text")
                return None

            Score_card = f"""{prompts.score_card_prompt2}
                ###Job Description###
                {job_description}
                ###Resume###
                {resume_text}"""

            with concurrent.futures.ThreadPoolExecutor() as executor:
                future = executor.submit(apis.final, Score_card, "scores2")
                try:
                    score_cards_output = future.result(timeout=TIMEOUT_SECONDS)
                except concurrent.futures.TimeoutError:
                    print(f"Attempt score {attempt + 1} timed out")
                    return json.loads("""{
                        "score_card2": {
                            "ats": {
                                "score": 505,
                                "description": "Time out occurred!",
                                "reason": "The process took too long.",
                                "improvementTip": "Please try again later."
                            },
                            "jd": {
                                "score": 505,
                                "description": "Time out occurred!",
                                "reason": "The process took too long.",
                                "improvementTip": "Please try again later."
                            },
                            "overall": {
                                "score": 505,
                                "description": "Time out occurred!",
                                "reason": "The process took too long.",
                                "improvementTip": "Please try again later."
                            }
                        }
                    }""")

            exp = score_cards_output.split("```")[1]
            d = json.loads(exp)
            
            end_time = time.time()
            time_taken = end_time - start_time
            # Print the time taken
            print(f"Time taken by Score Card 2: {time_taken:.2f} seconds")
                            
            mg_score = {
                "score_card2": 
                {
                    "ats":d["ats"],
                    "jd": 
                       d["jd"],
                    "overall": 
                        d["overall"]
                }
                }
            return mg_score

        except Exception as e:
            print(f"Attempt score {attempt + 1} failed with error: {e}")
            return json.loads("""{
                "score_card2": {
                    "ats": {
                        "score": 505,
                        "description": "Error Occurred!",
                        "reason": "An error occurred.",
                        "improvementTip": "Check the input or try again."
                    },
                    "jd": {
                        "score": 505,
                        "description": "Error Occurred!",
                        "reason": "An error occurred.",
                        "improvementTip": "Check the input or try again."
                    },
                    "overall": {
                        "score": 505,
                        "description": "Error Occurred!",
                        "reason": "An error occurred.",
                        "improvementTip": "Check the input or try again."
                    }
                }
            }""")

    # If all retries fail without specific timeout or exception handling
    score2_error = """{
        "score_card2": {
            "ats": {
                "score": 505,
                "description": "Error Occurred!",
                "reason": "An error occurred.",
                "improvementTip": "Check the input or try again."
            },
            "jd": {
                "score": 505,
                "description": "Error Occurred!",
                "reason": "An error occurred.",
                "improvementTip": "Check the input or try again."
            },
            "overall": {
                "score": 505,
                "description": "Error Occurred!",
                "reason": "An error occurred.",
                "improvementTip": "Check the input or try again."
            }
        }
    }"""
    end_time = time.time()

    time_taken = end_time - start_time
    # Print the time taken
    print(f"Time taken by Final Resume: {time_taken:.2f} seconds")

    return json.loads(score2_error)


def Strenths(resume_text, job_description):
    start_time = time.time()

    for attempt in range(MAX_RETRIES):
        try:
            if resume_text is None:
                print("Invalid resume_text")
                return None

            Strent_prompts = f"""{prompts.Strengths}
                ###Job Description###
                {job_description}
                ###Resume###
                {resume_text}"""

            with concurrent.futures.ThreadPoolExecutor() as executor:
                future = executor.submit(apis.final, Strent_prompts, "strength")
                try:
                    Strenths = future.result(timeout=TIMEOUT_SECONDS)
                except concurrent.futures.TimeoutError:
                    print(f"Attempt strengths {attempt + 1} timed out")
                    return json.loads("""{
                        "output": {
                            "Error point 1": "Time out occurred. Please try again later.",
                            "Error point 2": "Time out occurred. Please try again later.",
                            "Error point 3": "Time out occurred. Please try again later."
                        }
                    }""")

            exp = Strenths.split("```")[1]
            d = json.loads(exp)
            d["output"]
            end_time = time.time()
            time_taken = end_time - start_time
            # Print the time taken
            print(f"Time taken by Strenths: {time_taken:.2f} seconds")
            return d

        except Exception as e:
            print(f"Attempt strengths {attempt + 1} failed with error: {e}")
            return json.loads("""{
                "output": {
                    "Error point 1": "An error occurred. Please inform the author.",
                    "Error point 2": "An error occurred. Please inform the author.",
                    "Error point 3": "An error occurred. Please inform the author."
                }
            }""")

    # If all retries fail without specific timeout or exception handling
    Strenths_error = """{
        "output": {
            "Error point 1": "An error occurred. Please inform the author.",
            "Error point 2": "An error occurred. Please inform the author.",
            "Error point 3": "An error occurred. Please inform the author."
        }
    }"""
    return json.loads(Strenths_error)


def Worst_point(resume_text, job_description):
    start_time = time.time()
    for attempt in range(MAX_RETRIES):
        try:
            if resume_text is None:
                print("Invalid resume_text")
                return None

            weekness_ponts = f"""{prompts.Weekness}
                ###Job Description###
                {job_description}
                ###Resume###
                {resume_text}"""

            with concurrent.futures.ThreadPoolExecutor() as executor:
                future = executor.submit(apis.final, weekness_ponts, "weekness")
                try:
                    worst_point = future.result(timeout=TIMEOUT_SECONDS)
                except concurrent.futures.TimeoutError:
                    print(f"Attempt weaknesses {attempt + 1} timed out")
                    return json.loads("""{
                        "output": {
                            "Error point 1": "Time out occurred. Please try again later.",
                            "Error point 2": "Time out occurred. Please try again later.",
                            "Error point 3": "Time out occurred. Please try again later."
                        }
                    }""")

            exp = worst_point.split("```")[1]
            d = json.loads(exp)
            d["output"]
            end_time = time.time()
            time_taken = end_time - start_time
            # Print the time taken
            print(f"Time taken by Worst point: {time_taken:.2f} seconds")
            return d

        except Exception as e:
            print(f"Attempt weaknesses {attempt + 1} failed with error: {e}")
            return json.loads("""{
                "output": {
                    "Error point 1": "An error occurred. Please inform the author.",
                    "Error point 2": "An error occurred. Please inform the author.",
                    "Error point 3": "An error occurred. Please inform the author."
                }
            }""")

    # If all retries fail without specific timeout or exception handling
    worst_error = """{
        "output": {
            "Error point 1": "An error occurred. Please inform the author.",
            "Error point 2": "An error occurred. Please inform the author.",
            "Error point 3": "An error occurred. Please inform the author."
        }
    }"""
    end_time = time.time()
    time_taken = end_time - start_time
    # Print the time taken
    print(f"Time taken by Final Resume: {time_taken:.2f} seconds")


    return json.loads(worst_error)

