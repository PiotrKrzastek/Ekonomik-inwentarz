# Ekonomik inventory system
A full-stack asset management solution designed to digitize equipment tracking in a school faculty.

## Overview
This app was not made for commercial use and it was meant to solve a real-world problem with inventory management in the school I graduated from.

What started as a simple academic assignment evolved into a complex project as I chose to expand the MVP into a more robust system. While the project is currently in a frozen state and serves as a functional Proof of Concept, it remains a significant milestone in my development. Building this system was my first deep dive into cloud integration and complex backend logic, providing me with invaluable hands-on experience in software architecture.

## Features

* **Full CRUD Lifecycle Management:** Complete system for adding, editing, and deleting assets, featuring robust search and filtering by external ID, room, or category.

* **Hybrid Authentication System:** Integrated with Azure AD via a toggleable mode; supports both authenticated corporate sessions and a local "anonymous" mode for testing/flexible deployment.

* **Dynamic Asset Specifications:** Leverages MongoDB’s schema-less nature to allow custom metadata for different device types (e.g., RAM for PCs, HDMI ports for monitors) without database migrations.

* **Automated Labeling System:** Integrated python-barcode generation for standardized physical asset organization and tracking.

* **Cloud-Native Storage:** Fully integrated with AWS S3 (via Boto3) to store and serve asset photos and generated barcodes securely.

* **Interactive Spatial Navigation:** Frontend features a clickable building map with layers, allowing for intuitive room-based asset filtration.

* **Administrative Control Panel:**

    * **Specification Engine:** A dedicated subpage for managing custom attribute sets (OS, Hardware specs, etc.).

    * **Activity Auditing:** Lightweight tracking system that logs last login, last edit timestamp, and edited asset ID.

## Database schema 
I opted for a NoSQL (MongoDB) database to handle the inherently polymorphic nature of school assets.

In a school environment, a ```Monitor``` and a ```Laptop``` require entirely different metadata. Using a document-oriented approach allowed me to store these variations within a single ```specs``` object without the overhead of complex SQL joins or rigid table migrations.

**Comparison of Document Structures:**

* **Laptop:** Focuses on ```OS``` and ```RAM```.

* **Monitor:** Focuses on hardware connectivity like ```HDMI ports```.

While MongoDB was the optimal choice for rapid MVP development and flexible schema prototyping, I recognize that a future production-scale version would benefit from a migration to PostgreSQL.

**Deployment Note:** 
Because MongoDB is schema-less, no pre-configuration of collections is required. To initialize the database, simply provide your connection string in the .env file: ```DB_URL=<your_mongo_uri>```

## Integration and security

### Authentication
The authentication architecture was designed specifically for a school environment, balancing widespread accessibility with strict data integrity.

* **Primary Layer (Azure AD):** Leveraging MSAL to ensure that only users within the school’s domain can access the application. This eliminates the need for manual account creation for hundreds of students and faculty members.

* **Secondary Layer (Granular Access Control):** To mitigate the risk of unauthorized modifications by students within the domain, I implemented a custom internal authorization layer.

* **The "Trusted User" Logic:** This system allows "Super Users" (Faculty) to whitelist specific students for administrative tasks (e.g., scanning assets in a specific room) without requiring complex permission changes within the global Azure AD tenant.

* **Audit Logging:** Every interaction is tied to a unique user identity, logging the last_user and last_update timestamp to ensure full accountability for every asset modification.

**Deployment Note:** The application is designed for deployment flexibility, featuring a built-in hybrid mode managed via ```app/config/settings.py```. By toggling the ```LOGIN_ENABLED``` flag, developers can seamlessly switch between full Azure AD authentication and a local "Anonymous Mode", allowing for core logic auditing without an active cloud identity provider. Furthermore, administrative privileges are decoupled from global tenant configurations. the ```ROOT_LOGINS``` list allows for the dynamic assignment of Super User status to specific email addresses directly within the application settings.

### Storage
I integrated AWS S3 via the Boto3 library to handle asset photos and generated barcodes. While storing files locally was an option, I chose a cloud-native approach to gain hands-on experience with industry-standard storage solutions.

This integration allowed me to explore how a backend service orchestrates data across a distributed stack—fetching metadata from MongoDB, authenticating via Azure AD, and serving binary data through AWS S3. Implementing this taught me how to manage cloud credentials securely and handle asynchronous data streams within a Flask application.


## Setup

1. **Clone this repository:**
```
git clone https://github.com/PiotrKrzastek/Ekonomik-inwentarz
cd Ekonomik-inwentarz
```

2. **Create virtual environment and install dependencies:**
```
python3 -m venv .venv
source .venv/bin/activate # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

3. **Create .env based on .env.example:**
```
SECRET_KEY=

AUTHORITY=
CLIENT_ID=
CLIENT_SECRET=
REDIRECT_URI=

DB_URL=

AWS_ACCESS_KEY_ID=
AWS_SECRET_ACCESS_KEY=
``` 

4. **Run flask:**
```
flask run
```

## What I learned
Building this system was a steep learning curve that taught me more than any tutorial could. Key takeaways include:
* **Cloud Infrastructure:** Understanding the shared responsibility model and service orchestration between different providers (AWS, Azure, MongoDB Atlas).
* **NoSQL Data Modeling:** Learning when to use document-oriented databases to handle polymorphic data structures effectively.
* **Security Mindset:** Realizing that authentication (who you are) and authorization (what you can do) are two different layers that must be handled with care, especially in a public-facing environment like a school.