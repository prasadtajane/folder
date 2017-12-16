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
*DML
*/

-- --------------------------------------------------------

--
-- Database: `Trainly`
--
USE Trainly;

-- --------------------------------------------------------

--
-- INSERT INTO USER
--

INSERT INTO Trainly.User (userId, email, fname, lname, role, salt, password, street, city, postal_code, country) 
VALUES (10001, 'Georgi.10001@somemail.com', 'Georgi','Facello', 'admin', '3eff', SHA2('3effsomepass', 256), 'Street123', 'Boston', '02115', 'USA');

INSERT INTO Trainly.User (userId, email, fname, lname, role, salt, password, street, city, postal_code, country) 
VALUES (10002, 'Bezalel.10002@somemail.com', 'Bezalel','Simmel', 'admin', 'kp3z', SHA2('kp3zsomepass', 256), 'Street123', 'Boston', '02115', 'USA');

INSERT INTO Trainly.User (userId, email, fname, lname, role, salt, password, street, city, postal_code, country) 
VALUES (10003, 'Parto.10003@somemail.com', 'Parto','Bamford', 'admin', 'bg6f', SHA2('bg6fsomepass', 256), 'Street123', 'New York', '065001', 'USA');

INSERT INTO Trainly.User (userId, email, fname, lname, role, salt, password, street, city, postal_code, country) 
VALUES (10004, 'Chirstian.10004@somemail.com', 'Chirstian','Koblick', 'admin', '23sq', SHA2('23sqsomepass', 256), 'Street123', 'New York', '202012', 'USA');

INSERT INTO Trainly.User (userId, email, fname, lname, role, salt, password, street, city, postal_code, country) 
VALUES (10005, 'Kyoichi.10005@somemail.com', 'Kyoichi','Maliniak', 'admin', 'h669', SHA2('h669somepass', 256), 'Street123', 'New York', '202012', 'USA');

INSERT INTO Trainly.User (userId, email, fname, lname, role, salt, password, street, city, postal_code, country) 
VALUES (10006, 'Anneke.10006@somemail.com', 'Anneke','Preusig', 'admin', 'D4er', SHA2('D4ersomepass', 256), 'Street123', 'New York', '202012', 'USA');

INSERT INTO Trainly.User (userId, email, fname, lname, role, salt, password, street, city, postal_code, country) 
VALUES (10007, 'Tzvetan.10007@somemail.com', 'Tzvetan','Zielinski', 'admin', 'rQH5', SHA2('rQH5somepass', 256), 'Street123', 'New York', '065001', 'USA');

INSERT INTO Trainly.User (userId, email, fname, lname, role, salt, password, street, city, postal_code, country) 
VALUES (10008, 'Saniya.10008@somemail.com', 'Saniya','Kalloufi', 'admin', 'fACW', SHA2('fACWsomepass', 256), 'Street123', 'Seattle', '02115', 'USA');

INSERT INTO Trainly.User (userId, email, fname, lname, role, salt, password, street, city, postal_code, country) 
VALUES (10009, 'Sumant.10009@somemail.com', 'Sumant','Peac', 'admin', 'tTh2', SHA2('tTh2somepass', 256), 'Street123', 'Boston', '02115', 'USA');

INSERT INTO Trainly.User (userId, email, fname, lname, role, salt, password, street, city, postal_code, country) 
VALUES (10010, 'Duangkaew.10010@somemail.com', 'Duangkaew','Piveteau', 'admin', 'cvlk', SHA2('cvlksomepass', 256), 'Street123', 'Boston', '02115', 'USA');

INSERT INTO Trainly.User (userId, email, fname, lname, role, salt, password, street, city, postal_code, country) 
VALUES (10011, 'Mary.10011@somemail.com', 'Mary','Sluis', 'faculty', '68HH', SHA2('68HHsomepass', 256), 'Street123', 'Boston', '02115', 'USA');

INSERT INTO Trainly.User (userId, email, fname, lname, role, salt, password, street, city, postal_code, country) 
VALUES (10012, 'Patricio.10012@somemail.com', 'Patricio','Bridgland', 'faculty', 'bF34', SHA2('BF34somepass', 256), 'Street123', 'New York', '065001', 'USA');

INSERT INTO Trainly.User (userId, email, fname, lname, role, salt, password, street, city, postal_code, country) 
VALUES (10013, 'Eberhardt.10013@somemail.com', 'Eberhardt','Terkki', 'faculty', 'Ty12', SHA2('Ty12somepass', 256), 'Street123', 'Seattle', '202012', 'USA');

INSERT INTO Trainly.User (userId, email, fname, lname, role, salt, password, street, city, postal_code, country) 
VALUES (10014, 'Berni.10014@somemail.com', 'Berni','Genin', 'faculty', 'hhhh', SHA2('hhhhsomepass', 256), 'Street123', 'Seattle', '202012', 'USA');

INSERT INTO Trainly.User (userId, email, fname, lname, role, salt, password, street, city, postal_code, country) 
VALUES (10015, 'Guoxiang.10015@somemail.com', 'Guoxiang','Nooteboom', 'faculty', 'klpo', SHA2('klposomepass', 256), 'Street123', 'Seattle', '202012', 'USA');

INSERT INTO Trainly.User (userId, email, fname, lname, role, salt, password, street, city, postal_code, country) 
VALUES (10016, 'Kazuhito.10016@somemail.com', 'Kazuhito','Cappelletti', 'faculty', 'we32', SHA2('we32somepass', 256), 'Street123', 'Seattle', '202012', 'USA');

INSERT INTO Trainly.User (userId, email, fname, lname, role, salt, password, street, city, postal_code, country) 
VALUES (10017, 'Cristinel.10017@somemail.com', 'Cristinel','Bouloucos', 'faculty', '7777', SHA2('7777somepass', 256), 'Street123', 'Boston', '02115', 'USA');

