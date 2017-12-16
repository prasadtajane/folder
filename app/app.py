from __future__ import print_function
from flask import Flask, g, jsonify, redirect, render_template, request, session, url_for
from functools import wraps
from wtforms.form import Form
import wtforms.validators as validators
from wtforms.fields import FileField, BooleanField, IntegerField, TextAreaField, SubmitField, \
    StringField, PasswordField, SelectMultipleField, SelectField
from wtforms.validators import Email
import datetime
import random
import hashlib
import string
import itertools
import json
import pymysql
import sys

app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.secret_key = 'please dont try to break my site'


# Creates a connection with the locally running database and returns the
# connction to be used for a query
def get_db_connection():
	return pymysql.connect(host='localhost',
						   user='root',
						   password='',
						   db='Trainly',
						   charset='utf8',
						   cursorclass=pymysql.cursors.DictCursor)


# A wrapper that is used to ensure only users with the correct user roles
# can access certain routes. For instance, a student should not be able to
# access the /admin/ route. If they try, they will be redirected to the
# landing page
def requires_roles(*roles):
	def wrapper(f):
		@wraps(f)
		def wrapped(*args, **kwargs):
			no_role = roles == (None,)
			if (no_role and len(g.user_roles)) or (not no_role and not len(g.user_roles.intersection(list(roles)))):
				return redirect(url_for('landing_page'))
			return f(*args, **kwargs)

		return wrapped

	return wrapper


# Returns a random string that is 4 characters long to be used as a user's salt
def get_salt():
	return ''.join(random.choice(string.ascii_lowercase + string.ascii_uppercase + string.digits) for _ in range(4))


# Runs on every request. Looks to see if there is a user id stored in the
# brower's session representing a logged in user. If so, it queries
# the db to get info about that user and sets it on the g global object
@app.before_request
def before_request():
	g.user = None
	g.user_roles = set()
	if 'userId' in session and session['userId']:
		connection = get_db_connection()
		with connection.cursor() as cursor:
			sql = ('SELECT * FROM User '
				   'LEFT JOIN Faculty ON User.userId = Faculty.facultyId '
				   'LEFT JOIN Administrator ON User.userId = Administrator.adminId '
				   'WHERE userId = %s '
				   'AND active = "Y";')
			cursor.execute(sql, (session['userId']))
			result = cursor.fetchone()
			if result:
				g.user = result
				g.user_roles.add('student')
				if result['adminGrantedBy']:
					g.user_roles.add('admin')
				if result['facultyApprovedBy']:
					g.user_roles.add('faculty')


# Log in as the user with the given user id. This is horrible for security,
# but makes it much much easier to test/view all of the site's funcitonality
@app.route("/switch_user/<string:user_id>/")
def switch_user(user_id):
	connection = get_db_connection()
	with connection.cursor() as cursor:
		sql = ('SELECT * FROM User '
			   'LEFT JOIN Faculty ON User.userId = Faculty.facultyId '
			   'LEFT JOIN Administrator ON User.userId = Administrator.adminId '
			   'WHERE userId = %s '
			   'AND active = "Y";')
		cursor.execute(sql, user_id)
		result = cursor.fetchone()

		if result:
			session['userId'] = user_id

	return redirect(request.referrer)


# Landing page for the trainly app
@app.route("/")
def landing_page():
	g.user_role = 'faculty'
	can_sign_in = getattr(g, 'user_id', None) == None
	return render_template("landing_page.html", can_sign_in=can_sign_in)


# WTFForm used when a user is signing in. Verfies that both the
# email address and password fields are filled out
class SignInForm(Form):
	email = StringField('Email Address', [validators.DataRequired()])
	password = PasswordField('New Password', [validators.DataRequired()])


# Route for signing in. When posted to, it validates the sign in form
# and checks if the user's email and password match what is stored
# in the db. If so, it signs in the user by storing their userId
# in the browser's session
@app.route("/sign_in", methods=['GET', 'POST'])
def sign_in():
	form = SignInForm(request.form)
	if request.method == 'POST' and form.validate():
		email = form.email.data
		password = form.password.data
		connection = get_db_connection()
		with connection.cursor() as cursor:
			sql = 'SELECT * FROM User WHERE email = %s AND active = "Y";'
			cursor.execute(sql, (email))
			result = cursor.fetchone()

			if result:
				salt_plus_password = result['salt'] + password
				hash_object = hashlib.sha256(salt_plus_password.encode())
				salted_password = hash_object.hexdigest()
				if salted_password == result['password']:
					session['userId'] = result['userId']
					return redirect(url_for('courses'))
		return render_template("sign_in.html", form=form, invalid_user=True)
	return render_template("sign_in.html", form=form)


