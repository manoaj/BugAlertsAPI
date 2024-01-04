from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import or_

import candiateList
import tagList
import tagImplicationList
import alertworthyList
import models
import schemas
import Cred


def get_candidate(db: Session, bug_id: int):
    return db.query(models.Candidates).filter(models.Candidates.id == bug_id).first()

def get_all_candidates(db: Session, skip: int = 0):
    return db.query(models.Candidates).offset(skip).all()

def get_all_unassigned_candidates(db: Session, skip: int = 0):
    return db.query(models.Candidates).filter(or_(models.Candidates.bugalertOwner == "", models.Candidates.bugalertOwner == "unassigned")).offset(skip).all()

def get_all_user_candidates(db: Session, skip: int = 0):
    return db.query(models.Candidates).filter_by(bugalertOwner=Cred.username).offset(skip).all()

def create_all_candidate(db:Session, candidate: schemas.candidateCreate):
    candiate_List = candiateList.get_candidates()
    for candidate in candiate_List:
        db_candidate = models.Candidates(
            id = candidate["id"],
            bugalertOwner = candidate["bugalertOwner"],
            assignedOn = candidate["assignedOn"],
            description = candidate["description"],
            severity = candidate["severity"],
            CVE = candidate["CVE"],
            product = candidate["product"],
            versionsIntroduced = candidate["versionsIntroduced"],
            versionFixed = candidate["versionFixed"],
            bites = candidate["bites"],
            srCaseNumbers = candidate["srCaseNumbers"],
            lastBiteTime = candidate["lastBiteTime"],
            fixes = candidate["fixes"],
            lastFixTime = candidate["lastFixTime"],
            releaseNote = candidate["releaseNote"]
            )

        db_rows=db.query(models.Candidates).filter_by(id = int(db_candidate.id)).count()
        if db_rows == 0:
            db.add(db_candidate)
            db.commit()
            db.refresh(db_candidate)
        else:
            db.query(models.Candidates).filter_by(id = int(db_candidate.id)).update({
                models.Candidates.bugalertOwner: db_candidate.bugalertOwner,
                models.Candidates.assignedOn: db_candidate.assignedOn,
                models.Candidates.description: db_candidate.description,
                models.Candidates.severity: db_candidate.severity,
                models.Candidates.CVE: db_candidate.CVE,
                models.Candidates.product: db_candidate.product,
                models.Candidates.versionsIntroduced: db_candidate.versionsIntroduced,
                models.Candidates.versionFixed: db_candidate.versionFixed,
                models.Candidates.bites: db_candidate.bites,
                models.Candidates.srCaseNumbers: db_candidate.srCaseNumbers,
                models.Candidates.lastBiteTime: db_candidate.lastBiteTime,
                models.Candidates.fixes: db_candidate.fixes,
                models.Candidates.lastFixTime: db_candidate.lastFixTime,
                models.Candidates.releaseNote: db_candidate.releaseNote
            })
            print()
            print (db_candidate.id, db_candidate.bugalertOwner)
            print()
            db.commit()
    
    return candiate_List

def create_one_candidate(bug_id:int, db:Session, candidate: schemas.candidateCreate):
    candiate_List = candiateList.get_one_candidates(bug_id)
    for candidate in candiate_List:
        db_candidate = models.Candidates(
            id = candidate["id"],
            bugalertOwner = candidate["bugalertOwner"],
            assignedOn = candidate["assignedOn"],
            description = candidate["description"],
            severity = candidate["severity"],
            CVE = candidate["CVE"],
            product = candidate["product"],
            versionsIntroduced = candidate["versionsIntroduced"],
            versionFixed = candidate["versionFixed"],
            bites = candidate["bites"],
            srCaseNumbers = candidate["srCaseNumbers"],
            lastBiteTime = candidate["lastBiteTime"],
            fixes = candidate["fixes"],
            lastFixTime = candidate["lastFixTime"],
            releaseNote = candidate["releaseNote"]
            )

        db_rows=db.query(models.Candidates).filter_by(id = int(db_candidate.id)).count()
        if db_rows == 0:
            db.add(db_candidate)
            db.commit()
            db.refresh(db_candidate)
        else:
            db.query(models.Candidates).filter_by(id = int(db_candidate.id)).update({
                models.Candidates.bugalertOwner: db_candidate.bugalertOwner,
                models.Candidates.assignedOn: db_candidate.assignedOn,
                models.Candidates.description: db_candidate.description,
                models.Candidates.severity: db_candidate.severity,
                models.Candidates.CVE: db_candidate.CVE,
                models.Candidates.product: db_candidate.product,
                models.Candidates.versionsIntroduced: db_candidate.versionsIntroduced,
                models.Candidates.versionFixed: db_candidate.versionFixed,
                models.Candidates.bites: db_candidate.bites,
                models.Candidates.srCaseNumbers: db_candidate.srCaseNumbers,
                models.Candidates.lastBiteTime: db_candidate.lastBiteTime,
                models.Candidates.fixes: db_candidate.fixes,
                models.Candidates.lastFixTime: db_candidate.lastFixTime,
                models.Candidates.releaseNote: db_candidate.releaseNote
            })
            print()
            print (db_candidate.id, db_candidate.bugalertOwner)
            print()
            db.commit()
    
    return candiate_List


