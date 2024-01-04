from sqlalchemy import Boolean, Column, DateTime, Integer, String, PrimaryKeyConstraint
from sqlalchemy.orm import relationship

import datetime
from database import Base

class Candidates(Base):
    __tablename__ = "candidates"

    id = Column(Integer, primary_key=True, index=True)
    bugalertOwner = Column(String)
    assignedOn = Column(String)
    description = Column(String)
    severity= Column(String)
    CVE= Column(String)
    product=Column(String)
    versionsIntroduced=Column(String)
    versionFixed=Column(String)
    bites=Column(String)
    srCaseNumbers=Column(String)
    lastBiteTime=Column(String)
    fixes=Column(String)
    lastFixTime=Column(String)
    releaseNote=Column(String)
    createdOn=Column(DateTime, default=datetime.datetime.utcnow)
    updatedOn=Column(DateTime, default=datetime.datetime.utcnow)


class Tags(Base):
    __tablename__ = "tags"

    Tag = Column(String, primary_key=True, index=True)
    Tag_description = Column(String)
    createdOn=Column(DateTime, default=datetime.datetime.utcnow)
    updatedOn=Column(DateTime, default=datetime.datetime.utcnow)


class TagImplications(Base):
    __tablename__ = "tagImplications"

    Tag = Column(String, index=True)
    Tag_implication = Column(String)
    createdOn=Column(DateTime, default=datetime.datetime.utcnow)
    updatedOn=Column(DateTime, default=datetime.datetime.utcnow)
    
    __table_args__ = (
        PrimaryKeyConstraint('Tag', 'Tag_implication'),
    )


class Alerts(Base):
    __tablename__ = "alerts"

    id = Column(Integer, primary_key=True, index=True)
    bugalertOwner = Column(String)
    added = Column(String)
    description = Column(String)
    severity = Column(String)
    product = Column(String)
    versionsIntroduced = Column(String)
    versionFixed = Column(String)
    CVE = Column(String)
    bites = Column(String)
    srCaseNumbers = Column(String)
    lastBiteTime = Column(String)
    rule = Column(String)
    alertSummary = Column(String)
    releaseNote = Column(String)
    supported = Column(String)
    createdOn=Column(DateTime, default=datetime.datetime.utcnow)
    updatedOn=Column(DateTime, default=datetime.datetime.utcnow)