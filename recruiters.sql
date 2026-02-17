-- Recruiters (1 per company)
INSERT INTO Users (FullName, Email, PasswordHash, Role, IsApproved, IsActive)
VALUES
('John Carter', 'john.carter@google.com', 'recruiter_pass_1', 'Recruiter', 1, 1),
('Emily Davis', 'emily.davis@microsoft.com', 'recruiter_pass_2', 'Recruiter', 1, 1),
('Michael Brown', 'michael.brown@amazon.com', 'recruiter_pass_3', 'Recruiter', 1, 1),
('Sarah Wilson', 'sarah.wilson@tesla.com', 'recruiter_pass_4', 'Recruiter', 1, 1),
('David Lee', 'david.lee@ibm.com', 'recruiter_pass_5', 'Recruiter', 1, 1),
('Sophia Clark', 'sophia.clark@quantuminnovations.com', 'recruiter_pass_6', 'Recruiter', 1, 1),
('James Taylor', 'james.taylor@cybercoresys.com', 'recruiter_pass_7', 'Recruiter', 1, 1),
('Olivia Moore', 'olivia.moore@greentechsolutions.com', 'recruiter_pass_8', 'Recruiter', 1, 1),
('Daniel Harris', 'daniel.harris@visionarylabs.com', 'recruiter_pass_9', 'Recruiter', 1, 1),
('Emma Martinez', 'emma.martinez@nanotechsolutions.com', 'recruiter_pass_10', 'Recruiter', 1, 1),
('William Anderson', 'william.anderson@intel.com', 'recruiter_pass_11', 'Recruiter', 1, 1),
('Ava Jackson', 'ava.jackson@netflix.com', 'recruiter_pass_12', 'Recruiter', 1, 1),
('Liam White', 'liam.white@salesforce.com', 'recruiter_pass_13', 'Recruiter', 1, 1),
('Charlotte Lewis', 'charlotte.lewis@futurewavetech.com', 'recruiter_pass_14', 'Recruiter', 1, 1),
('Noah Hall', 'noah.hall@skynetanalytics.com', 'recruiter_pass_15', 'Recruiter', 1, 1),
('Isabella Young', 'isabella.young@biogeninnovations.com', 'recruiter_pass_16', 'Recruiter', 1, 1),
('Lucas King', 'lucas.king@spaceworks.com', 'recruiter_pass_17', 'Recruiter', 1, 1),
('Mia Scott', 'mia.scott@aerovisionsystems.com', 'recruiter_pass_18', 'Recruiter', 1, 1),
('Ethan Green', 'ethan.green@adobe.com', 'recruiter_pass_19', 'Recruiter', 1, 1),
('Amelia Adams', 'amelia.adams@cisco.com', 'recruiter_pass_20', 'Recruiter', 1, 1);

-- Link recruiters to their companies
INSERT INTO Recruiters (RecruiterID, CompanyID, Designation)
VALUES
(81, 1, 'Senior Talent Acquisition Lead'),  -- Google
(82, 2, 'HR Manager'),                     -- Microsoft
(83, 3, 'Technical Recruiter'),            -- Amazon
(84, 4, 'Campus Recruitment Head'),        -- Tesla
(85, 5, 'AI Talent Specialist'),           -- IBM
(86, 6, 'Quantum Hiring Manager'),         -- Quantum Innovations
(87, 7, 'Cybersecurity Recruiter'),        -- CyberCore Systems
(88, 8, 'Green Energy HR Lead'),           -- GreenTech Solutions
(89, 9, 'Robotics Talent Partner'),        -- Visionary Labs
(90, 10, 'Nanotech Recruitment Head'),     -- NanoTech Solutions
(91, 11, 'Semiconductor Recruiter'),       -- Intel
(92, 12, 'Entertainment Talent Manager'),  -- Netflix
(93, 13, 'CRM Recruitment Specialist'),    -- Salesforce
(94, 14, 'Telecom HR Lead'),               -- FutureWave Technologies
(95, 15, 'Data Science Recruiter'),        -- SkyNet Analytics
(96, 16, 'Biotech Talent Partner'),        -- BioGen Innovations
(97, 17, 'Aerospace Recruitment Head'),    -- SpaceWorks Dynamics
(98, 18, 'Drone Technology Recruiter'),    -- AeroVision Systems
(99, 19, 'Creative Talent Manager'),       -- Adobe
(100, 20, 'Networks HR Lead');             -- Cisco