/*
*Project 16:
*Team members:
*    Sanket Mathur
*    Eric Ropiak
*    Wei DU
*    Prasad Tajane
*
*
*Datebase - MySQL
*DDL
*/

--
-- Database: `Trainly`
--
DROP DATABASE IF EXISTS Trainly;
CREATE DATABASE IF NOT EXISTS Trainly;
USE Trainly;


-- --------------------------------------------------------

--
-- Table structure for table `User`
--

CREATE TABLE Trainly.User (
    userId VARCHAR(20),
    email VARCHAR(50) UNIQUE NOT NULL,
    fname CHAR(50),
    lname CHAR(50),
    role CHAR(20) NOT NULL,
    salt CHAR(4) NOT NULL,
    password CHAR(128) NOT NULL,
    picture BLOB,
    street VARCHAR(70),
    city CHAR(30),
    postal_code VARCHAR(15),
    country CHAR(30),
    PRIMARY KEY (userId)
);


-- --------------------------------------------------------

--
-- Table structure for table `Administrator`
--

CREATE TABLE Trainly.Administrator (
    adminId VARCHAR(20),
    role CHAR(50),
    adminGrantedBy VARCHAR(50) NOT NULL,
    grantedOnDate DATE NOT NULL,
    grantedAtTime TIME NOT NULL,
    PRIMARY KEY (adminId),
    FOREIGN KEY (adminId) REFERENCES User(userId),
    FOREIGN KEY (adminGrantedBy) REFERENCES Administrator(adminId)
);


-- --------------------------------------------------------

--
-- Table structure for table `Faculty`
--

CREATE TABLE Trainly.Faculty (
    facultyId VARCHAR(20),
    title VARCHAR(20),
    affiliation VARCHAR(50),
    website VARCHAR(100),
    facultyApprovedBy VARCHAR(50),
    approvedOnDate DATE NOT NULL,
    approvedAtTime TIME NOT NULL,
    PRIMARY KEY (facultyId),
    FOREIGN KEY (facultyId) REFERENCES User(userId),
    FOREIGN KEY (facultyApprovedBy) REFERENCES Administrator(adminId)
);


-- --------------------------------------------------------

--
-- Table structure for table `Course`
--

CREATE TABLE Trainly.Course (
    id VARCHAR(10),
    name VARCHAR(40),
    description TEXT,
    cost INT,
    creationTime DATETIME,
    primaryTopic VARCHAR(100) NOT NULL,
    PRIMARY KEY (id)
);

-- --------------------------------------------------------

--
-- Table structure for table `CourseMaterial`
--

CREATE TABLE Trainly.CourseMaterial (
    materialId CHAR(20),
    courseId VARCHAR(10),
    materialOrder SMALLINT,
    materialName VARCHAR(50),
    materialType VARCHAR(50),
    passingScore SMALLINT,
    textContent TEXT,
    path VARCHAR(100),
    size INT,
    type VARCHAR(50),
    videoFlag CHAR(1),
    Url VARCHAR(100),
    PRIMARY KEY (materialId),
    FOREIGN KEY (courseId) REFERENCES Course(id)
);

-- --------------------------------------------------------

--
-- Table structure for table `MaterialComplete`
--

CREATE TABLE Trainly.MaterialComplete (
    materialId CHAR(20),
    userId VARCHAR(50),
    date DATE,
    PRIMARY KEY (materialId, userId),
    FOREIGN KEY (materialId) REFERENCES CourseMaterial(materialId),
    FOREIGN KEY (userId) REFERENCES User(userId)
);

-- --------------------------------------------------------

--
-- Table structure for table `InterestedCourse`
--

CREATE TABLE Trainly.InterestedCourse (
    courseId VARCHAR(10),
    userId VARCHAR(50),
    PRIMARY KEY (courseId, userId),
    FOREIGN KEY (userId) REFERENCES User(userId),
    FOREIGN KEY (courseId) REFERENCES Course(id)
);

-- --------------------------------------------------------

--
-- Table structure for table `EnrolledCourse`
--

CREATE TABLE Trainly.EnrolledCourse (
    courseId VARCHAR(10),
    userId VARCHAR(50),
    time TIME,
    date DATE,
    code VARCHAR(20) UNIQUE,
    PRIMARY KEY (courseId, userId),
    FOREIGN KEY (courseId) REFERENCES Course(id),
    FOREIGN KEY (userId) REFERENCES User(userId)
);

-- --------------------------------------------------------

--
-- Table structure for table `CourseCompleted`
--