# WTForm used when a user is signing up. Makes sure all required fields are
# included, that passwords match and that the phone number is ten digits.
# Also checks to see if the email is already in use
class SignUpForm(Form):
	first_name = StringField('First Name', [validators.DataRequired()])
	last_name = StringField('Last Name', [validators.DataRequired()])
	phone_number = IntegerField('Phone Number')
	street = StringField('Street', [validators.DataRequired()])
	city = StringField('City', [validators.DataRequired()])
	postal_code = StringField('Postal Code', [validators.DataRequired()])
	country = StringField('Country', [validators.DataRequired()])
	profile_picture = FileField('Profile Picture', [validators.DataRequired()])
	email = StringField('Email', [validators.DataRequired(), Email()])
	password = PasswordField('New Password', [
		validators.DataRequired(),
		validators.EqualTo('confirm', message='Passwords must match')
	])
	confirm = PasswordField('Repeat Password')

	def validate(self):
		res = super(SignUpForm, self).validate()

		if len(str(self.phone_number.data)) != 10:
			self.phone_number.errors = ["Phone number must be ten digits"]
			res = False

		if self.email.data:
			connection = get_db_connection()
			with connection.cursor() as cursor:
				sql = ('SELECT * FROM User WHERE User.email = %s;')
				cursor.execute(sql, (self.email.data))
				if len(cursor.fetchall()):
					self.email.errors.append("Account already exists for given email")
					res = False
		return res


# Route for signing up. When posted to it validates the sign up form and
# creates a new user in the database if everything is valid
@app.route("/sign_up", methods=['GET', 'POST'])
def sign_up():
	form = SignUpForm(request.form)
	if request.method == 'POST' and form.validate():
		connection = get_db_connection()
		with connection.cursor() as cursor:
			sql = ('SELECT max(User.userId) as max from User;')
			cursor.execute(sql, ())
			new_id = int(cursor.fetchone()['max']) + 1

			salt = get_salt()
			salt_plus_password = salt + form.password.data
			hash_object = hashlib.sha256(salt_plus_password)
			salted_password = hash_object.hexdigest()

			sql = ('INSERT INTO User '
				   '(userId, email, fname, lname, role, salt, password, street, city, postal_code, country, picture) '
				   'VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);')
			cursor.execute(sql, (new_id, form.email.data, form.first_name.data, form.last_name.data, 'student', salt,
								 salted_password, form.street.data, form.city.data, form.postal_code.data,
								 form.country.data,
								 form.profile_picture.data))

			sql = ('INSERT INTO Contact '
				   '(userId, phoneNumber) '
				   'VALUES (%s, %s);')
			cursor.execute(sql, (new_id, form.phone_number.data))

			connection.commit()
			session['userId'] = new_id
			return redirect(url_for('courses'))
	return render_template("sign_up.html", form=form)


# Signs the current user out by removing their userId from the browser's session storage
@app.route("/sign_out")
def sign_out():
	session['userId'] = None
	return redirect(url_for('landing_page'))


# Route for the admin to see all users so that their can change user
# roles
@app.route("/admin")
@requires_roles('admin')
def admin():
	users = []
	connection = get_db_connection()

	with connection.cursor() as cursor:
		sql = ('SELECT * FROM User '
			   'WHERE User.active = "Y" '
			   'ORDER BY User.email DESC;')
		cursor.execute(sql, ())
		users = cursor.fetchall()

	return render_template("admin.html",
						   users=users)


@app.route("/member")
# @requires_roles('admin')
def member():
	users = []
	connection = get_db_connection()

	with connection.cursor() as cursor:
		sql = ('SELECT * FROM Member;')
		cursor.execute(sql, ())
		users = cursor.fetchall()

	return render_template("member.html",
						   users=users)



@app.route("/delete/<string:member_id>", methods=['POST'])
#@requires_roles('admin')
def delete_member(member_id):
	connection = get_db_connection()

	with connection.cursor() as cursor:

		sql = ('DELETE '
		   'FROM Member '
		   'WHERE Member.member_id = %s;')
		cursor.execute(sql, (member_id))
		connection.commit()
	return redirect(request.referrer)


@app.route("/insert", methods=['POST'])
def insert():
	connection = get_db_connection()

	print('Insert')
	print(request.form)

	f = request.form['firstName']
	l = request.form['lastName']
	m = request.form['marital_status']
	w = request.form['whether_dependent']
	p = request.form['home_phone_number']
	g = request.form['group_id']
	plan = request.form['plan_id']
	contact = request.form['contact_id']
	member_id = request.form['member_id']

	with connection.cursor() as cursor:
		sql = ('INSERT INTO Member '
			   '(`firstName`, `lastName`, `marital_status`, `whether_dependent`, `home_phone_number`, `group_id`, `plan_id`, `contact_id`, `member_id`) '
			   'VALUES (%s, %s,%s, %s, %s, %s, %s, %s, %s);')
		cursor.execute(sql, (f, l, m, w, p, g, plan, contact, member_id))

		print('Inserted successfully')

		connection.commit()
		session['userId'] = member_id
	return redirect(url_for('member'))


