-- Job Postings (50 entries, 2-3 per company)
INSERT INTO JobPostings (CompanyID, Title, JobType, SalaryRange, Location, Description, RequiredSkills, PostedBy)
VALUES
-- Google (CompanyID=1, PostedBy=81)
(1, 'Software Engineer', 'Full-time', '$90,000 - $130,000', 'Remote', 'Develop scalable backend systems using Python/Go.', 'Python, Go, SQL, REST APIs', 81),
(1, 'Data Science Intern', 'Internship', '$5,000/month', 'New York', 'Assist in building ML models for analytics.', 'Python, TensorFlow, SQL', 81),
(1, 'Frontend Developer', 'Full-time', '$85,000 - $115,000', 'Remote', 'Build responsive UIs with React.js.', 'JavaScript, React, CSS', 81),

-- Microsoft (CompanyID=2, PostedBy=82)
(2, 'Cloud Solutions Architect', 'Full-time', '$120,000 - $160,000', 'Seattle', 'Design Azure-based cloud infrastructure.', 'Azure, Terraform, DevOps', 82),
(2, 'UI/UX Designer', 'Internship', '$4,500/month', 'Remote', 'Design interfaces for enterprise software.', 'Figma, Adobe XD, HTML/CSS', 82),
(2, 'DevOps Engineer', 'Full-time', '$110,000 - $140,000', 'Redmond', 'Automate CI/CD pipelines for Azure.', 'Azure, Docker, Kubernetes', 82),

-- Amazon (CompanyID=3, PostedBy=83)
(3, 'Machine Learning Engineer', 'Full-time', '$140,000 - $180,000', 'Austin', 'Build recommendation systems for e-commerce.', 'Python, PyTorch, AWS', 83),
(3, 'Supply Chain Analyst', 'Full-time', '$80,000 - $100,000', 'Dallas', 'Optimize logistics and inventory management.', 'Excel, SQL, Tableau', 83),
(3, 'Product Manager', 'Full-time', '$130,000 - $160,000', 'Seattle', 'Lead e-commerce product development.', 'Agile, Jira, SQL', 83),

-- Tesla (CompanyID=4, PostedBy=84)
(4, 'Autopilot Engineer', 'Full-time', '$130,000 - $170,000', 'Fremont', 'Develop autonomous driving algorithms.', 'C++, Python, Robotics', 84),
(4, 'Battery Systems Intern', 'Internship', '$6,000/month', 'Austin', 'Research next-gen battery technologies.', 'Electrochemistry, MATLAB', 84),
(4, 'Electrical Engineer', 'Full-time', '$100,000 - $130,000', 'Fremont', 'Design EV charging systems.', 'Circuit Design, MATLAB', 84),

-- IBM (CompanyID=5, PostedBy=85)
(5, 'Quantum Computing Researcher', 'Full-time', '$150,000 - $200,000', 'New York', 'Advance quantum algorithms for optimization.', 'Qiskit, Python, Linear Algebra', 85),
(5, 'AI Ethics Researcher', 'Full-time', '$95,000 - $120,000', 'Cambridge', 'Study ethical implications of AI systems.', 'Ethics, Python, NLP', 85),

-- Quantum Innovations (CompanyID=6, PostedBy=86)
(6, 'Quantum Software Developer', 'Full-time', '$110,000 - $140,000', 'Boston', 'Build tools for quantum computing platforms.', 'Python, C++, Quantum Mechanics', 86),
(6, 'Quantum Algorithm Intern', 'Internship', '$5,500/month', 'Boston', 'Research quantum machine learning.', 'Qiskit, Linear Algebra', 86),

-- CyberCore Systems (CompanyID=7, PostedBy=87)
(7, 'Cybersecurity Analyst', 'Full-time', '$95,000 - $125,000', 'Remote', 'Monitor and mitigate network threats.', 'SIEM, Firewalls, Ethical Hacking', 87),
(7, 'Penetration Tester', 'Full-time', '$105,000 - $135,000', 'Remote', 'Simulate cyberattacks for vulnerability testing.', 'Kali Linux, Metasploit', 87),

-- GreenTech Solutions (CompanyID=8, PostedBy=88)
(8, 'Renewable Energy Engineer', 'Full-time', '$85,000 - $110,000', 'Denver', 'Design solar/wind energy systems.', 'AutoCAD, MATLAB, Physics', 88),
(8, 'Solar Energy Analyst', 'Full-time', '$80,000 - $100,000', 'Phoenix', 'Optimize solar farm efficiency.', 'Python, GIS, Data Analysis', 88),

-- Visionary Labs (CompanyID=9, PostedBy=89)
(9, 'Robotics Engineer', 'Full-time', '$100,000 - $135,000', 'San Francisco', 'Develop AI-driven robotic systems.', 'ROS, Python, Computer Vision', 89),
(9, 'AI Robotics Intern', 'Internship', '$4,200/month', 'San Francisco', 'Train ML models for robot navigation.', 'Python, TensorFlow, ROS', 89),

