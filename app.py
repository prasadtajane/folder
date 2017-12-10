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


def get_db_connection():
    return pymysql.connect(host='localhost',
                           user='root',
                           password='',
                           db='Trainly',
                           charset='utf8',
                           cursorclass=pymysql.cursors.DictCursor)


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


def get_salt():
    return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(4))


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
                   'WHERE userId = %s;')
            cursor.execute(sql, (session['userId']))
            result = cursor.fetchone()
            if result:
                g.user = result
                g.user_roles.add('student')
                if result['adminGrantedBy']:
                    g.user_roles.add('admin')
                if result['facultyApprovedBy']:
                    g.user_roles.add('faculty')


@app.route("/")
def landing_page():
    g.user_role = 'faculty'
    can_sign_in = getattr(g, 'user_id', None) == None
    return render_template("base.html", can_sign_in=can_sign_in)


class SignInForm(Form):
    email = StringField('Email Address', [validators.DataRequired()])
    password = PasswordField('New Password', [validators.DataRequired()])


@app.route("/sign_in", methods=['GET', 'POST'])
@requires_roles(None)
def sign_in():
    form = SignInForm(request.form)
    if request.method == 'POST' and form.validate():
        email = form.email.data
        password = form.password.data
        connection = get_db_connection()
        with connection.cursor() as cursor:
            sql = 'SELECT * FROM User WHERE email = %s;'
            cursor.execute(sql, (email))
            result = cursor.fetchone()

            if result:
                salt_plus_password = result['salt'] + password
                hash_object = hashlib.sha256(salt_plus_password)
                salted_password = hash_object.hexdigest()
                if salted_password == result['password']:
                    session['userId'] = result['userId']
                    return redirect(url_for('courses'))
        return render_template("sign_in.html", form=form, invalid_user=True)
    return render_template("sign_in.html", form=form)


@app.route("/admin")
@requires_roles('admin')
def admin():
    users=[]
    # distinctRoles = ['admin', 'facutly', 'student']
    # users={result=[], distinctRoles=[]}
    connection = get_db_connection()

    with connection.cursor() as cursor:
        sql = ('SELECT * FROM User '
               'ORDER BY User.email DESC;')
        cursor.execute(sql, ())
        users = cursor.fetchall()


    return render_template("admin.html",
                           users=users)



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
            connection.commit()
            session['userId'] = new_id
            return redirect(url_for('courses'))
    return render_template("sign_up.html", form=form)


@app.route("/sign_out")
def sign_out():
    session['userId'] = None
    return redirect(url_for('landing_page'))


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


class BrowseByTopicForm(Form):
    topic = SelectField('Topic')


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


class BrowseByKeywordForm(Form):
    keyword = StringField('Search')
    submit = SubmitField('Search')


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


@app.route("/browse/comp_percent/")
@requires_roles('student')
def browse_courses_by_completion_percent():
    courses = []
    interested_courses = []
    secondary_topics = {}
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


@app.route("/history/")
@requires_roles('student')
def browse_history():
    courses = []
    interested_courses = []
    secondary_topics = {}
    connection = get_db_connection()
    with connection.cursor() as cursor:
        sql = (
        'SELECT DISTINCT c.id AS id, enroll.userId, c.name, enroll.date AS eDate, comp.date AS cDate, c.cost, enroll.code '
        'FROM (EnrolledCourse enroll LEFT JOIN CourseCompleted comp ON enroll.userId = comp.userId  and enroll.courseId = comp.courseId) '
        'INNER JOIN Course c ON enroll.courseId = c.id '
        'WHERE enroll.userId = %s;')
        cursor.execute(sql, (g.user['userId']))
        courses = cursor.fetchall()

    return render_template("user_account_history.html",
                           courses=courses,
                           interested_courses=interested_courses,
                           secondary_topics=secondary_topics)


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


class AskQuestionForm(Form):
    question = TextAreaField('Question', [validators.DataRequired()])
    materials = SelectMultipleField('Course Materials')
    submit = SubmitField('Ask Question')


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


class AnswerQuestionForm(Form):
    answer = TextAreaField('Answer', [validators.DataRequired()])
    submit = SubmitField('Answer Question')


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


@app.route("/like_question/<string:course_id>/<string:question_id>/", methods=["POST"])
@requires_roles('student')
def like_question(course_id, question_id):
    connection = get_db_connection()
    with connection.cursor() as cursor:
        sql = ('INSERT INTO QuestionLike (userId, questionId) VALUES (%s, %s);')
        cursor.execute(sql, (g.user['userId'], question_id))
        connection.commit()

    return redirect(url_for('course_questions', course_id=course_id))


@app.route("/unlike_question/<string:course_id>/<string:question_id>/", methods=["POST"])
@requires_roles('student')
def unlike_question(course_id, question_id):
    connection = get_db_connection()
    with connection.cursor() as cursor:
        sql = ('DELETE FROM QuestionLike WHERE userId = %s AND questionId = %s;')
        cursor.execute(sql, (g.user['userId'], question_id))
        connection.commit()

    return redirect(url_for('course_questions', course_id=course_id))


@app.route("/make_visible/<string:course_id>/<string:question_id>/", methods=["POST"])
@requires_roles('faculty')
def make_question_visible(course_id, question_id):
    connection = get_db_connection()
    with connection.cursor() as cursor:
        sql = ('UPDATE CourseQuestion SET visible = "t" WHERE questionId = %s;')
        cursor.execute(sql, (question_id))
        connection.commit()

    return redirect(url_for('course_questions', course_id=course_id))


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


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


## Start app when this file is run
if __name__ == '__main__':
    app.run()