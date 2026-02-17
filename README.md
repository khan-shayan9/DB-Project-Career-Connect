Career-Connect: Job Application Portal
A robust, multi-role recruitment management system designed to streamline the job application process for Students, Recruiters, and Administrators. This project focuses on high-integrity database design and role-based data management.

🛠 Technologies Used
Language: Python

Database: MySQL

Libraries: mysql-connector-python (or your specific driver)

Concepts: Relational Database Design, RBAC (Role-Based Access Control), Data Normalization (3NF).

🚀 Key Features
Multi-Role Authentication: Secure login system with distinct permissions for Students, Recruiters, and Admins.

Student Module: Profile management, job searching, and real-time application tracking.

Recruiter Dashboard: Post job openings, manage candidate pools, and update application statuses (Shortlisted, Accepted, Rejected).

Admin Reporting: A powerful analytics suite that uses SQL aggregation to generate summaries of hiring trends and portal activity.

Referential Integrity: Strictly enforced database constraints (Primary/Foreign Keys) to ensure data consistency across complex joins.

📊 Database Schema Highlights
The system is built on a normalized schema including:

Users: Unified table for credentials with role identification.

Companies: Profiles for registered employers.

Jobs: Detailed postings linked to companies.

Applications: A junction table managing the many-to-many relationship between students and job posts.

💻 Technical Implementation
Complex Queries: Utilizes advanced SQL JOINs and GROUP BY clauses for real-time reporting.

Python Integration: Implemented a modular Python interface to handle database connectivity and execute CRUD operations safely.

Integrity: Applied ON DELETE CASCADE and NOT NULL constraints to prevent orphaned records.