INSERT INTO Trainly.User (userId, email, fname, lname, role, salt, password, street, city, postal_code, country) 
VALUES (10018, 'Kazuhide.10018@somemail.com', 'Kazuhide','Peha', 'faculty', 'lp09', SHA2('lp09somepass', 256), 'Street123', 'Boston', '02115', 'USA');

INSERT INTO Trainly.User (userId, email, fname, lname, role, salt, password, street, city, postal_code, country) 
VALUES (10019, 'Lillian.10019@somemail.com', 'Lillian','Haddadi', 'faculty', 'wq21', SHA2('wq21somepass', 256), 'Street123', 'Seattle', '065001', 'USA');

INSERT INTO Trainly.User (userId, email, fname, lname, role, salt, password, street, city, postal_code, country) 
VALUES (10020, 'Mayuko.10020@somemail.com', 'Mayuko','Warwick', 'faculty', 'jasd', SHA2('jasdsomepass', 256), 'Street123', 'Boston', '02115', 'USA');

INSERT INTO Trainly.User (userId, email, fname, lname, role, salt, password, street, city, postal_code, country) 
VALUES (10021, 'Ramzi.10021@somemail.com', 'Ramzi','Erde', 'student', 'b654', SHA2('b654somepass', 256), 'Street123', 'Seattle', '065001', 'USA');

INSERT INTO Trainly.User (userId, email, fname, lname, role, salt, password, street, city, postal_code, country) 
VALUES (10022, 'Shah.10022@somemail.com', 'Shah','Famili', 'student', 'llpp', SHA2('llppsomepass', 256), 'Street123', 'Seattle', '065001', 'USA');

INSERT INTO Trainly.User (userId, email, fname, lname, role, salt, password, street, city, postal_code, country) 
VALUES (10023, 'Bojan.10023@somemail.com', 'Bojan','Montemayor', 'student', 'ASDF', SHA2('ASDFsomepass', 256), 'Street123', 'Seattle', '202012', 'USA');

INSERT INTO Trainly.User (userId, email, fname, lname, role, salt, password, street, city, postal_code, country) 
VALUES (10024, 'Suzette.10024@somemail.com', 'Suzette','Pettey', 'student', 'POO0', SHA2('POO0somepass', 256), 'Street123', 'Seattle', '202012', 'India');

INSERT INTO Trainly.User (userId, email, fname, lname, role, salt, password, street, city, postal_code, country) 
VALUES (10025, 'Prasadram.10025@somemail.com', 'Prasadram','Heyers', 'student', 'HR43', SHA2('HR43somepass', 256), 'Street123', 'Seattle', '202012', 'India');

INSERT INTO Trainly.User (userId, email, fname, lname, role, salt, password, street, city, postal_code, country) 
VALUES (10026, 'Yongqiao.10026@somemail.com', 'Yongqiao','Berztiss', 'student', 'PoYT', SHA2('POYTsomepass', 256), 'Street123', 'Seattle', '202012', 'India');

INSERT INTO Trainly.User (userId, email, fname, lname, role, salt, password, street, city, postal_code, country) 
VALUES (10027, 'Divier.10027@somemail.com', 'Divier','Reistad', 'student', 'FY65', SHA2('FY65Somepass', 256), 'Street123', 'Boston', '02115', 'USA');

INSERT INTO Trainly.User (userId, email, fname, lname, role, salt, password, street, city, postal_code, country) 
VALUES (10028, 'Domenick.10028@somemail.com', 'Domenick','Tempesti', 'student', 'H124', SHA2('H124somepass', 256), 'Street123', 'Boston', '02115', 'USA');

INSERT INTO Trainly.User (userId, email, fname, lname, role, salt, password, street, city, postal_code, country) 
VALUES (10029, 'Otmar.10029@somemail.com', 'Otmar','Herbst', 'student', 'GGGG', SHA2('GGGGsomepass', 256), 'Street123', 'Seattle', '065001', 'USA');

INSERT INTO Trainly.User (userId, email, fname, lname, role, salt, password, street, city, postal_code, country) 
VALUES (10030, 'Elvis.10030@somemail.com', 'Elvis','Demeyer', 'student', 'LH87', SHA2('LH87somepass', 256), 'Street123', 'Seattle', '065001', 'USA');


-- --------------------------------------------------------

--
-- INSERT INTO ADMINISTRATOR
--

INSERT INTO Trainly.Administrator (adminId, role, adminGrantedBy, grantedOnDate, grantedAtTime)
VALUES (10001, 'Super Admin', 10001, '2015-01-01', '08:00:00');

INSERT INTO Trainly.Administrator (adminId, role, adminGrantedBy, grantedOnDate, grantedAtTime)
VALUES (10002, 'Admin', 10001, '2015-01-01', '08:00:00');

INSERT INTO Trainly.Administrator (adminId, role, adminGrantedBy, grantedOnDate, grantedAtTime)
VALUES (10003, 'Admin', 10002, '2015-01-01', '08:00:00');

INSERT INTO Trainly.Administrator (adminId, role, adminGrantedBy, grantedOnDate, grantedAtTime)
VALUES (10004, 'Admin', 10002, '2015-01-01', '08:00:00');

INSERT INTO Trainly.Administrator (adminId, role, adminGrantedBy, grantedOnDate, grantedAtTime)
VALUES (10005, 'Admin', 10003, '2015-01-01', '08:00:00');

INSERT INTO Trainly.Administrator (adminId, role, adminGrantedBy, grantedOnDate, grantedAtTime)
VALUES (10006, 'Admin', 10001, '2015-01-01', '08:00:00');

INSERT INTO Trainly.Administrator (adminId, role, adminGrantedBy, grantedOnDate, grantedAtTime)
VALUES (10007, 'Admin', 10002, '2015-01-01', '08:00:00');

INSERT INTO Trainly.Administrator (adminId, role, adminGrantedBy, grantedOnDate, grantedAtTime)
VALUES (10008, 'Admin', 10002, '2015-01-01', '08:00:00');

