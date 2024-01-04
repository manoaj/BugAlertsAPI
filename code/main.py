from ast import List
from typing import List, Union

import paramiko
import Cred

from fastapi import Body, Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

import crud
import models
import schemas
from database import SessionLocal, engine
from schemas import candidateCreate
from schemas import tagCreate
from schemas import alertworthyCreate
from schemas import AlertworthyAdd
from schemas import CandidateAdd

app = FastAPI()


origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


models.Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/getCandidate/{bug_id}")
async def read_candidates(bug_id:int , db: Session = Depends(get_db)):
    db_bugs= crud.get_candidate(db,bug_id)
    if(db_bugs == None):
        return {"reponse":"data not found for bug_id: "+str(bug_id)}
    return db_bugs

@app.get("/getAll/Candidates")
async def read_all_candidates(skip: int = 0, db: Session = Depends(get_db)):
    db_bugs= crud.get_all_candidates(db,skip=skip)
    if(len(db_bugs) == 0):
        return {"reponse":"Empty Bug List.Kindly create a bug"}
    return db_bugs

@app.get("/getAllUnassiged/Candidates")
async def read_all_unassigned_candidates(skip: int = 0, db: Session = Depends(get_db)):
    db_bugs= crud.get_all_unassigned_candidates(db,skip=skip)
    if(len(db_bugs) == 0):
        return {"reponse":"Empty Bug List.Kindly create a bug"}
    return db_bugs

@app.get("/getAllUserAssigned/Candidates")
async def read_all_user_candidates(skip: int = 0, db: Session = Depends(get_db)):
    db_bugs= crud.get_all_user_candidates(db,skip=skip)
    if(len(db_bugs) == 0):
        return {"reponse":"Empty Bug List.Kindly create a bug"}
    return db_bugs

@app.put("/create/candidateAll")
async def create_candidate(candidateRequest:List[schemas.candidateCreate],db:Session =Depends(get_db)):
    for candidate in candidateRequest:
        db_bugs= crud.create_all_candidate(db,candidate)
    return db_bugs

@app.put("/create/candidate/{bug_id}")
async def create_one_candidate(bug_id:int,candidateRequest:List[schemas.candidateCreate],db:Session =Depends(get_db)):
    for candidate in candidateRequest:
        db_bugs= crud.create_one_candidate(bug_id,db,candidate)
    return db_bugs

@app.delete("/delete/candidate/{bug_id}")
async def delete_candidate(bug_id:int, db:Session= Depends(get_db)):
    return crud.delete_candidate(db,bug_id)

# Route to receive POST requests with Candidate id
@app.post("/grab_candidate")
async def grab_candidate(candidate_data: CandidateAdd):
    # Print the Candidate id  to the terminal
    candidate_id = candidate_data.id

    print("Received candidate Data: "+str(candidate_id))

    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh_client.load_system_host_keys()
    ssh_client.connect(Cred.hostname, Cred.port, Cred.username, Cred.password)

    command = "b4 candidate "+str(candidate_id)
    stdin, stdout, stderr = ssh_client.exec_command(command)
    print (command)
    response = stdout.read().decode().strip("\n'")
    
    ssh_client.close()
    
    if response == ("Assigned candidate BUG"+str(candidate_id)+" to user "+Cred.username):
        print(response)
        return {"message": response}
    else:
        error_message = stderr.read().decode().strip("\n'")
        if error_message:
            print(error_message)
            return {"message": error_message}
        else:
            return {"message": "Unknown error occurred"}
   
   
   
    

@app.put("/create/tag")
async def create_tag(tagRequest:List[schemas.tagCreate], db:Session =Depends(get_db)):
    for tag in tagRequest:
        db_tags= crud.create_tag(db,tag)
    return db_tags

@app.get("/getAll/tags")
async def read_all_tags(skip: int = 0, db: Session = Depends(get_db)):
    db_tags= crud.get_all_tags(db,skip=skip)
    if(len(db_tags) == 0):
        return {"reponse":"Empty Tag List. Kindly create a tag"}
    return db_tags

@app.get("/getTagsContaining/{tag_contains}")
async def read_tags(tag_contains:str , db: Session = Depends(get_db)):
    db_tags= crud.get_tags_containing(db,tag_contains)
    if(db_tags == None):
        return {"reponse":"data not found for string: "+(tag_contains)}
    return db_tags




@app.put("/create/tagImplications")
async def create_tag_implication(tagImplicationRequest:List[schemas.tagImplicationCreate], db:Session =Depends(get_db)):
    for tag in tagImplicationRequest:
        db_tag_implication= crud.create_tag_implication(db,tag)
    return db_tag_implication

@app.get("/getAll/tagimplications")
async def read_all_tagimplications(skip: int = 0, db: Session = Depends(get_db)):
    db_tag_implication= crud.get_all_tagimplications(db,skip=skip)
    if(len(db_tag_implication) == 0):
        return {"reponse":"Empty Tag List. Kindly create a tag"}
    return db_tag_implication





@app.put("/create/alertworthyAll")
async def create_alertworthy(alertRequest:List[schemas.alertworthyCreate], db:Session =Depends(get_db)):
    for alert in alertRequest:
        db_alerts= crud.create_alertworthy(db,alert)
    return db_alerts

@app.put("/create/alertworthy/{bug_id}")
async def create_one_alertworthy(bug_id:int,alertRequest:List[schemas.alertworthyCreate], db:Session =Depends(get_db)):
    for alert in alertRequest:
        db_alerts= crud.create_one_alertworthy(bug_id,db,alert)
    return db_alerts

@app.get("/getAlertworthy/{bug_id}")
async def read_alerts(bug_id:int , db: Session = Depends(get_db)):
    db_alerts= crud.get_alertworthy(db,bug_id)
    if(db_alerts == None):
        return {"reponse":"data not found for bug_id: "+str(bug_id)}
    return db_alerts

@app.get("/getAll/alertworthy")
async def read_all_alerts(skip: int = 0, db: Session = Depends(get_db)):
    db_alerts= crud.get_all_alertworthy(db,skip=skip)
    if(len(db_alerts) == 0):
        return {"reponse":"Empty Bug List.Kindly create a bug"}
    return db_alerts

# Route to receive POST requests with Alertworthy data
@app.post("/add_alertworthy")
async def receive_alertworthy(alert_request: AlertworthyAdd):
    # Access the Alertworthy data from the request
    alertworthy_data = alert_request
    # Print the Alertworthy data to the terminal
    print("Received Alertworthy Data:")
    print(alertworthy_data)
    
    
    alertworthy = alert_request.alertworthy

    print("Received candidate Data: "+str(alertworthy))

    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh_client.load_system_host_keys()
    ssh_client.connect(Cred.hostname, Cred.port, Cred.username, Cred.password)

    stdin, stdout, stderr = ssh_client.exec_command(alertworthy)
    response = stdout.read().decode().strip("\n'")
    error_message = stderr
    print(stderr)
    
    ssh_client.close()
    
    if response == ("adding alertworthy"):
        print(response)
        return {"message": response}
    elif (response != "" and error_message == ""):
        print(response)
        return {"message": response}
    elif (response == "" and error_message == ""):
        print(response)
        return {"message": "Already exists"}
    else:
        error_message = stderr.read().decode().strip("\n'")
        print(error_message)
        return {"message": error_message}