# Find the number of course materials that need to be completed by a given user for each course. Sort
# the results by the number of materials left (descending). If there is a tie, the course that the student
# has most recently enrolled in should come first.
# 5 tables joined -> 1 point
# Left join -> 1 point
# 2 ordering fields -> 1 point
# Grouping -> 1 point
# 2 WHERE conditions -> 1 point
# Aggregate function (COUNT) -> 1 point
# Justification in domain: It makes sense to give the student an overview of the courses they are enrolled
# in by telling them how many materials are left for each -> 1 point
# TOTAL: 7 points
SELECT Course.name as courseName, COUNT(CourseMaterial.materialName) as materialsLeft
FROM CourseMaterial 
INNER JOIN Course on CourseMaterial.courseId = Course.id
INNER JOIN EnrolledCourse on EnrolledCourse.courseId = Course.id
INNER JOIN User on User.userId = EnrolledCourse.userId
LEFT JOIN MaterialComplete on MaterialComplete.materialId = CourseMaterial.materialId AND MaterialComplete.userId = User.userId
WHERE User.email = "GIVEN EMAIL" AND MaterialComplete.userId is NULL
GROUP BY Course.id 
ORDER BY materialsLeft DESC, EnrolledCourse.date DESC;

# Find the amount of money made per course creator and sort it in descending order.
# 4 tables joined -> 1 point
# 1 subquery -> 1 point
# Aggregate function (SUM) -> 1 point
# Grouping -> 1 point
# Non aggregate function used in SELECT (*) -> 1 point
# Justification in domain: This report could be used by an admin to find which faculty members 
# have brought in the most revenue. Could be useful for some kind of faculty reward program -> 1 point
# TOTAL: 6 points
SELECT User.email courseCreator, SUM(tmp.courseCost) courseEarnings
FROM (SELECT Course.id as courseId, Course.name, COUNT(EnrolledCourse.courseId) * Course.cost as courseCost
	  FROM Course 
	  INNER JOIN EnrolledCourse on Course.id = EnrolledCourse.courseId
	  GROUP BY Course.id) tmp
INNER JOIN CourseCreator on CourseCreator.courseId = tmp.courseId
INNER JOIN User on User.userId = CourseCreator.userId
GROUP BY CourseCreator.userId
ORDER BY SUM(tmp.courseCost) DESC;


# Sort courses by rating for the given topic (i.e. 'Database').
# 3 tables joined -> 1 point
# 1 subquery -> 1 point
# Aggregate function (AVG) -> 1 point
# LEFT/RIGHT JOIN -> 1 point
# Grouping -> 1 point
# 2 WHERE conditions -> 1 point
# Justification in domain: It is very likely that a student searching for courses may want to search
# by topic and see the best courses (highest rating) for that topic -> 1 point
# TOTAL: 7 points
SELECT Course.name as courseName, AVG(CourseCompleted.rating) as avgRating
FROM CourseCompleted 
RIGHT JOIN Course on Course.id = CourseCompleted.courseId
WHERE Course.id in (
	SELECT Course.id
	FROM Course 
	LEFT JOIN SecondaryCourse on SecondaryCourse.courseId = Course.id
	WHERE Course.primaryTopic = "GIVEN TOPIC" OR SecondaryCourse.SecondaryTopic = "GIVEN TOPIC"
)
GROUP BY Course.id
ORDER BY avgRating DESC;

# Sort courses by completion percentage (descending. if tie, the course with more completions should come first)
# 4 tables joined -> 1 point
# Left join -> 1 point
# Aggregate function (COUNT) -> 1 point
# Grouping -> 1 point
# 2 ordering fields -> 1 point
# Non aggregate function used in SELECT (/) -> 1 point
# Justification in domain: This could be used by admins/faculty to see which courses are being started but not 
# completed. This info will help them update and refine the courses as necessary -> 1 point
# TOTAL: 7 points
SELECT Course.id, Course.name, Course.description, Course.primaryTopic,
ROUND(COUNT(CourseCompleted.courseId) / COUNT(EnrolledCourse.courseId) * 100, 2) as compPercent,
COUNT(EnrolledCourse.courseId) as numEnrolled
FROM Course
LEFT JOIN EnrolledCourse on EnrolledCourse.courseId = Course.id
LEFT JOIN User on User.userId = EnrolledCourse.userId 
LEFT JOIN CourseCompleted on CourseCompleted.courseId = Course.id and User.userId = CourseCompleted.userId
GROUP BY Course.id
ORDER BY compPercent DESC, COUNT(CourseCompleted.courseId);


# Get info about the most popular courses with the given keyword in its description (i.e. 'data')
# 4 tables joined -> 1 point
# 1 subquery -> 1 point
# LEFT JOIN -> 1 point
# Aggregate function (COUNT) -> 1 point
# Grouping -> 1 point
# 2 conditions in WHERE -> 1 point
# Motivation on domain: Would be useful for students who want to search for courses pertaining to 
# a specific topic -> 1 point
# TOTAL: 6 points
SELECT Course.name as courseName, Course.description as description, COUNT(EnrolledCourse.courseId) as courseEnrollment
FROM Course
LEFT JOIN Course on Course.id = tmp.courseId
WHERE Course.description LIKE '%data%' OR Course.name LIKE '%data%'
GROUP BY Course.id
ORDER BY tmp.courseEnrollment DESC;

# For a given faculty member, get a list of their created courses which have unanswered question.
# The course with the most unanswered questions should be first. If there is a tie, the oldest question
# should be shown first
# 3 tables joined -> 1 point
# Aggregate function (COUNT, MIN) -> 1 point
# 2 conditions in WHERE -> 1 point
# Grouping -> 1 point
# 2 orderings -> 1 point
# Motivation on domain: For a faculty member, it would be useful to be able to see which courses
# need their attention
SELECT Course.id, COUNT(CourseQuestion.questionId) as questionCount, MIN(CourseQuestion.questionId) as questId
FROM CourseQuestion
INNER JOIN Course ON Course.id = CourseQuestion.courseId
INNER JOIN CourseCreator ON CourseCreator.courseId = Course.id
WHERE CourseCreator.userId = "USER_ID" and CourseQuestion.answer is NULL
GROUP BY Course.id
ORDER BY questionCount DESC, questionId ASC;