INSERT INTO Trainly.Administrator (adminId, role, adminGrantedBy, grantedOnDate, grantedAtTime)
VALUES (10009, 'Admin', 10003, '2015-06-01', '10:00:00');

INSERT INTO Trainly.Administrator (adminId, role, adminGrantedBy, grantedOnDate, grantedAtTime)
VALUES (10010, 'Admin', 10003, '2015-06-01', '10:00:00');


-- --------------------------------------------------------

--
-- INSERT INTO FACULTY
--

INSERT INTO Trainly.Faculty (facultyId, title, affiliation, website, facultyApprovedBy, approvedOnDate, approvedAtTime)
VALUES (10011, 'Director', 'Faculty', 'Mary.10011.cs.com', 10002, '2015-01-02', '08:00:00');

INSERT INTO Trainly.Faculty (facultyId, title, affiliation, website, facultyApprovedBy, approvedOnDate, approvedAtTime)
VALUES (10012, 'Assistant Director', 'Faculty', 'Patricio.10012.cs.com', 10002, '2015-01-02', '08:00:00');

INSERT INTO Trainly.Faculty (facultyId, title, affiliation, website, facultyApprovedBy, approvedOnDate, approvedAtTime)
VALUES (10013, 'Professor', 'Faculty', 'iu', 10002, '2015-01-02', '08:00:00');

INSERT INTO Trainly.Faculty (facultyId, title, affiliation, website, facultyApprovedBy, approvedOnDate, approvedAtTime)
VALUES (10014, 'Professor', 'Faculty', 'Berni.10014.cs.com', 10002, '2015-01-02', '08:00:00');

INSERT INTO Trainly.Faculty (facultyId, title, affiliation, website, facultyApprovedBy, approvedOnDate, approvedAtTime)
VALUES (10015, 'Associate Professor', 'Faculty', 'Guoxiang.10015.cs.com', 10003, '2015-01-02', '08:00:00');

INSERT INTO Trainly.Faculty (facultyId, title, affiliation, website, facultyApprovedBy, approvedOnDate, approvedAtTime)
VALUES (10016, 'Associate Professor', 'Faculty', 'Kazuhito.10016.cs.com', 10003, '2015-01-02', '08:00:00');

INSERT INTO Trainly.Faculty (facultyId, title, affiliation, website, facultyApprovedBy, approvedOnDate, approvedAtTime)
VALUES (10017, 'Lecturer', 'Faculty', 'Cristinel.10017.cs.com', 10005, '2015-01-02', '08:00:00');

INSERT INTO Trainly.Faculty (facultyId, title, affiliation, website, facultyApprovedBy, approvedOnDate, approvedAtTime)
VALUES (10018, 'Lecturer', 'Faculty', 'Kazuhide.10018.cs.com', 10005, '2015-01-02', '08:00:00');

INSERT INTO Trainly.Faculty (facultyId, title, affiliation, website, facultyApprovedBy, approvedOnDate, approvedAtTime)
VALUES (10019, 'Lecturer', 'Faculty', 'Lillian.10019.cs.com', 10005, '2015-01-02', '08:00:00');

INSERT INTO Trainly.Faculty (facultyId, title, affiliation, website, facultyApprovedBy, approvedOnDate, approvedAtTime)
VALUES (10020, 'Lecturer', 'Faculty', 'Mayuko.10020.cs.com', 10005, '2015-01-02', '08:00:00');


-- --------------------------------------------------------

--
-- INSERT INTO CONTACT
--

INSERT INTO Trainly.Contact (userId, phoneNumber)
VALUES (10001, 5250491525);

INSERT INTO Trainly.Contact (userId, phoneNumber)
VALUES (10002, 3486284529);

INSERT INTO Trainly.Contact (userId, phoneNumber)
VALUES (10002, 6358340772);

INSERT INTO Trainly.Contact (userId, phoneNumber)
VALUES (10003, 3424466457);

INSERT INTO Trainly.Contact (userId, phoneNumber)
VALUES (10004, 2663709358);

INSERT INTO Trainly.Contact (userId, phoneNumber)
VALUES (10004, 7113839767);

INSERT INTO Trainly.Contact (userId, phoneNumber)
VALUES (10004, 9552171923);

INSERT INTO Trainly.Contact (userId, phoneNumber)
VALUES (10005, 8776196308);

INSERT INTO Trainly.Contact (userId, phoneNumber)
VALUES (10006, 9693661250);

INSERT INTO Trainly.Contact (userId, phoneNumber)
VALUES (10007, 2216075231);

INSERT INTO Trainly.Contact (userId, phoneNumber)
VALUES (10008, 9814876982);

INSERT INTO Trainly.Contact (userId, phoneNumber)
VALUES (10009, 8313335555);

INSERT INTO Trainly.Contact (userId, phoneNumber)
VALUES (10010, 3738518970);

INSERT INTO Trainly.Contact (userId, phoneNumber)
VALUES (10011, 2531713038);

INSERT INTO Trainly.Contact (userId, phoneNumber)
VALUES (10011, 1137378149);

INSERT INTO Trainly.Contact (userId, phoneNumber)
VALUES (10012, 3470874275);

INSERT INTO Trainly.Contact (userId, phoneNumber)
VALUES (10012, 3304662497);

INSERT INTO Trainly.Contact (userId, phoneNumber)
VALUES (10013, 9480591821);

INSERT INTO Trainly.Contact (userId, phoneNumber)
VALUES (10014, 2031582693);

INSERT INTO Trainly.Contact (userId, phoneNumber)
VALUES (10015, 4585789152);

INSERT INTO Trainly.Contact (userId, phoneNumber)
VALUES (10016, 5759539641);

INSERT INTO Trainly.Contact (userId, phoneNumber)
VALUES (10017, 4308477515);