@app.route("/update/<string:member_id>", methods=['POST'])
#@requires_roles('admin')
def update_member(member_id):
	connection = get_db_connection()
	newRole = 'None'
	result = {}
	if not member_id:
		member_id=request.form['member_id']

	with connection.cursor() as cursor:

		if member_id:

			sql = ('SELECT * '
				   'FROM Member '
				   'WHERE Member.member_id =  %s;')
			cursor.execute(sql, (member_id))
			result = cursor.fetchall()


			print('Deleting')
			print(member_id)
			sql = ('DELETE FROM Member '
				   'WHERE member_id = %s;')
			cursor.execute(sql, (member_id))

			print('Insert')
			print(request.form)

			f=request.form['firstName']
			l=request.form['lastName']
			m=request.form['marital_status']
			w=request.form['whether_dependent']
			p=request.form['home_phone_number']
			g=request.form['group_id']
			plan=request.form['plan_id']
			contact=request.form['contact_id']

			if f == '':
				f=result[0]['firstName']
			if l == '':
				l=result[0]['lastName']
			if m == '':
				m=result[0]['marital_status']
			if w == '':
				w=result[0]['whether_dependent']

			if p == '':
				p=result[0]['home_phone_number']
			if g == '':
				g=result[0]['group_id']
			if plan == '':
				plan=result[0]['plan_id']
			if contact == '':
				contact=result[0]['contact_id']


			sql = ('INSERT INTO Member '
				   '(`firstName`, `lastName`, `marital_status`, `whether_dependent`, `home_phone_number`, `group_id`, `plan_id`, `contact_id`, `member_id`) '
				   'VALUES (%s, %s,%s, %s, %s, %s, %s, %s, %s);')
			cursor.execute(sql, (f, l, m, w, p, g, plan, contact, member_id))

			print('Inserted successfully')

			connection.commit()
			session['userId'] = member_id

		return redirect(url_for('member'))


# Changes the given user's user role to the newrole that
# was posted on the form
@app.route("/change_role/<string:user_id>", methods=['POST'])
@requires_roles('admin')
def change_role(user_id):
	connection = get_db_connection()
	newRole = 'None'
	result = {}

	with connection.cursor() as cursor:
		sql = ('SELECT * '
			   'FROM User '
			   'WHERE User.userId =  %s;')
		cursor.execute(sql, (user_id))
		result = cursor.fetchall()

		if request.form['make1'] == 'faculty' and result[0]['role'] == 'admin':
			newRole = 'admin'
		else:
			newRole = request.form['make1']

		sql = ('UPDATE User '
			   'SET role = %s '
			   'WHERE userId = %s;')
		cursor.execute(sql, (newRole, user_id))

		if request.form['make1'] == 'admin':
			sql = ('DELETE FROM Administrator '
				   'WHERE adminId = %s;')
			cursor.execute(sql, (user_id))
			sql = ('INSERT INTO Administrator (adminId, role, adminGrantedBy) '
				   'VALUES (%s, %s , %s);')
			cursor.execute(sql, (user_id, request.form['make1'], g.user['userId']))
		elif request.form['make1'] == 'faculty':
			sql = ('DELETE FROM Faculty '
				   'WHERE facultyId = %s;')
			cursor.execute(sql, (user_id))
			sql = ('INSERT INTO Faculty (facultyId, facultyApprovedBy) '
				   'VALUES (%s , %s);')
			cursor.execute(sql, (user_id, g.user['userId']))
		else:
			sql = ('DELETE FROM Administrator '
				   'WHERE adminId = %s;')
			cursor.execute(sql, (user_id))
			sql = ('DELETE FROM Faculty '
				   'WHERE facultyId = %s;')
			cursor.execute(sql, (user_id))
		connection.commit()
	return redirect(request.referrer)


# Deletes the user with the given user id by setting their 'active' flag
# to false.
@app.route("/admin/<string:user_id>/<string:user_role>", methods=['POST'])
@requires_roles('admin')
def delete_user(user_id, user_role):
	connection = get_db_connection()

	with connection.cursor() as cursor:
		sql = ('SELECT * '
			   'FROM User '
			   'WHERE User.userId =  %s '
			   'AND User.role = %s;')
		cursor.execute(sql, (user_id, user_role))
		result = cursor.fetchall()

		if result:
			sql = ('UPDATE User '
				   'set User.active = "N"'
				   'WHERE User.userId =  %s '
				   'AND User.role = %s;')
			cursor.execute(sql, (user_id, user_role))
		connection.commit()
	return redirect(request.referrer)


# Gets a list of all of a student's courses, organized into three categories:
# enrolled, completed or interested. Sorts the results by rating
@app.route("/courses")
@requires_roles('student')
def courses():
	current_courses = []
	completed_courses = []
	interested_courses = []
	secondary_topics = {}
	connection = get_db_connection()
	with connection.cursor() as cursor:
		sql = ('SELECT * FROM Course '
			   'JOIN CourseCompleted ON CourseCompleted.courseId = Course.id '
			   'JOIN User ON CourseCompleted.userId = User.userId '
			   'WHERE User.userId = %s '
			   'ORDER BY CourseCompleted.rating DESC;')
		cursor.execute(sql, (g.user['userId']))
		completed_courses = cursor.fetchall()

		sql = ('SELECT Course.id, Course.name, Course.description, Course.primaryTopic, '
			   'COUNT(CourseMaterial.materialName) as materialsLeft, AVG(CourseCompleted.rating) as avgRating '
			   'FROM Course '
			   'LEFT JOIN CourseMaterial on CourseMaterial.courseId = Course.id '
			   'INNER JOIN EnrolledCourse on EnrolledCourse.courseId = Course.id '
			   'INNER JOIN User on User.userId = EnrolledCourse.userId '
			   'LEFT JOIN MaterialComplete on MaterialComplete.materialId = CourseMaterial.materialId AND MaterialComplete.userId = User.userId '
			   'LEFT JOIN CourseCompleted ON CourseCompleted.courseId = Course.id '
			   'WHERE User.userId = %s AND MaterialComplete.date is NULL '
			   'GROUP BY Course.id '
			   'ORDER BY avgRating DESC;')
		cursor.execute(sql, (g.user['userId']))
		current_courses = cursor.fetchall()

		sql = (
		'SELECT Course.id, Course.name, Course.description, Course.primaryTopic, AVG(CourseCompleted.rating) as avgRating '
		'FROM Course '
		'INNER JOIN InterestedCourse on InterestedCourse.courseId = Course.id '
		'INNER JOIN User on User.userId = InterestedCourse.userId '
		'LEFT JOIN EnrolledCourse on EnrolledCourse.courseId = Course.id AND EnrolledCourse.userId = User.userId '
		'LEFT JOIN CourseCompleted ON CourseCompleted.courseId = Course.id '
		'WHERE User.userId = %s AND EnrolledCourse.userId is NULL '
		'GROUP BY Course.id '
		'ORDER BY avgRating DESC;')
		cursor.execute(sql, (g.user['userId']))
		interested_courses = cursor.fetchall()

		sql = ('SELECT * FROM SecondaryCourse;')
		cursor.execute(sql, ())
		secondary_courses = cursor.fetchall()
		for secondary_course in secondary_courses:
			if secondary_course['courseId'] in secondary_topics:
				secondary_topics[secondary_course['courseId']].append(secondary_course['secondaryTopic'])
			else:
				secondary_topics[secondary_course['courseId']] = [secondary_course['secondaryTopic']]

	return render_template("courses.html",
						   current_courses=current_courses,
						   completed_courses=completed_courses,
						   interested_courses=interested_courses,
						   secondary_topics=secondary_topics)