def delete_candidate(db: Session, bug_id: int):
    try: 
        numRows= db.query(models.Candidates).filter_by(id=bug_id).delete()
        if numRows == 0:
            return {"response" : "Bug id: "+str(bug_id)+ " not found"}
        else:
            db.commit()
            return {"response" : "Bug id: "+str(bug_id)+ " deleted Successfully"}
    except Exception as e:
        return {"response" : "exception Occured." + str(e)}

def create_tag(db:Session, tag: schemas.tagCreate):
    tag_List =tagList.get_tags()
    
    for tags in tag_List:
        db_tag = models.Tags(
            Tag = tag.Tag, 
            Tag_description = tag.Tag_description,
            createdOn= tag.createdOn, 
            updatedOn=tag.updatedOn
            )
       
        for attr, value in tags.items():
            setattr(db_tag, attr, value)

        db_rows=db.query(models.Tags).filter_by(Tag = str(db_tag.Tag)).count()
        if db_rows == 0:
            db.add(db_tag)
            db.commit()
            db.refresh(db_tag)
        else:
            db.query(models.Tags).filter_by(Tag = str(db_tag.Tag)).update({
                models.Tags.Tag_description: db_tag.Tag_description,
                models.Tags.createdOn: db_tag.createdOn,
                models.Tags.updatedOn: db_tag.updatedOn
            })
            print()
            print (tag.Tag, models.Tags.Tag)
            print (db_tag.Tag, db_tag.Tag_description)
            print()
            db.commit()
    
    return tag_List

def get_all_tags(db: Session, skip: int = 0):
    return db.query(models.Tags).offset(skip).all()

def get_tags_containing(db: Session, tag_contains:str):
    return db.query(models.Tags).filter(or_(models.Tags.Tag_description.ilike('%' + tag_contains + '%'),models.Tags.Tag.ilike('%' + tag_contains + '%'))).all()



def create_tag_implication(db:Session, tag: schemas.tagImplicationCreate):
    tag_implication_List =tagImplicationList.get_tagimplications()
    
    for tags in tag_implication_List:
        db_tag_implication = models.TagImplications(
            Tag = tag.Tag, 
            Tag_implication = tag.Tag_implication,
            createdOn= tag.createdOn, 
            updatedOn=tag.updatedOn
            )
       
        for attr, value in tags.items():
            setattr(db_tag_implication, attr, value)

        db_rows=db.query(models.TagImplications).filter_by(Tag = str(db_tag_implication.Tag), Tag_implication = str(db_tag_implication.Tag_implication)).count()
        if db_rows == 0:
            db.add(db_tag_implication)
            db.commit()
            db.refresh(db_tag_implication)
        else:
            db.query(models.TagImplications).filter_by(Tag = str(db_tag_implication.Tag)).update({
                models.TagImplications.Tag_implication: db_tag_implication.Tag_implication,
                models.TagImplications.createdOn: db_tag_implication.createdOn,
                models.TagImplications.updatedOn: db_tag_implication.updatedOn
            })
            db.commit()
    
    return tag_implication_List

def get_all_tagimplications(db: Session, skip: int = 0):
    return db.query(models.TagImplications).offset(skip).all()