INSERT INTO Trainly.Contact (userId, phoneNumber)
VALUES (10017, 1532055418);

INSERT INTO Trainly.Contact (userId, phoneNumber)
VALUES (10018, 6248728441);

INSERT INTO Trainly.Contact (userId, phoneNumber)
VALUES (10019, 9722654307);

INSERT INTO Trainly.Contact (userId, phoneNumber)
VALUES (10020, 2811781991);

INSERT INTO Trainly.Contact (userId, phoneNumber)
VALUES (10021, 9540565281);

INSERT INTO Trainly.Contact (userId, phoneNumber)
VALUES (10021, 2084433135);

INSERT INTO Trainly.Contact (userId, phoneNumber)
VALUES (10021, 4439225298);

INSERT INTO Trainly.Contact (userId, phoneNumber)
VALUES (10022, 7906036220);

INSERT INTO Trainly.Contact (userId, phoneNumber)
VALUES (10023, 4319137952);

INSERT INTO Trainly.Contact (userId, phoneNumber)
VALUES (10024, 7207146640);

INSERT INTO Trainly.Contact (userId, phoneNumber)
VALUES (10025, 9639551410);

INSERT INTO Trainly.Contact (userId, phoneNumber)
VALUES (10025, 7917727466);

INSERT INTO Trainly.Contact (userId, phoneNumber)
VALUES (10026, 5811430808);

INSERT INTO Trainly.Contact (userId, phoneNumber)
VALUES (10027, 7014034615);

INSERT INTO Trainly.Contact (userId, phoneNumber)
VALUES (10028, 1851182488);

INSERT INTO Trainly.Contact (userId, phoneNumber)
VALUES (10028, 6048004628);

INSERT INTO Trainly.Contact (userId, phoneNumber)
VALUES (10029, 8470418709);

INSERT INTO Trainly.Contact (userId, phoneNumber)
VALUES (10030, 9270493213);


-- --------------------------------------------------------

--
-- INSERT INTO COURSE
--

INSERT INTO Trainly.Course (id, name, description, cost, creationTime, primaryTopic)
VALUES ('CS1001', 'Databases Programming', 'This overview course focuses on the uses of relational and object-oriented databases for storing and managing information. Topics covered include computer database terminology and the evolution of the modern database. Database management systems (DBMS) such as Oracle, MySQL, Microsoft SQL Server, and Microsoft Access are introduced along with query languages. Hands-on instruction includes the creation of simple databases, inputting data, and developing basic queries.', 500, '2015-02-01 08:00:00', 'Database');

INSERT INTO Trainly.Course (id, name, description, cost, creationTime, primaryTopic)
VALUES ('CS1002', 'Natural Language Processing', 'Introduces the computational modeling of human language; the ongoing effort to create computer programs that can communicate with people in natural language; and current applications of the natural language field, such as automated document classification, intelligent query processing, and information extraction. Topics include computational models of grammar and automatic parsing, statistical language models and the analysis of large text corpora, natural language semantics and programs that understand language, models of discourse structure, and language use by intelligent agents. Course work includes formal and mathematical analysis of language models and implementation of working programs that analyze and interpret natural language text. Knowledge of statistics is helpful. ', 500, '2015-02-01 08:00:00', 'Computational Modeling of Human Language');

INSERT INTO Trainly.Course (id, name, description, cost, creationTime, primaryTopic)
VALUES ('CS1003', 'Computer Graphics', 'Charts a path through every major aspect of computer graphics with varying degrees of emphasis. Discusses hardware issues: size and speed; lines, polygons, and regions; modeling, or objects and their relations; viewing, or what can be seen (visibility and perspective); rendering, or how it looks (properties of surfaces, light, and color); transformations, or moving, placing, distorting, and animating and interaction, or drawing, selecting, and transforming. ', 500, '2015-02-01 08:00:00', 'Programming in C');

INSERT INTO Trainly.Course (id, name, description, cost, creationTime, primaryTopic)
VALUES ('CS1004', 'Compilers', 'Studies the construction of compilers and integrates material from earlier courses on programming languages, automata theory, computer architecture, and software design. Examines syntax trees; static semantics; type checking; typical machine architectures and their software structures; code generation; lexical analysis; and parsing techniques. Uses a hands-on approach with a substantial term project. ', 500, '2015-02-01 08:00:00', 'Compilers and Interpreters');

INSERT INTO Trainly.Course (id, name, description, cost, creationTime, primaryTopic)
VALUES ('CS1005', 'Developing Web Databases', 'Internet retailers collect an incredible amount of data in order to complete a sale, including customer names, addresses, and credit card numbers. The data is inputted by the buyer and stored in a relational database for retrieval by the seller.', 500, '2015-02-01 08:00:00', 'Database');

INSERT INTO Trainly.Course (id, name, description, cost, creationTime, primaryTopic)
VALUES ('CS1006', 'Discrete Structures', 'Introduces the mathematical structures and methods that form the foundation of computer science. Studies structures such as sets, tuples, sequences, lists, trees, and graphs. Discusses functions, relations, ordering, and equivalence relations. Examines inductive and recursive definitions of structures and functions. Discusses principles of proof such as truth tables, inductive proof, and basic logic. Also covers the counting techniques and arguments needed to estimate the size of sets, the growth of functions, and the space-time complexity of algorithms. ', 500, '2015-02-01 08:00:00', 'Algorithms');

INSERT INTO Trainly.Course (id, name, description, cost, creationTime, primaryTopic)
VALUES ('CS1007', 'Computer Science and Its Application', 'Introduces students to the field of computer science and the patterns of thinking that enable them to become intelligent users of software tools in a problem-solving setting. Examines several important software applications so that students may develop the skills necessary to use computers effectively in their own disciplines.', 500, '2015-02-01 08:00:00', 'Software Development');

