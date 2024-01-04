from pydantic import BaseModel

import datetime

class candidateCreate(BaseModel):
    id:int
    bugalertOwner:str
    assignedOn:str
    description:str
    severity:str
    CVE:str
    product:str
    versionsIntroduced:str
    versionFixed:str
    bites:str
    srCaseNumbers:str
    lastBiteTime:str
    fixes:str
    lastFixTime:str
    releaseNote:str
    createdOn: datetime.datetime
    updatedOn: datetime.datetime

class tagCreate(BaseModel):
    Tag:str
    Tag_description:str
    createdOn: datetime.datetime
    updatedOn: datetime.datetime

class tagImplicationCreate(BaseModel):
    Tag:str
    Tag_implication:str
    createdOn: datetime.datetime
    updatedOn: datetime.datetime

class alertworthyCreate(BaseModel):
    id:int
    bugalertOwner:str
    added:str
    description:str
    severity:str
    product:str
    versionsIntroduced:str
    versionFixed:str
    CVE:str
    bites:str
    srCaseNumbers:str
    lastBiteTime:str
    rule:str
    alertSummary:str
    releaseNote:str
    supported:str
    createdOn: datetime.datetime
    updatedOn: datetime.datetime
    
class AlertworthyAdd(BaseModel):
    alertworthy: str  
    
class CandidateAdd(BaseModel):
    id:int