def create_alertworthy(db:Session, alert: schemas.alertworthyCreate):
    alert_List = alertworthyList.get_alertworthies()

    for alertworthy in alert_List:
        db_alert = models.Alerts(
            id = alert.id,
            bugalertOwner = alert.bugalertOwner,
            added = alert.added,
            description = alert.description,
            severity = alert.severity,
            product = alert.product,
            versionsIntroduced = alert.versionsIntroduced,
            versionFixed = alert.versionFixed,
            CVE = alert.CVE,
            bites = alert.bites,
            srCaseNumbers = alert.srCaseNumbers,
            lastBiteTime = alert.lastBiteTime,
            rule = alert.rule,
            alertSummary = alert.alertSummary,
            releaseNote = alert.releaseNote,
            supported = alert.supported
            )
        
        for attr, value in alertworthy.items():
            setattr(db_alert, attr, value)

        db_rows=db.query(models.Alerts).filter_by(id = int(db_alert.id)).count()
        if db_rows == 0:
            db.add(db_alert)
            db.commit()
            db.refresh(db_alert)
        else:
            db.query(models.Alerts).filter_by(id = int(db_alert.id)).update({
                models.Alerts.bugalertOwner: db_alert.bugalertOwner,
                models.Alerts.added: db_alert.added,
                models.Alerts.description: db_alert.description,
                models.Alerts.severity: db_alert.severity,
                models.Alerts.product: db_alert.product,
                models.Alerts.versionsIntroduced: db_alert.versionsIntroduced,
                models.Alerts.versionFixed: db_alert.versionFixed,
                models.Alerts.CVE: db_alert.CVE,
                models.Alerts.bites: db_alert.bites,
                models.Alerts.srCaseNumbers: db_alert.srCaseNumbers,
                models.Alerts.lastBiteTime: db_alert.lastBiteTime,
                models.Alerts.rule: db_alert.rule,
                models.Alerts.alertSummary: db_alert.alertSummary,
                models.Alerts.releaseNote: db_alert.releaseNote,
                models.Alerts.supported: db_alert.supported
            })
            print()
            print (alert.id, models.Alerts.id)
            print (db_alert.id, db_alert.bugalertOwner)
            print()
            db.commit()
            
    return alert_List

def create_one_alertworthy(bug_id:int, db:Session, alert: schemas.alertworthyCreate):
    alert_List = alertworthyList.get_one_alertworthies(bug_id)

    for alertworthy in alert_List:
        db_alert = models.Alerts(
            id = alert.id,
            bugalertOwner = alert.bugalertOwner,
            added = alert.added,
            description = alert.description,
            severity = alert.severity,
            product = alert.product,
            versionsIntroduced = alert.versionsIntroduced,
            versionFixed = alert.versionFixed,
            CVE = alert.CVE,
            bites = alert.bites,
            srCaseNumbers = alert.srCaseNumbers,
            lastBiteTime = alert.lastBiteTime,
            rule = alert.rule,
            alertSummary = alert.alertSummary,
            releaseNote = alert.releaseNote,
            supported = alert.supported
            )
        
        for attr, value in alertworthy.items():
            setattr(db_alert, attr, value)

        db_rows=db.query(models.Alerts).filter_by(id = int(db_alert.id)).count()
        if db_rows == 0:
            db.add(db_alert)
            db.commit()
            db.refresh(db_alert)
        else:
            db.query(models.Alerts).filter_by(id = int(db_alert.id)).update({
                models.Alerts.bugalertOwner: db_alert.bugalertOwner,
                models.Alerts.added: db_alert.added,
                models.Alerts.description: db_alert.description,
                models.Alerts.severity: db_alert.severity,
                models.Alerts.product: db_alert.product,
                models.Alerts.versionsIntroduced: db_alert.versionsIntroduced,
                models.Alerts.versionFixed: db_alert.versionFixed,
                models.Alerts.CVE: db_alert.CVE,
                models.Alerts.bites: db_alert.bites,
                models.Alerts.srCaseNumbers: db_alert.srCaseNumbers,
                models.Alerts.lastBiteTime: db_alert.lastBiteTime,
                models.Alerts.rule: db_alert.rule,
                models.Alerts.alertSummary: db_alert.alertSummary,
                models.Alerts.releaseNote: db_alert.releaseNote,
                models.Alerts.supported: db_alert.supported
            })
            print()
            print (alert.id, models.Alerts.id)
            print (db_alert.id, db_alert.bugalertOwner)
            print()
            db.commit()
            
    return alert_List


def get_alertworthy(db: Session, bug_id: int):
    return db.query(models.Alerts).filter(models.Alerts.id == bug_id).first()

def get_all_alertworthy(db: Session, skip: int = 0):
    return db.query(models.Alerts).offset(skip).all()