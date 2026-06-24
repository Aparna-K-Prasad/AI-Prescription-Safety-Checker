# AI Prescription Safety Checker

## Overview

AI Prescription Safety Checker is a Django-based Clinical Decision Support System (CDSS) designed to assist healthcare professionals in identifying medication-related risks before issuing prescriptions.

The system analyzes prescriptions against patient medical records and generates safety alerts for allergies, contraindications, and drug interactions. It also provides alternative medication suggestions and downloadable PDF reports.

---

## Features

### Patient Management

* Add new patients
* Edit patient information
* View patient history
* Automatic age calculation

### Prescription Management

* Create prescriptions
* Edit prescriptions
* Follow-up date tracking
* Prescription history timeline

### Safety Analysis

* Drug Interaction Detection
* Allergy Checking
* Contraindication Checking
* Alternative Drug Suggestions

### Drug Information Support

* Side Effects Information
* Pregnancy Warnings
* Pediatric Warnings
* Maximum Daily Dosage Information

### Reporting

* Prescription Safety Report
* PDF Report Generation
* Replace and Reanalyze Workflow

---

## Technology Stack

* Python
* Django
* SQLite
* Bootstrap 5
* ReportLab

---

## Project Structure

```text
patients/         -> Patient management
prescriptions/    -> Prescription management
interactions/     -> Drug interaction and safety logic
reports/          -> Report generation
templates/        -> Frontend templates
```

---

## Installation

```bash
git clone https://github.com/Aparna-K-Prasad/AI-Prescription-Safety-Checker.git

cd AI-Prescription-Safety-Checker

pip install -r requirements.txt

python manage.py migrate

python manage.py runserver
```

---

## Future Scope

* User Authentication
* Expanded Drug Database
* AI-based Prescription Recommendations
* Electronic Health Record Integration
* Cloud Deployment

---

## Author

Aparna K Prasad