INSERT INTO Trainly.Course (id, name, description, cost, creationTime, primaryTopic)
VALUES ('CS1008', 'Web Development', 'Discusses Web development for sites that are dynamic, data driven, and interactive. Focuses on the software development issues of integrating multiple languages, assorted data technologies, and Web interaction. Considers ASP.NET, C#, HTTP, HTML, CSS, XML, XSLT, JavaScript, AJAX, RSS/Atom, SQL, and Web services. Requires each student to deploy individually designed Web experiments that illustrate the Web technologies and at least one major integrative Web site project. Students may work as a team with the permission of the instructor. Each student or team must also create extensive documentation of their goals, plans, design decisions, accomplishments, and user guidelines. All source files must be open and be automatically served by a sources server.', 500, '2015-02-01 08:00:00', 'HTML and CSS Basics');

INSERT INTO Trainly.Course (id, name, description, cost, creationTime, primaryTopic)
VALUES ('CS1009', 'Programming in C++', 'Examines how to program in C++ in a robust and safe manner. Reviews basics, including scoping, typing, and primitive data structures. Discusses data types (primitive, array, structure, class, string); addressing/parameter mechanisms (value, pointer, reference); stacks; queues; linked lists; binary trees; hash tables; and the design of classes and class inheritance, emphasizing single inheritance. Considers the instantiation of objects, the trade-offs of stack vs. heap allocation, and the design of constructors and destructors. Emphasizes the need for a strategy for dynamic memory management. Addresses function and operator overloading; templates, the Standard Template Library (STL), and the STL components (containers, generic algorithms, iterators, adaptors, allocators, function objects); streams; exception handling; and system calls for processes and threads ', 500, '2015-02-01 08:00:00', 'object-oriented Programming');

INSERT INTO Trainly.Course (id, name, description, cost, creationTime, primaryTopic)
VALUES ('CS1010', 'Game Programming', 'Introduces the different subsystems used to create a 3D game, including rendering, animation, collision, physics, audio, trigger systems, game logic, behavior trees, and simple artificial intelligence. Offers students an opportunity to learn the inner workings of game engines and how to use multiple libraries such as physics and graphics libraries to develop a game. Discusses graphics pipeline, scene graph, level design, behavior scripting, object-oriented game design, world editors, and game scripting languages. ', 500, '2015-02-01 08:00:00', 'Gaming Design');

INSERT INTO Trainly.Course (id, name, description, cost, creationTime, primaryTopic)
VALUES ('CS1011', 'Artificial Intelligence', 'Introduces the fundamental problems, theories, and algorithms of the artificial intelligence field. Includes heuristic search; knowledge representation using predicate calculus; automated deduction and its applications; planning; and machine learning. Additional topics include game playing; uncertain reasoning and expert systems; natural language processing; logic for common-sense reasoning; ontologies; and multiagent systems. ', 500, '2015-02-01 08:00:00', 'Python Programming');


-- --------------------------------------------------------

--
-- INSERT INTO COURSECREATOR
--

INSERT INTO Trainly.CourseCreator (courseId, userId)
VALUES ('CS1001', 10013);

INSERT INTO Trainly.CourseCreator (courseId, userId)
VALUES ('CS1002', 10013);

INSERT INTO Trainly.CourseCreator (courseId, userId)
VALUES ('CS1003', 10013);

INSERT INTO Trainly.CourseCreator (courseId, userId)
VALUES ('CS1004', 10013);

INSERT INTO Trainly.CourseCreator (courseId, userId)
VALUES ('CS1005', 10013);

INSERT INTO Trainly.CourseCreator (courseId, userId)
VALUES ('CS1006', 10003);

INSERT INTO Trainly.CourseCreator (courseId, userId)
VALUES ('CS1007', 10003);

INSERT INTO Trainly.CourseCreator (courseId, userId)
VALUES ('CS1008', 10006);

INSERT INTO Trainly.CourseCreator (courseId, userId)
VALUES ('CS1009', 10006);

INSERT INTO Trainly.CourseCreator (courseId, userId)
VALUES ('CS1010', 10007);

INSERT INTO Trainly.CourseCreator (courseId, userId)
VALUES ('CS1011', 10008);


-- --------------------------------------------------------

--
-- INSERT INTO SECONDARYCOURSE
--

INSERT INTO Trainly.SecondaryCourse (courseId, secondaryTopic)
VALUES ('CS1001', 'Programming in SQL');

INSERT INTO Trainly.SecondaryCourse (courseId, secondaryTopic)
VALUES ('CS1001', 'Database Design');

INSERT INTO Trainly.SecondaryCourse (courseId, secondaryTopic)
VALUES ('CS1001', 'Relational Database');

INSERT INTO Trainly.SecondaryCourse (courseId, secondaryTopic)
VALUES ('CS1004', 'Automata Theory');

INSERT INTO Trainly.SecondaryCourse (courseId, secondaryTopic)
VALUES ('CS1004', 'Software Design');

INSERT INTO Trainly.SecondaryCourse (courseId, secondaryTopic)
VALUES ('CS1006', 'Data Structures');

INSERT INTO Trainly.SecondaryCourse (courseId, secondaryTopic)
VALUES ('CS1007', 'Computer Architecture');

INSERT INTO Trainly.SecondaryCourse (courseId, secondaryTopic)
VALUES ('CS1008', 'Angular JS');

INSERT INTO Trainly.SecondaryCourse (courseId, secondaryTopic)
VALUES ('CS1008', 'Node JS');

INSERT INTO Trainly.SecondaryCourse (courseId, secondaryTopic)
VALUES ('CS1011', 'Special tpoics in AI');

INSERT INTO Trainly.SecondaryCourse (courseId, secondaryTopic)
VALUES ('CS1009', 'Inheritance, abstraction and Polymorphism');


-- --------------------------------------------------------

--
-- INSERT INTO COURSEMATERIAL
--