# Gets and displays all course info (description, topics, materials) etc
# for the course with the given id
@app.route("/course/<string:course_id>/")
@requires_roles('student')
def course_info(course_id):
	course_materials = []
	course_info = None
	completed_ids = []
	secondary_topics = []
	enrolled_info = None
	next_material_to_complete = None
	completion_info = None
	connection = get_db_connection()
	with connection.cursor() as cursor:
		sql = ('SELECT * FROM Course WHERE Course.id = %s;')
		cursor.execute(sql, (course_id,))
		course_info = cursor.fetchone()

		sql = (
		'SELECT * FROM CourseMaterial WHERE CourseMaterial.courseId = %s ORDER BY CourseMaterial.materialOrder ASC;')
		cursor.execute(sql, (course_id,))
		course_materials = cursor.fetchall()

		sql = ('SELECT * FROM MaterialComplete '
			   'INNER JOIN CourseMaterial on CourseMaterial.materialId = MaterialComplete.materialId '
			   'WHERE CourseMaterial.courseId = %s and MaterialComplete.userId =  %s;')
		cursor.execute(sql, (course_id, g.user['userId']))
		results = cursor.fetchall()
		completed_ids = {completion['materialId']: completion for completion in results}
		next_material_to_complete = max([result['materialOrder'] for result in results]) + 1 if len(results) else 1

		sql = ('SELECT * FROM SecondaryCourse WHERE SecondaryCourse.courseId = %s;')
		cursor.execute(sql, (course_id))
		secondary_topics = [secondary['secondaryTopic'] for secondary in cursor.fetchall()]

		sql = ('SELECT * FROM EnrolledCourse '
			   'WHERE EnrolledCourse.courseId = %s AND EnrolledCourse.userId = %s;')
		cursor.execute(sql, (course_id, g.user['userId']))
		results = cursor.fetchall()
		enrolled_info = results[0] if len(results) else None

		sql = ('SELECT * FROM CourseCompleted '
			   'WHERE CourseCompleted.courseId = %s AND CourseCompleted.userId = %s;')
		cursor.execute(sql, (course_id, g.user['userId']))
		results = cursor.fetchall()
		completion_info = results[0] if len(results) else None

	return render_template("course_info.html",
						   course_info=course_info,
						   course_materials=course_materials,
						   completed_ids=completed_ids,
						   secondary_topics=secondary_topics,
						   next_material_to_complete=next_material_to_complete,
						   completion_info=completion_info,
						   enrolled_info=enrolled_info)


# Helper function to get a list of all courses that the current user is interested in
# and a lst of all of the secondary topics for courses
def get_interested_courses_and_secondary_topics():
	interested_courses = []
	secondary_topics = {}
	connection = get_db_connection()
	with connection.cursor() as cursor:
		sql = ('SELECT InterestedCourse.courseId '
			   'FROM InterestedCourse '
			   'WHERE InterestedCourse.userId =  %s;')
		cursor.execute(sql, (g.user['userId']))
		interested_courses = [course['courseId'] for course in cursor.fetchall()]

		sql = ('SELECT * FROM SecondaryCourse;')
		cursor.execute(sql, ())
		secondary_courses = cursor.fetchall()
		for secondary_course in secondary_courses:
			if secondary_course['courseId'] in secondary_topics:
				secondary_topics[secondary_course['courseId']].append(secondary_course['secondaryTopic'])
			else:
				secondary_topics[secondary_course['courseId']] = [secondary_course['secondaryTopic']]

	return (interested_courses, secondary_topics)


