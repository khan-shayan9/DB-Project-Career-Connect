create Database CareerConnect
use CareerConnect


--Creating the Tables 

--1) User Table
create table Users (
    UserID INT PRIMARY KEY IDENTITY,
    FullName NVARCHAR(100),
    Email VARCHAR(100) UNIQUE,
    PasswordHash VARCHAR(255),
    Role VARCHAR(20), -- 'Student', 'Recruiter', 'TPO', 'Coordinator'
    IsApproved BIT DEFAULT 0, -- Recruiter approval
    IsActive BIT DEFAULT 1
)

--2) Students Table
create table Students (
    StudentID INT PRIMARY KEY,
    FAST_ID VARCHAR(20) UNIQUE,
    GPA DECIMAL(3,2),
    DegreeProgram VARCHAR(100),
    CurrentSemester INT,
   FOREIGN KEY (StudentID) REFERENCES Users(UserID)
)


--3) Companies Table
create table Companies (
    CompanyID INT PRIMARY KEY IDENTITY,
    CompanyName VARCHAR(100),
    Sector VARCHAR(100),
    Description TEXT,
    Website VARCHAR(255)
)


--4) Recruiters Table
create table Recruiters (
    RecruiterID INT PRIMARY KEY,
    CompanyID INT,
    Designation VARCHAR(100),
    FOREIGN KEY (RecruiterID) REFERENCES Users(UserID),
    FOREIGN KEY (CompanyID) REFERENCES Companies(CompanyID)
)

--5) JobPostings Table
create table JobPostings (
    JobID INT PRIMARY KEY IDENTITY,
    CompanyID INT,
    Title VARCHAR(100),
    JobType VARCHAR(20), -- 'Internship', 'Full-time'
    SalaryRange VARCHAR(50),
    Location VARCHAR(100),
    Description TEXT,
    RequiredSkills TEXT,
    PostedBy INT,
    FOREIGN KEY (CompanyID) REFERENCES Companies(CompanyID),
    FOREIGN KEY (PostedBy) REFERENCES Recruiters(RecruiterID)
)


--6) JobFairEvents Table
create table JobFairEvents (
    JobFairID INT PRIMARY KEY IDENTITY,
    Title VARCHAR(100),
    StartDate DATE,
    EndDate DATE,
    Location VARCHAR(100),
)

--7) Applications Table
create table Applications (
    ApplicationID INT PRIMARY KEY IDENTITY,
    StudentID INT,
    JobID INT,
    Status VARCHAR(50), -- 'Applied', 'Shortlisted', 'Rejected', 'Hired'
    AppliedOn DATETIME DEFAULT GETDATE(),
    FOREIGN KEY (StudentID) REFERENCES Students(StudentID),
    FOREIGN KEY (JobID) REFERENCES JobPostings(JobID)
)

--8) Interviews Table
create table Interviews (
    InterviewID INT PRIMARY KEY IDENTITY,
    StudentID INT,
    RecruiterID INT,
    JobFairID INT,
    JobID INT,
    InterviewSlot DATETIME,
    Status VARCHAR(50), -- 'Scheduled', 'Completed', 'Cancelled'
    FOREIGN KEY (StudentID) REFERENCES Students(StudentID),
    FOREIGN KEY (RecruiterID) REFERENCES Recruiters(RecruiterID),
    FOREIGN KEY (JobFairID) REFERENCES JobFairEvents(JobFairID),
    FOREIGN KEY (JobID) REFERENCES JobPostings(JobID)
)

--9) Reviews Table
create table Reviews (
    ReviewID INT PRIMARY KEY IDENTITY,
    InterviewID INT,
    StudentID INT,
    Rating INT CHECK (Rating BETWEEN 1 AND 5),
    Comments TEXT,
    SubmittedOn DATETIME DEFAULT GETDATE(),
    FOREIGN KEY (InterviewID) REFERENCES Interviews(InterviewID),
    FOREIGN KEY (StudentID) REFERENCES Students(StudentID)
)