INSERT INTO Trainly.CourseMaterial (materialId, courseId, materialOrder, materialName, materialType, passingScore, textContent, path, size, type, videoFlag, Url)
VALUES ('M001', 'CS1001', 4, 'Programming Quiz', 'Quiz', 50, null, null, null, null, null, null);

INSERT INTO Trainly.CourseMaterial (materialId, courseId, materialOrder, materialName, materialType, passingScore, textContent, path, size, type, videoFlag, Url)
VALUES ('M002', 'CS1009', 4, 'Database Quiz', 'Quiz', 50, null, null, null, null, null, null);

INSERT INTO Trainly.CourseMaterial (materialId, courseId, materialOrder, materialName, materialType, passingScore, textContent, path, size, type, videoFlag, Url)
VALUES ('M003', 'CS1008', 1, 'Web Development Quiz', 'Quiz', 50, null, null, null, null, null, null);

INSERT INTO Trainly.CourseMaterial (materialId, courseId, materialOrder, materialName, materialType, passingScore, textContent, path, size, type, videoFlag, Url)
VALUES ('M004', 'CS1009', 3, 'Programming Post', 'Post', null, 'Computer programming (often shortened to programming) is a process that leads from an original formulation of a computing problem to executable computer programs.', null, null, null, null, null);

INSERT INTO Trainly.CourseMaterial (materialId, courseId, materialOrder, materialName, materialType, passingScore, textContent, path, size, type, videoFlag, Url)
VALUES ('M005', 'CS1005', 3, 'Database Post', 'Post', null, 'A database is an organized collection of data. A relational database, more restrictively, is a collection of schemas, tables, queries, reports, views, and other elements.', null, null, null, null, null);

INSERT INTO Trainly.CourseMaterial (materialId, courseId, materialOrder, materialName, materialType, passingScore, textContent, path, size, type, videoFlag, Url)
VALUES ('M006', 'CS1003', 3, 'Computer Architecture Post', 'Post', null, 'In computer engineering, computer architecture is a set of rules and methods that describe the functionality, organization, and implementation of computer systems.', null, null, null, null, null);

INSERT INTO Trainly.CourseMaterial (materialId, courseId, materialOrder, materialName, materialType, passingScore, textContent, path, size, type, videoFlag, Url)
VALUES ('M007', 'CS1001', 2, 'Programming File', 'File', null, null, '/somepath/file', 1000, 'java', null, null);

INSERT INTO Trainly.CourseMaterial (materialId, courseId, materialOrder, materialName, materialType, passingScore, textContent, path, size, type, videoFlag, Url)
VALUES ('M008', 'CS1011', 2, 'Artificial Intelligence File', 'File', null, null, '/somepath/file', 900, 'py', null, null);

INSERT INTO Trainly.CourseMaterial (materialId, courseId, materialOrder, materialName, materialType, passingScore, textContent, path, size, type, videoFlag, Url)
VALUES ('M009', 'CS1010', 2, 'Game Programming File', 'File', null, null, '/somepath/file', 1000, 'py', null, null);

INSERT INTO Trainly.CourseMaterial (materialId, courseId, materialOrder, materialName, materialType, passingScore, textContent, path, size, type, videoFlag, Url)
VALUES ('M010', 'CS1001', 1, 'Programming Link', 'Link', null, null, null, null, null, 'N', 'https://www.somelink.com');

INSERT INTO Trainly.CourseMaterial (materialId, courseId, materialOrder, materialName, materialType, passingScore, textContent, path, size, type, videoFlag, Url)
VALUES ('M011', 'CS1005', 1, 'Database Link', 'Link', null, null, null, null, null, 'Y', 'https://www.somelink.com');

INSERT INTO Trainly.CourseMaterial (materialId, courseId, materialOrder, materialName, materialType, passingScore, textContent, path, size, type, videoFlag, Url)
VALUES ('M012','CS1010', 1, 'Gaming Link', 'Link', null, null, null, null, null, 'Y', 'https://www.somelink.com');


-- --------------------------------------------------------

--
-- INSERT INTO MATERIALCOMPLETE
--

INSERT INTO Trainly.MaterialComplete (materialId, userId, date)
VALUES ('M001', '10021', '2015-01-02');

INSERT INTO Trainly.MaterialComplete (materialId, userId, date)
VALUES ('M001', '10022', '2015-01-02');

INSERT INTO Trainly.MaterialComplete (materialId, userId, date)
VALUES ('M001', '10023', '2015-01-02');

INSERT INTO Trainly.MaterialComplete (materialId, userId, date)
VALUES ('M001', '10024', '2015-01-02');

INSERT INTO Trainly.MaterialComplete (materialId, userId, date)
VALUES ('M001', '10025', '2015-01-02');

INSERT INTO Trainly.MaterialComplete (materialId, userId, date)
VALUES ('M001', '10026', '2015-01-02');

INSERT INTO Trainly.MaterialComplete (materialId, userId, date)
VALUES ('M001', '10027', '2015-01-02');

INSERT INTO Trainly.MaterialComplete (materialId, userId, date)
VALUES ('M001', '10028', '2015-01-02');

INSERT INTO Trainly.MaterialComplete (materialId, userId, date)
VALUES ('M001', '10029', '2015-01-02');

INSERT INTO Trainly.MaterialComplete (materialId, userId, date)
VALUES ('M001', '10030', '2015-01-02');

INSERT INTO Trainly.MaterialComplete (materialId, userId, date)
VALUES ('M002', '10021', '2015-01-02');

INSERT INTO Trainly.MaterialComplete (materialId, userId, date)
VALUES ('M002', '10023', '2015-01-02');

INSERT INTO Trainly.MaterialComplete (materialId, userId, date)
VALUES ('M002', '10025', '2015-01-02');

INSERT INTO Trainly.MaterialComplete (materialId, userId, date)
VALUES ('M002', '10027', '2015-01-02');

INSERT INTO Trainly.MaterialComplete (materialId, userId, date)
VALUES ('M002', '10029', '2015-01-02');