# Route that a student can use to browse all courses. Displays basic course info for each course
# and sorts the list by average rating
@app.route("/browse/")
@requires_roles('student')
def browse_courses():
	courses = []
	interested_courses = []
	secondary_topics = {}
	connection = get_db_connection()
	with connection.cursor() as cursor:
		sql = (
		'SELECT Course.id, Course.name, Course.description, Course.primaryTopic, AVG(CourseCompleted.rating) as avgRating '
		'FROM Course '
		'LEFT JOIN CourseCompleted ON CourseCompleted.courseId = Course.id '
		'GROUP BY Course.id '
		'ORDER BY avgRating DESC;')
		cursor.execute(sql, ())
		courses = cursor.fetchall()

	(interested_courses, secondary_topics) = get_interested_courses_and_secondary_topics()

	return render_template("find_courses.html",
						   courses=courses,
						   interested_courses=interested_courses,
						   secondary_topics=secondary_topics)


# Form for selecting which topic the user wants to browse courses for
class BrowseByTopicForm(Form):
	topic = SelectField('Topic')


# Route which allows a student to browse all courses for a selected topic
@app.route("/browse/topic/")
@requires_roles('student')
def browse_courses_by_topic():
	topic = request.args.get('topic')

	form = BrowseByTopicForm(topic=topic)
	courses = []
	interested_courses = []
	secondary_topics = {}
	connection = get_db_connection()

	with connection.cursor() as cursor:
		if topic:
			sql = (
			'SELECT Course.id, Course.name, Course.description, Course.primaryTopic, AVG(CourseCompleted.rating) as avgRating '
			'FROM CourseCompleted '
			'RIGHT JOIN Course on Course.id = CourseCompleted.courseId '
			'WHERE Course.id in ( '
			'SELECT DISTINCT Course.id '
			'FROM Course '
			'LEFT JOIN SecondaryCourse on SecondaryCourse.courseId = Course.id '
			'WHERE Course.primaryTopic = %s OR SecondaryCourse.SecondaryTopic = %s '
			') '
			'GROUP BY Course.id '
			'ORDER BY avgRating DESC;')
			cursor.execute(sql, (topic, topic))
			courses = cursor.fetchall()
		else:
			sql = (
			'SELECT Course.id, Course.name, Course.description, Course.primaryTopic, AVG(CourseCompleted.rating) as avgRating '
			'FROM Course '
			'LEFT JOIN CourseCompleted ON CourseCompleted.courseId = Course.id '
			'GROUP BY Course.id '
			'ORDER BY avgRating DESC;')
			cursor.execute(sql, ())
			courses = cursor.fetchall()

		sql = (
		'SELECT DISTINCT primaryTopic FROM Course UNION SELECT DISTINCT secondaryTopic as primaryTopic FROM SecondaryCourse;')
		cursor.execute(sql, ())
		all_topics = [topic['primaryTopic'] for topic in cursor.fetchall()]
		form.topic.choices = [(topic, topic) for topic in all_topics]

	(interested_courses, secondary_topics) = get_interested_courses_and_secondary_topics()

	return render_template("find_courses.html",
						   search_type="topic",
						   topic=topic,
						   topic_form=form,
						   courses=courses,
						   interested_courses=interested_courses,
						   secondary_topics=secondary_topics)


# Form used for searching courses by keyword
class BrowseByKeywordForm(Form):
	keyword = StringField('Search')
	submit = SubmitField('Search')


# Route which allows students to search course titles and descriptions
# for a certain keyword
@app.route("/browse/keyword/")
@requires_roles('student')
def browse_courses_by_keyword():
	keyword = request.args.get('keyword')

	form = BrowseByKeywordForm(keyword=keyword)
	courses = []
	interested_courses = []
	secondary_topics = {}
	connection = get_db_connection()
	with connection.cursor() as cursor:
		if keyword:
			sql = (
			'SELECT Course.id, Course.name, Course.description, Course.primaryTopic, AVG(CourseCompleted.rating) as avgRating '
			'FROM Course '
			'LEFT JOIN CourseCompleted ON CourseCompleted.courseId = Course.id '
			'WHERE Course.description LIKE %s OR Course.name LIKE %s '
			'GROUP BY Course.id '
			'ORDER BY avgRating DESC;')
			cursor.execute(sql, ('%' + keyword + '%', '%' + keyword + '%'))
			courses = cursor.fetchall()
		else:
			sql = (
			'SELECT Course.id, Course.name, Course.description, Course.primaryTopic, AVG(CourseCompleted.rating) as avgRating '
			'FROM Course '
			'LEFT JOIN CourseCompleted ON CourseCompleted.courseId = Course.id '
			'GROUP BY Course.id '
			'ORDER BY avgRating DESC;')
			cursor.execute(sql, ())
			courses = cursor.fetchall()

	(interested_courses, secondary_topics) = get_interested_courses_and_secondary_topics()

	return render_template("find_courses.html",
						   search_type="keyword",
						   keyword=keyword,
						   keyword_form=form,
						   courses=courses,
						   interested_courses=interested_courses,
						   secondary_topics=secondary_topics)


# Route which displays quiz course material
@app.route("/<string:course_id>/quiz/<string:material_id>/")
@requires_roles('student')
def quiz_info(course_id, material_id):
	connection = get_db_connection()
	questions = []
	with connection.cursor() as cursor:
		sql = ('SELECT * FROM QuizQuestion WHERE materialId = %s;')
		cursor.execute(sql, (material_id))
		questions = cursor.fetchall()
	return render_template("quiz.html",
						   questions=questions,
						   course_id=course_id)