CREATE TABLE Trainly.CourseCompleted (
    courseId VARCHAR(10),
    userId VARCHAR(50),
    time Time NOT NULL,
    date DATE NOT NULL,
    rating SMALLINT,
    PRIMARY KEY (courseId, userId),
    FOREIGN KEY (courseId) REFERENCES Course(id),
    FOREIGN KEY (userId) REFERENCES User(userId)
);

-- --------------------------------------------------------

--
-- Table structure for table `CourseCreator`
--

CREATE TABLE Trainly.CourseCreator (
    courseId VARCHAR(10),
    userId VARCHAR(50),
    PRIMARY KEY (courseId, userId),
    FOREIGN KEY (courseId) REFERENCES Course(id),
    FOREIGN KEY (userId) REFERENCES User(userId)
);

-- --------------------------------------------------------

--
-- Table structure for table `Contact`
--

CREATE TABLE Trainly.Contact (
    userId VARCHAR(50),
    phoneNumber BIGINT UNIQUE,
    PRIMARY KEY (userId, phoneNumber),
    FOREIGN KEY (userId) REFERENCES User(userId)
);

-- --------------------------------------------------------

--
-- Table structure for table `PlayList`
--

CREATE TABLE Trainly.PlayList (
    playListId VARCHAR(10) PRIMARY KEY,
    name VARCHAR(50) UNIQUE
);

-- --------------------------------------------------------

--
-- Table structure for table `PlayListOwner`
--

CREATE TABLE Trainly.PlayListOwner (
    userId VARCHAR(50),
    playListId VARCHAR(10),
    PRIMARY KEY (userId, playListId),
    FOREIGN KEY (userId) REFERENCES User(userId)
);

-- --------------------------------------------------------

--
-- Table structure for table `CoursePlayList`
--

CREATE TABLE Trainly.CoursePlayList (
	playListId VARCHAR(10),
    materialId CHAR(20),
    PRIMARY KEY (playListId, materialId),
    FOREIGN KEY (playListId) REFERENCES PlayList(playListId),
    FOREIGN KEY (materialId) REFERENCES CourseMaterial(materialId)
);

-- --------------------------------------------------------

--
-- Table structure for table `QuizQuestion`
--

CREATE TABLE Trainly.QuizQuestion(
    materialId CHAR(20),
    number SMALLINT,
    text TEXT,
    PRIMARY KEY (materialId, number),
    FOREIGN KEY (materialId) REFERENCES CourseMaterial(materialId)
);

-- --------------------------------------------------------

--
-- Table structure for table `CourseQuestion`
--

CREATE TABLE Trainly.CourseQuestion (
    questionId INT AUTO_INCREMENT,
    text TEXT,
    visible CHAR(1),
    answer TEXT,
    userId VARCHAR(50),
    courseId VARCHAR(50) NOT NULL,
    PRIMARY KEY(questionId),
    FOREIGN KEY (userId) REFERENCES User(userId),
    FOREIGN KEY (courseId) REFERENCES Course(id)
);

-- --------------------------------------------------------

--
-- Table structure for table `QuestionMaterial`
--

CREATE TABLE Trainly.QuestionMaterial (
    questionId INT,
    materialId CHAR(20),
    PRIMARY KEY(questionId, materialId),
    FOREIGN KEY (questionId) REFERENCES CourseQuestion(questionId),
    FOREIGN KEY (materialId) REFERENCES CourseMaterial(materialId)
);

-- --------------------------------------------------------

--
-- Table structure for table `QuestionLike`
--

CREATE TABLE Trainly.QuestionLike (
    questionId INT,
    userId VARCHAR(50),
    PRIMARY KEY (questionId, userId),
    FOREIGN KEY (questionId) REFERENCES CourseQuestion(questionId),
    FOREIGN KEY (userId) REFERENCES User(userId)
);

-- --------------------------------------------------------

--
-- Table structure for table `QuizAnswer`
--

CREATE TABLE Trainly.QuizAnswer ( 
	letter CHAR(1), 
	qNumber SMALLINT(6), 
	materialId CHAR(20), 
	text TEXT, 
	indication CHAR(1), 
	feedback TEXT, 
	PRIMARY KEY (letter, qNumber, materialId), 
	FOREIGN KEY (materialId, qNumber) REFERENCES QuizQuestion(materialId, number)
);

-- --------------------------------------------------------

--
-- Table structure for table `SecondaryCourse`
--

CREATE TABLE Trainly.SecondaryCourse (
  courseId varchar(10) NOT NULL,
  secondaryTopic varchar(100) NOT NULL,
  PRIMARY KEY (courseId, secondaryTopic),
  FOREIGN KEY (courseId) REFERENCES Course(id)
);