INSERT INTO Trainly.MaterialComplete (materialId, userId, date)
VALUES ('M003', '10022', '2015-01-02');

INSERT INTO Trainly.MaterialComplete (materialId, userId, date)
VALUES ('M003', '10026', '2015-01-02');

INSERT INTO Trainly.MaterialComplete (materialId, userId, date)
VALUES ('M003', '10028', '2015-01-02');

INSERT INTO Trainly.MaterialComplete (materialId, userId, date)
VALUES ('M003', '10030', '2015-01-02');

INSERT INTO Trainly.MaterialComplete (materialId, userId, date)
VALUES ('M004', '10021', '2015-01-02');

INSERT INTO Trainly.MaterialComplete (materialId, userId, date)
VALUES ('M004', '10030', '2015-01-02');

INSERT INTO Trainly.MaterialComplete (materialId, userId, date)
VALUES ('M005', '10021', '2015-01-02');

INSERT INTO Trainly.MaterialComplete (materialId, userId, date)
VALUES ('M005', '10030', '2015-01-02');

INSERT INTO Trainly.MaterialComplete (materialId, userId, date)
VALUES ('M006', '10021', '2015-01-02');

INSERT INTO Trainly.MaterialComplete (materialId, userId, date)
VALUES ('M006', '10022', '2015-01-02');

INSERT INTO Trainly.MaterialComplete (materialId, userId, date)
VALUES ('M006', '10030', '2015-01-02');

INSERT INTO Trainly.MaterialComplete (materialId, userId, date)
VALUES ('M007', '10021', '2015-01-02');

INSERT INTO Trainly.MaterialComplete (materialId, userId, date)
VALUES ('M007', '10030', '2015-01-02');

INSERT INTO Trainly.MaterialComplete (materialId, userId, date)
VALUES ('M008', '10021', '2015-01-02');

INSERT INTO Trainly.MaterialComplete (materialId, userId, date)
VALUES ('M008', '10030', '2015-01-02');

INSERT INTO Trainly.MaterialComplete (materialId, userId, date)
VALUES ('M009', '10021', '2015-01-02');

INSERT INTO Trainly.MaterialComplete (materialId, userId, date)
VALUES ('M009', '10030', '2015-01-02');

INSERT INTO Trainly.MaterialComplete (materialId, userId, date)
VALUES ('M010', '10021', '2015-01-02');

INSERT INTO Trainly.MaterialComplete (materialId, userId, date)
VALUES ('M010', '10030', '2015-01-02');


-- --------------------------------------------------------

--
-- INSERT INTO INTERESTEDCOURSE
--

INSERT INTO Trainly.InterestedCourse (courseId, userId)
VALUES ('CS1001', '10021');

INSERT INTO Trainly.InterestedCourse (courseId, userId)
VALUES ('CS1001', '10022');

INSERT INTO Trainly.InterestedCourse (courseId, userId)
VALUES ('CS1001', '10023');

INSERT INTO Trainly.InterestedCourse (courseId, userId)
VALUES ('CS1001', '10024');

INSERT INTO Trainly.InterestedCourse (courseId, userId)
VALUES ('CS1001', '10025');

INSERT INTO Trainly.InterestedCourse (courseId, userId)
VALUES ('CS1001', '10026');

INSERT INTO Trainly.InterestedCourse (courseId, userId)
VALUES ('CS1002', '10021');

INSERT INTO Trainly.InterestedCourse (courseId, userId)
VALUES ('CS1006', '10021');

INSERT INTO Trainly.InterestedCourse (courseId, userId)
VALUES ('CS1002', '10022');

INSERT INTO Trainly.InterestedCourse (courseId, userId)
VALUES ('CS1002', '10023');

INSERT INTO Trainly.InterestedCourse (courseId, userId)
VALUES ('CS1002', '10024');

INSERT INTO Trainly.InterestedCourse (courseId, userId)
VALUES ('CS1002', '10025');

INSERT INTO Trainly.InterestedCourse (courseId, userId)
VALUES ('CS1003', '10025');

INSERT INTO Trainly.InterestedCourse (courseId, userId)
VALUES ('CS1003', '10026');

INSERT INTO Trainly.InterestedCourse (courseId, userId)
VALUES ('CS1003', '10027');

INSERT INTO Trainly.InterestedCourse (courseId, userId)
VALUES ('CS1004', '10024');

INSERT INTO Trainly.InterestedCourse (courseId, userId)
VALUES ('CS1004', '10022');

INSERT INTO Trainly.InterestedCourse (courseId, userId)
VALUES ('CS1005', '10022');

INSERT INTO Trainly.InterestedCourse (courseId, userId)
VALUES ('CS1005', '10027');

INSERT INTO Trainly.InterestedCourse (courseId, userId)
VALUES ('CS1006', '10028');

INSERT INTO Trainly.InterestedCourse (courseId, userId)
VALUES ('CS1006', '10029');

INSERT INTO Trainly.InterestedCourse (courseId, userId)
VALUES ('CS1007', '10030');

-- --------------------------------------------------------

--
-- INSERT INTO ENROLLEDCOURSE
--

INSERT INTO Trainly.EnrolledCourse (courseId, userId, date, time, code)
VALUES ('CS1001', '10021', '2015-01-02', '08:00:00', 'TXN100001');

INSERT INTO Trainly.EnrolledCourse (courseId, userId, date, time, code)
VALUES ('CS1001', '10022', '2015-01-02', '08:00:00', 'TXN100002');

INSERT INTO Trainly.EnrolledCourse (courseId, userId, date, time, code)
VALUES ('CS1001', '10023', '2015-01-02', '08:00:00', 'TXN100003');

INSERT INTO Trainly.EnrolledCourse (courseId, userId, date, time, code)
VALUES ('CS1001', '10024', '2015-01-02', '08:00:00', 'TXN100004');