# Route which displays a student's certificate of completion
@app.route("/certification/<string:course_id>")
@requires_roles('student')
def genCert(course_id):
	connection = get_db_connection()
	user = []
	with connection.cursor() as cursor:
		sql = ('SELECT * FROM User WHERE userId = %s;')
		cursor.execute(sql, (g.user['userId']))
		user = cursor.fetchone()
		sql = ('SELECT cc.date FROM CourseCompleted cc WHERE cc.courseId = %s and cc.userId = %s;')
		cursor.execute(sql, (course_id, g.user['userId']))
		result = cursor.fetchone()
		if not result:
			return redirect(request.referrer)

		date = result['date'].strftime("%B %d, %Y")
	return render_template("certification.html",
						   user=user,
						   course_id=course_id,
						   date=date)


# Route which allows students to browse courses by completion percentage
@app.route("/browse/comp_percent/")
@requires_roles('student')
def browse_courses_by_completion_percent():
	courses = []
	connection = get_db_connection()
	with connection.cursor() as cursor:
		sql = ('SELECT Course.id, Course.name, Course.description, Course.primaryTopic, '
			   'ROUND(COUNT(CourseCompleted.courseId) / COUNT(EnrolledCourse.courseId) * 100, 2) as compPercent, '
			   'COUNT(EnrolledCourse.userId) as numEnrolled '
			   'FROM Course '
			   'LEFT JOIN EnrolledCourse on EnrolledCourse.courseId = Course.id '
			   'LEFT JOIN User on User.userId = EnrolledCourse.userId '
			   'LEFT JOIN CourseCompleted on CourseCompleted.courseId = Course.id and User.userId = CourseCompleted.userId '
			   'GROUP BY Course.id '
			   'ORDER BY compPercent DESC, COUNT(CourseCompleted.courseId);')
		cursor.execute(sql, ())
		courses = cursor.fetchall()

	(interested_courses, secondary_topics) = get_interested_courses_and_secondary_topics()

	return render_template("find_courses.html",
						   search_type="percent",
						   courses=courses,
						   interested_courses=interested_courses,
						   secondary_topics=secondary_topics)


# Route which gets a student's history, including which courses they have
# completed, the confirmation codes and the amount of money that they have spent
@app.route("/history/")
@requires_roles('student')
def browse_history():
	courses = []
	phone_numbers = ""
	connection = get_db_connection()
	with connection.cursor() as cursor:
		sql = (
		'SELECT DISTINCT c.id AS id, enroll.userId, c.name, enroll.date AS eDate, comp.date AS cDate, c.cost, enroll.code '
		'FROM (EnrolledCourse enroll LEFT JOIN CourseCompleted comp ON enroll.userId = comp.userId  and enroll.courseId = comp.courseId) '
		'INNER JOIN Course c ON enroll.courseId = c.id '
		'WHERE enroll.userId = %s;')
		cursor.execute(sql, (g.user['userId']))
		courses = cursor.fetchall()

		sql = ('SELECT phoneNumber FROM Contact WHERE Contact.userId = %s;')
		cursor.execute(sql, (g.user['userId']))
		phone_numbers = ", ".join([str(contact["phoneNumber"]) for contact in cursor.fetchall()])

	return render_template("user_account_history.html",
						   courses=courses,
						   phone_numbers=phone_numbers)


# Allows a student to mark a course as 'interested'
@app.route("/interest/<string:course_id>/", methods=['POST'])
@requires_roles('student')
def toggle_interest(course_id):
	connection = get_db_connection()
	with connection.cursor() as cursor:
		sql = ('SELECT * '
			   'FROM InterestedCourse '
			   'WHERE InterestedCourse.userId =  %s and InterestedCourse.courseId = %s;')
		cursor.execute(sql, (g.user['userId'], course_id))
		if len(cursor.fetchall()):
			sql = ('DELETE FROM InterestedCourse '
				   'WHERE InterestedCourse.userId =  %s and InterestedCourse.courseId = %s;')
			cursor.execute(sql, (g.user['userId'], course_id))
		else:
			sql = ('INSERT INTO InterestedCourse (courseId, userId) '
				   'VALUES (%s, %s);')
			cursor.execute(sql, (course_id, g.user['userId']))
		connection.commit()

	return redirect(request.referrer)


# Allows a student to enroll in the given course
@app.route("/enroll/<string:course_id>/", methods=['POST'])
@requires_roles('student')
def course_enroll(course_id):
	connection = get_db_connection()
	with connection.cursor() as cursor:
		date = datetime.date.today()
		time = datetime.datetime.now().time()
		sql = ('INSERT INTO EnrolledCourse (courseId, userId, date, time, code) '
			   'VALUES (%s, %s, %s, %s, %s);')
		cursor.execute(sql, (course_id, g.user['userId'], date, time, 'conf' + course_id + g.user['userId']))
		connection.commit()

	return redirect(url_for('course_info', course_id=course_id))


