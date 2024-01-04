from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Candidates, Alerts
import crud
import candiateList
import tagList
import tagImplicationList
import alertworthyList
import models
import schemas
import Cred
import time
from datetime import datetime
import pytz 

SQLALCHEMY_DATABASE_URL = f"postgresql://{Cred.DB_USER}:{Cred.DB_PASSWORD}@{Cred.DB_HOST}:{Cred.DB_PORT}/{Cred.DB_NAME}"

# Create a SQLAlchemy engine and session
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def synchronize_data():
    while True:
        db = SessionLocal()
        
        print("Start time:", str(datetime.now(pytz.utc).astimezone(pytz.timezone("Asia/Kolkata"))) + "IST / " + str(datetime.now(pytz.utc).astimezone(pytz.timezone("GMT"))) + "GMT")
     
        alert_List = alertworthyList.get_alertworthies()
        for alertworthy in alert_List:
            db_alert = models.Alerts(
                id = alertworthy['id'],
                bugalertOwner = alertworthy['bugalertOwner'],
                added = alertworthy['added'],
                description = alertworthy['description'],
                severity = alertworthy['severity'],
                product = alertworthy['product'],
                versionsIntroduced = alertworthy['versionsIntroduced'],
                versionFixed = alertworthy['versionFixed'],
                CVE = alertworthy['CVE'],
                bites = alertworthy['bites'],
                srCaseNumbers = alertworthy['srCaseNumbers'],
                lastBiteTime = alertworthy['lastBiteTime'],
                rule = alertworthy['rule'],
                alertSummary = alertworthy['alertSummary'],
                releaseNote = alertworthy['releaseNote'],
                supported = alertworthy['supported']
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
                db.commit()        
        print("Completed create_alertworthy")

        try:
            # Clearing state entries in candidate table
            # Step 1: Retrieve all the IDs from the "Alerts" table
            alert_ids = db.query(Alerts.id).all()
            alert_id_list = [alert.id for alert in alert_ids]

            if alert_id_list:
                # Step 2: Delete corresponding records from the "Candidates" table
                num_deleted = db.query(Candidates).filter(Candidates.id.in_(alert_id_list)).delete(synchronize_session=False)
                db.commit()
                print(f"Deleted {num_deleted} records from Candidates table.")
            else:
                print("No records to delete.")
                

        except Exception as e:
            db.rollback()
            print("An error occurred:", str(e))
            
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
        print("Completed create_all_candidate")    
        
        tag_List =tagList.get_tags()
        for tags in tag_List:
            db_tag = models.Tags(
                Tag = tags["Tag"], 
                Tag_description = tags["Tag_description"],
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
        print("Completed create_tag")
        
        tag_implication_List =tagImplicationList.get_tagimplications()
        for tag_implication in tag_implication_List:
            db_tag_implication = models.TagImplications(
                Tag = tag_implication["Tag"], 
                Tag_implication = tag_implication["Tag_implication"],
                )
        
            for attr, value in tag_implication.items():
                setattr(db_tag_implication, attr, value)
                
            db_rows=db.query(models.TagImplications).filter_by(Tag = str(db_tag_implication.Tag), Tag_implication = str(db_tag_implication.Tag_implication)).count()
            if db_rows == 0:
                db.add(db_tag_implication)
                db.commit()
                db.refresh(db_tag_implication)
            else:
                db.query(models.TagImplications).filter_by(Tag = str(db_tag_implication.Tag), Tag_implication = str(db_tag_implication.Tag_implication)).update({
                models.TagImplications.Tag_implication: db_tag_implication.Tag_implication,
                    models.TagImplications.createdOn: db_tag.createdOn,
                    models.TagImplications.updatedOn: db_tag.updatedOn
                })
                db.commit()
        print("Completed create_tag_implication")
    
        print("End time:", str(datetime.now(pytz.utc).astimezone(pytz.timezone("Asia/Kolkata"))) + "IST / " + str(datetime.now(pytz.utc).astimezone(pytz.timezone("GMT"))) + "GMT")
        db.close()
        time.sleep(600)