INSERT INTO Trainly.EnrolledCourse (courseId, userId, date, time, code)
VALUES ('CS1001', '10025', '2015-01-02', '08:00:00', 'TXN100005');

INSERT INTO Trainly.EnrolledCourse (courseId, userId, date, time, code)
VALUES ('CS1001', '10026', '2015-01-02', '08:00:00', 'TXN100006');

INSERT INTO Trainly.EnrolledCourse (courseId, userId, date, time, code)
VALUES ('CS1001', '10027', '2015-01-02', '08:00:00', 'TXN100007');

INSERT INTO Trainly.EnrolledCourse (courseId, userId, date, time, code)
VALUES ('CS1001', '10028', '2015-01-02', '08:00:00', 'TXN100008');

INSERT INTO Trainly.EnrolledCourse (courseId, userId, date, time, code)
VALUES ('CS1001', '10029', '2015-01-02', '08:00:00', 'TXN100009');

INSERT INTO Trainly.EnrolledCourse (courseId, userId, date, time, code)
VALUES ('CS1001', '10030', '2015-01-02', '08:00:00', 'TXN100010');

INSERT INTO Trainly.EnrolledCourse (courseId, userId, date, time, code)
VALUES ('CS1009', '10021', '2015-01-02', '08:00:00', 'TXN100011');

INSERT INTO Trainly.EnrolledCourse (courseId, userId, date, time, code)
VALUES ('CS1009', '10023', '2015-01-02', '08:00:00', 'TXN100012');

INSERT INTO Trainly.EnrolledCourse (courseId, userId, date, time, code)
VALUES ('CS1009', '10025', '2015-01-02', '08:00:00', 'TXN100013');

INSERT INTO Trainly.EnrolledCourse (courseId, userId, date, time, code)
VALUES ('CS1009', '10027', '2015-01-02', '08:00:00', 'TXN100014');

INSERT INTO Trainly.EnrolledCourse (courseId, userId, date, time, code)
VALUES ('CS1009', '10029', '2015-01-02', '08:00:00', 'TXN100015');

INSERT INTO Trainly.EnrolledCourse (courseId, userId, date, time, code)
VALUES ('CS1008', '10022', '2015-01-02', '08:00:00', 'TXN100016');

INSERT INTO Trainly.EnrolledCourse (courseId, userId, date, time, code)
VALUES ('CS1008', '10026', '2015-01-02', '08:00:00', 'TXN100017');

INSERT INTO Trainly.EnrolledCourse (courseId, userId, date, time, code)
VALUES ('CS1008', '10028', '2015-01-02', '08:00:00', 'TXN100018');

INSERT INTO Trainly.EnrolledCourse (courseId, userId, date, time, code)
VALUES ('CS1008', '10030', '2015-01-02', '08:00:00', 'TXN100019');

INSERT INTO Trainly.EnrolledCourse (courseId, userId, date, time, code)
VALUES ('CS1005', '10021', '2015-01-02', '08:00:00', 'TXN100020');

INSERT INTO Trainly.EnrolledCourse (courseId, userId, date, time, code)
VALUES ('CS1005', '10030', '2015-01-02', '08:00:00', 'TXN100021');

INSERT INTO Trainly.EnrolledCourse (courseId, userId, date, time, code)
VALUES ('CS1003', '10021', '2015-01-02', '08:00:00', 'TXN100022');

INSERT INTO Trainly.EnrolledCourse (courseId, userId, date, time, code)
VALUES ('CS1003', '10022', '2015-01-02', '08:00:00', 'TXN100023');

INSERT INTO Trainly.EnrolledCourse (courseId, userId, date, time, code)
VALUES ('CS1003', '10030', '2015-01-02', '08:00:00', 'TXN100024');

INSERT INTO Trainly.EnrolledCourse (courseId, userId, date, time, code)
VALUES ('CS1011', '10021', '2015-01-02', '08:00:00', 'TXN100025');

INSERT INTO Trainly.EnrolledCourse (courseId, userId, date, time, code)
VALUES ('CS1011', '10030', '2015-01-02', '08:00:00', 'TXN100026');

INSERT INTO Trainly.EnrolledCourse (courseId, userId, date, time, code)
VALUES ('CS1010', '10021', '2015-01-02', '08:00:00', 'TXN100027');

INSERT INTO Trainly.EnrolledCourse (courseId, userId, date, time, code)
VALUES ('CS1010', '10030', '2015-01-02', '08:00:00', 'TXN100028');

INSERT INTO Trainly.EnrolledCourse (courseId, userId, date, time, code)
VALUES ('CS1008', '10021', '2015-01-02', '08:00:00', 'TXN100029');

INSERT INTO Trainly.EnrolledCourse (courseId, userId, date, time, code)
VALUES ('CS1002', '10021', '2015-01-02', '08:00:00', 'TXN100030');


-- --------------------------------------------------------

--
-- INSERT INTO COURSECOMPLETE
--

INSERT INTO Trainly.CourseCompleted (courseId, userId, date, time, rating)
VALUES ('CS1001', '10028', '2015-01-02', '08:00:00', 5);

INSERT INTO Trainly.CourseCompleted (courseId, userId, date, time, rating)
VALUES ('CS1001', '10023', '2015-01-02', '08:00:00', 3);

INSERT INTO Trainly.CourseCompleted (courseId, userId, date, time, rating)
VALUES ('CS1001', '10024', '2015-01-02', '08:00:00', 5);

INSERT INTO Trainly.CourseCompleted (courseId, userId, date, time, rating)
VALUES ('CS1001', '10021', '2015-01-02', '08:00:00', 5);

INSERT INTO Trainly.CourseCompleted (courseId, userId, date, time, rating)
VALUES ('CS1005', '10021', '2015-01-02', '08:00:00', 2);

INSERT INTO Trainly.CourseCompleted (courseId, userId, date, time, rating)
VALUES ('CS1005', '10030', '2015-01-02', '08:00:00', 3);