# Allows a student to mark the given course material as complete
@app.route("/complete_material/<string:course_id>/<string:material_id>/", methods=['POST'])
@requires_roles('student')
def complete_material(course_id, material_id):
	connection = get_db_connection()
	with connection.cursor() as cursor:
		date = datetime.date.today()
		sql = ('INSERT INTO MaterialComplete (materialId, userId, date) '
			   'VALUES (%s, %s, %s);')
		cursor.execute(sql, (material_id, g.user['userId'], date))

		sql = ('SELECT CourseMaterial.materialId '
			   'FROM CourseMaterial '
			   'WHERE CourseMaterial.courseId =  %s')
		cursor.execute(sql, (course_id))
		total_materials = len(cursor.fetchall())

		sql = ('SELECT MaterialComplete.materialId '
			   'FROM MaterialComplete '
			   'INNER JOIN CourseMaterial ON CourseMaterial.materialId = MaterialComplete.materialId '
			   'WHERE CourseMaterial.courseId =  %s and MaterialComplete.userId = %s')
		cursor.execute(sql, (course_id, g.user['userId']))
		completed_materials = len(cursor.fetchall())

		if completed_materials == total_materials:
			time = datetime.datetime.now().time()
			sql = ('INSERT INTO CourseCompleted (courseId, userId, date, time) '
				   'VALUES (%s, %s, %s, %s);')
			cursor.execute(sql, (course_id, g.user['userId'], date, time))
		connection.commit()

	return redirect(url_for('course_info', course_id=course_id))


# Allows a student to rate a course once they have completed it
@app.route("/rate/<string:course_id>/", methods=['POST'])
@requires_roles('student')
def rate_course(course_id):
	connection = get_db_connection()
	with connection.cursor() as cursor:
		sql = ('UPDATE CourseCompleted '
			   'SET rating = %s '
			   'WHERE CourseCompleted.courseId = %s AND CourseCompleted.userId = %s')
		cursor.execute(sql, (request.form['rating'], course_id, g.user['userId']))
		connection.commit()

	return redirect(url_for('course_info', course_id=course_id))


# Form which students can use to ask qustions about a course
class AskQuestionForm(Form):
	question = TextAreaField('Question', [validators.DataRequired()])
	materials = SelectMultipleField('Course Materials')
	submit = SubmitField('Ask Question')


# Route which allows students to ask questions about a course,
# pretaining to one or more course materials
@app.route("/ask_question/<string:course_id>/", methods=["GET", "POST"])
@requires_roles('student')
def ask_question(course_id):
	form = AskQuestionForm(request.form)
	all_materials = []

	connection = get_db_connection()
	with connection.cursor() as cursor:
		sql = ('SELECT * FROM Course '
			   'LEFT JOIN CourseMaterial ON CourseMaterial.courseId = Course.id '
			   'WHERE Course.id = %s;')
		cursor.execute(sql, (course_id))
		all_materials = cursor.fetchall()

		if all_materials and all_materials[0]['materialId']:
			form.materials.choices = [(material['materialId'], material['materialName']) for material in all_materials]

		if request.method == 'POST' and form.validate():
			sql = ('INSERT INTO CourseQuestion (text, userId, courseId) VALUES  '
				   ' (%s, %s, %s);')
			cursor.execute(sql, (form.question.data, g.user['userId'], course_id))
			sql = ('SELECT LAST_INSERT_ID();')
			cursor.execute(sql, ())
			question_id = cursor.fetchone()['LAST_INSERT_ID()']
			for material_id in form.materials.data:
				sql = ('INSERT INTO QuestionMaterial (questionId, materialId) VALUES (%s, %s);')
				cursor.execute(sql, (question_id, material_id))

			connection.commit()

			return redirect(url_for('course_questions', course_id=course_id))
	return render_template('ask_question.html', all_materials=all_materials, form=form)


# Form that faculty can use to respond to course questions
class AnswerQuestionForm(Form):
	answer = TextAreaField('Answer', [validators.DataRequired()])
	submit = SubmitField('Answer Question')


# Route which displays all visible questions have have been asked for
# the specified course
@app.route("/questions/<string:course_id>/", methods=["GET"])
@requires_roles('student')
def course_questions(course_id):
	all_questions = []
	course_info = None
	related_course_materials = {}
	liked_question_ids = []
	answer_question_form = AnswerQuestionForm()

	connection = get_db_connection()
	with connection.cursor() as cursor:
		sql = ('SELECT * FROM CourseQuestion WHERE CourseQuestion.courseId = %s;')
		cursor.execute(sql, (course_id))
		all_questions = cursor.fetchall()

		sql = ('SELECT * FROM Course WHERE Course.id = %s;')
		cursor.execute(sql, (course_id))
		course_info = cursor.fetchone()

		sql = ('SELECT questionId FROM QuestionLike WHERE QuestionLike.userId = %s;')
		cursor.execute(sql, (g.user['userId']))
		liked_question_ids = [question['questionId'] for question in cursor.fetchall()]

		sql = ('SELECT * FROM QuestionMaterial '
			   'INNER JOIN CourseQuestion on CourseQuestion.questionId = QuestionMaterial.questionId '
			   'INNER JOIN CourseMaterial on CourseMaterial.materialId = QuestionMAterial.materialId '
			   'WHERE CourseQuestion.courseId = %s;')
		cursor.execute(sql, (course_id))
		question_materials = cursor.fetchall()
		for material in question_materials:
			if material['questionId'] in related_course_materials:
				related_course_materials[material['questionId']] += ', ' + material['materialName']
			else:
				related_course_materials[material['questionId']] = material['materialName']

	return render_template('course_questions.html',
						   all_questions=all_questions,
						   course_info=course_info,
						   related_course_materials=related_course_materials,
						   answer_question_form=answer_question_form,
						   liked_question_ids=liked_question_ids)