-- NanoTech Solutions (CompanyID=10, PostedBy=90)
(10, 'Nanotech Research Scientist', 'Full-time', '$120,000 - $150,000', 'Boston', 'Develop nanomaterials for medical devices.', 'SEM/TEM, LabVIEW, Chemistry', 90),
(10, 'Materials Scientist', 'Full-time', '$115,000 - $140,000', 'Boston', 'Develop graphene-based nanomaterials.', 'Materials Science, Lab Skills', 90),

-- Intel (CompanyID=11, PostedBy=91)
(11, 'Semiconductor Engineer', 'Full-time', '$105,000 - $140,000', 'Santa Clara', 'Design next-gen microprocessors.', 'VLSI, Verilog, CAD Tools', 91),
(11, 'FPGA Engineer', 'Full-time', '$125,000 - $155,000', 'Hillsboro', 'Design FPGA-based accelerators.', 'VHDL, Verilog, Digital Design', 91),

-- Netflix (CompanyID=12, PostedBy=92)
(12, 'Content Recommendation Analyst', 'Full-time', '$95,000 - $120,000', 'Los Angeles', 'Optimize streaming content algorithms.', 'Python, SQL, Machine Learning', 92),
(12, 'Video Encoding Engineer', 'Full-time', '$140,000 - $180,000', 'Los Angeles', 'Optimize video compression algorithms.', 'FFmpeg, C++, H.264/HEVC', 92),

-- Salesforce (CompanyID=13, PostedBy=93)
(13, 'CRM Solutions Architect', 'Full-time', '$130,000 - $160,000', 'Remote', 'Implement Salesforce for enterprise clients.', 'Salesforce, Apex, Integration', 93),
(13, 'Salesforce Admin', 'Full-time', '$90,000 - $110,000', 'Remote', 'Manage Salesforce CRM for clients.', 'Salesforce, Workflows', 93),

-- FutureWave Technologies (CompanyID=14, PostedBy=94)
(14, '5G Network Engineer', 'Full-time', '$100,000 - $130,000', 'Dallas', 'Deploy and optimize 5G infrastructure.', '5G, LTE, Python', 94),
(14, 'IoT Solutions Architect', 'Full-time', '$100,000 - $130,000', 'Austin', 'Design IoT systems for smart cities.', 'IoT, MQTT, Python', 94),

-- SkyNet Analytics (CompanyID=15, PostedBy=95)
(15, 'Big Data Engineer', 'Full-time', '$115,000 - $145,000', 'Chicago', 'Build ETL pipelines for analytics.', 'Spark, Hadoop, Scala', 95),
(15, 'Data Visualization Specialist', 'Full-time', '$95,000 - $120,000', 'Chicago', 'Create dashboards for business analytics.', 'Tableau, Power BI, SQL', 95),

-- BioGen Innovations (CompanyID=16, PostedBy=96)
(16, 'Biotech Research Intern', 'Internship', '$4,000/month', 'Boston', 'Assist in gene-editing research.', 'CRISPR, Lab Techniques', 96),
(16, 'Bioinformatics Analyst', 'Full-time', '$85,000 - $110,000', 'San Diego', 'Analyze genomic data for research.', 'Python, R, Bioinformatics', 96),

-- SpaceWorks Dynamics (CompanyID=17, PostedBy=97)
(17, 'Aerospace Engineer', 'Full-time', '$120,000 - $150,000', 'Los Angeles', 'Design satellite propulsion systems.', 'CAD, CFD, Aerospace Engineering', 97),
(17, 'Satellite Communications Engineer', 'Full-time', '$130,000 - $160,000', 'Los Angeles', 'Develop satellite communication protocols.', 'RF, MATLAB, DSP', 97),

-- AeroVision Systems (CompanyID=18, PostedBy=98)
(18, 'Drone Software Developer', 'Full-time', '$90,000 - $120,000', 'Seattle', 'Build autonomy software for drones.', 'C++, ROS, Robotics', 98),
(18, 'Drone Hardware Engineer', 'Full-time', '$95,000 - $120,000', 'Seattle', 'Design drone propulsion systems.', 'CAD, Mechanical Engineering', 98),

-- Adobe (CompanyID=19, PostedBy=99)
(19, 'Creative Cloud Developer', 'Full-time', '$110,000 - $140,000', 'San Jose', 'Enhance Adobe Photoshop/Illustrator tools.', 'C++, OpenGL, APIs', 99),
(19, 'Video Editor Tools Developer', 'Full-time', '$105,000 - $135,000', 'San Jose', 'Enhance Adobe Premiere Pro features.', 'C++, OpenGL, APIs', 99),

-- Cisco (CompanyID=20, PostedBy=100)
(20, 'Network Security Engineer', 'Full-time', '$95,000 - $130,000', 'Raleigh', 'Secure enterprise network infrastructure.', 'Cisco IOS, Firewalls, VPN', 100),
(20, 'Network Automation Engineer', 'Full-time', '$110,000 - $140,000', 'Raleigh', 'Automate network configuration tasks.', 'Python, Ansible, Cisco', 100);

SELECT COUNT(*) FROM JobPostings;