# Route which allows faculty to answer a question asked by a student for
# the specified course
@app.route("/answer_question/<string:course_id>/<string:question_id>/", methods=["POST"])
@requires_roles('faculty')
def answer_questions(course_id, question_id):
	answer_question_form = AnswerQuestionForm(request.form)

	if request.method == 'POST' and answer_question_form.validate():
		connection = get_db_connection()
		with connection.cursor() as cursor:
			sql = ('UPDATE CourseQuestion SET CourseQuestion.answer = %s WHERE CourseQuestion.questionId = %s;')
			cursor.execute(sql, (answer_question_form.answer.data, question_id))
			connection.commit()

	return redirect(url_for('course_questions', course_id=course_id))


# Route which allows a user to like a question
@app.route("/like_question/<string:course_id>/<string:question_id>/", methods=["POST"])
@requires_roles('student')
def like_question(course_id, question_id):
	connection = get_db_connection()
	with connection.cursor() as cursor:
		sql = ('INSERT INTO QuestionLike (userId, questionId) VALUES (%s, %s);')
		cursor.execute(sql, (g.user['userId'], question_id))
		connection.commit()

	return redirect(url_for('course_questions', course_id=course_id))


# Route which allows a user to unlike a question
@app.route("/unlike_question/<string:course_id>/<string:question_id>/", methods=["POST"])
@requires_roles('student')
def unlike_question(course_id, question_id):
	connection = get_db_connection()
	with connection.cursor() as cursor:
		sql = ('DELETE FROM QuestionLike WHERE userId = %s AND questionId = %s;')
		cursor.execute(sql, (g.user['userId'], question_id))
		connection.commit()

	return redirect(url_for('course_questions', course_id=course_id))


# Route which allows faculty members to make a course question visible to all students
@app.route("/make_visible/<string:course_id>/<string:question_id>/", methods=["POST"])
@requires_roles('faculty')
def make_question_visible(course_id, question_id):
	connection = get_db_connection()
	with connection.cursor() as cursor:
		sql = ('UPDATE CourseQuestion SET visible = "y" WHERE questionId = %s;')
		cursor.execute(sql, (question_id))
		connection.commit()

	return redirect(url_for('course_questions', course_id=course_id))


# Route which lets faculty members see any courses that have unanswered questions.
# Also shows all courses which they have created
@app.route("/faculty/")
@requires_roles('faculty')
def faculty():
	courses_needing_attention = []
	courses = []
	connection = get_db_connection()
	with connection.cursor() as cursor:
		sql = (
		'SELECT Course.name, Course.id, COUNT(CourseQuestion.questionId) as questionCount, MIN(CourseQuestion.questionId) as questId '
		'FROM CourseQuestion '
		'INNER JOIN Course ON Course.id = CourseQuestion.courseId '
		'INNER JOIN CourseCreator ON CourseCreator.courseId = Course.id '
		'WHERE CourseCreator.userId = %s and CourseQuestion.answer is NULL '
		'GROUP BY Course.id '
		'ORDER BY questionCount DESC, questId ASC;')
		cursor.execute(sql, (g.user['userId']))
		courses_needing_attention = cursor.fetchall()

		sql = (
		'SELECT Course.name, Course.id, COUNT(EnrolledCourse.userId) as enrolledCount, COUNT(CourseCompleted.userId) as completedCount '
		' FROM Course '
		'INNER JOIN CourseCreator ON CourseCreator.courseId = Course.id '
		'LEFT JOIN EnrolledCourse on EnrolledCourse.courseId = Course.id '
		'LEFT JOIN CourseCompleted on CourseCompleted.courseId = Course.id AND CourseCompleted.userId = EnrolledCourse.userId '
		'WHERE CourseCreator.userId = %s '
		'GROUP BY Course.id;')
		cursor.execute(sql, (g.user['userId']))
		courses = cursor.fetchall()

	return render_template('faculty.html',
						   courses_needing_attention=courses_needing_attention,
						   courses=courses)


# Route which shows admin users the earnings report for faculty members
@app.route("/admin/report/")
@requires_roles('admin')
def earnings_report():
	earnings = []
	connection = get_db_connection()
	with connection.cursor() as cursor:
		sql = ('SELECT User.email as courseCreator, SUM(tmp.courseCost) as courseEarnings '
			   'FROM (SELECT Course.id as courseId, Course.name, COUNT(EnrolledCourse.courseId) * Course.cost as courseCost '
			   'FROM Course  '
			   'INNER JOIN EnrolledCourse on Course.id = EnrolledCourse.courseId '
			   'GROUP BY Course.id) tmp '
			   'INNER JOIN CourseCreator on CourseCreator.courseId = tmp.courseId '
			   'INNER JOIN User on User.userId = CourseCreator.userId '
			   'GROUP BY CourseCreator.userId '
			   'ORDER BY SUM(tmp.courseCost) DESC;')
		cursor.execute(sql, ())
		earnings = cursor.fetchall()

	return render_template('admin_report.html', earnings=earnings)


@app.errorhandler(404)
def page_not_found(e):
	return render_template('404.html'), 404


## Start app when this file is run
if __name__ == '__main__':
	app.run()