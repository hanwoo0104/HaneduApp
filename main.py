from flask import Flask, render_template, request, jsonify
import authutil, usermanager
from urllib.parse import unquote
import json, os

app = Flask('app')


@app.route('/')
def home():
  return render_template('index.html')


@app.route('/notice', methods=['GET'])
def notice():
  try:
    teacher_list = []
    teachers = open('teachers.txt', 'r', encoding="utf-8")
    lines = teachers.readlines()
    for line in lines:
      line = line.strip()
      teacher_list.append(line)
    try:
      name = unquote(request.cookies.get('name'))
    except:
      return render_template('notice.html')
    if name not in teacher_list:
      with open('posts.json', 'r') as f:
        posts = json.load(f)
      joinedclass = authutil.getinfo("class", name)
      joined_list = joinedclass.split('/')
      print(joinedclass)

      # "class" 키의 값이 joined_list에 있는 경우만 유지
      filtered_posts = [
          post for post in posts if post.get('class') in joined_list
      ]

      return render_template('notice.html', postings=filtered_posts)
    else:
      with open('posts.json', 'r') as f:
        posts = json.load(f)
      joinedclass = authutil.getinfo("class", name)
      joined_list = joinedclass.split('/')
      print(joinedclass)

      # "class" 키의 값이 joined_list에 있는 경우만 유지
      filtered_posts = [
          post for post in posts if post.get('class') in joined_list
      ]

      return render_template('notice_t.html', postings=filtered_posts)
  except:
    return render_template('error.html')


@app.route('/noticeview/<string:num>')
def noticeview(num):
  if num == "6":
    with open('class.json', 'r') as f:
      data = json.load(f)
    return render_template('applynotice.html', lectures=data)
  else:
    return render_template('noticeview.html', num=num)


@app.route('/postview/<string:num>')
def postview(num):
  with open('posts.json', 'r') as f:
    data = json.load(f)
  for item in data:
    if item['num'] == num:
      name = item['name']
      naeyong = item['content']
  return render_template('postview.html', title=name, content=naeyong)


@app.route('/classinfo/<string:num>', methods=['GET', 'POST'])
def classinfo(num):
  teacher_list = []
  teachers = open('teachers.txt', 'r', encoding="utf-8")
  lines = teachers.readlines()
  for line in lines:
    line = line.strip()
    teacher_list.append(line)
  try:
    name = unquote(request.cookies.get('name'))
  except:
    return '<script>location.href="https://32fcfb33-7a7b-4b47-8c3d-4e2b0260a1bb-00-3c18wu9dtnmx2.janeway.replit.dev/login"</script>'

  if name not in teacher_list:
    with open('class.json', 'r') as f:
      data = json.load(f)
    for item in data:
      if item['code'] == num:
        name = item['name']
        teacher = item['teacher']
        info = item['info']
        week = item['week']
    return render_template('classinfo.html',
                           title=name,
                           week=week,
                           teacher=teacher,
                           content=info)
  else:
    with open('user.json', 'r') as f:
      data = json.load(f)
    with open('student.json', 'r') as file:
      posts = json.load(file)
    for item in data:
      isjoined = item['class'].split('/')
      if num in isjoined:
        name = item['name']
        posts.append({
            "name": name,
        })
    with open('class.json', 'r') as f:
      classes = json.load(f)
    for thing in classes:
      if thing['code'] == num:
        name = thing['name']
        teacher = thing['teacher']
        week = thing['week']

    weeks = []
    for i in range(1, int(week) + 1):
      weeks.append(i)

    return render_template('classinfo_t.html',
                           students=posts,
                           code=num,
                           name=name,
                           week=week,
                           weeks=weeks,
                           teacher=teacher)


@app.route('/submit', methods=['POST'])
def submit():
  data = request.form  # form data를 받아옵니다.
  attend = []
  late = []
  absent = []

  for key, value in data.items():
    if value == '출석':
      attend.append(key)
    elif value == '지각':
      late.append(key)
    elif value == '결석':
      absent.append(key)
    elif key == 'today':
      week = value

  code = request.form["code"]
  with open('class.json', 'r') as f:
    data = json.load(f)
  for item in data:
    if item['code'] == code:
      name = item['name']

  status = {"attend": attend, "late": late, "absent": absent}
  with open(f'./ClassDB/{code}/{week}.json', 'w', encoding='utf-8') as file:
    json.dump(status, file, indent=4, ensure_ascii=False)

  return '<script>alert("출석체크가 완료되었습니다");location.href="https://32fcfb33-7a7b-4b47-8c3d-4e2b0260a1bb-00-3c18wu9dtnmx2.janeway.replit.dev/lesson"</script>'


@app.route('/lesson')
def lesson():
  try:
    teacher_list = []
    teachers = open('teachers.txt', 'r', encoding="utf-8")
    lines = teachers.readlines()
    for line in lines:
      line = line.strip()
      teacher_list.append(line)
    try:
      name = unquote(request.cookies.get('name'))
    except:
      return render_template('lesson.html', postings="")
    if name not in teacher_list:
      with open('class.json', 'r') as f:
        lessons = json.load(f)
      joinedclass = authutil.getinfo("class", name)
      joined_list = joinedclass.split('/')

      # "class" 키의 값이 joined_list에 있는 경우만 유지
      filtered_posts = [
          lesson for lesson in lessons if lesson.get('code') in joined_list
      ]

      return render_template('lesson.html', postings=filtered_posts)
    else:
      teacher_list = []
      teachers = open('teachers.txt', 'r', encoding="utf-8")
      lines = teachers.readlines()
      for line in lines:
        line = line.strip()
        teacher_list.append(line)
      try:
        name = unquote(request.cookies.get('name'))
      except:
        return render_template('lesson.html', postings="")
      with open('class.json', 'r') as f:
        lessons = json.load(f)
      joinedclass = authutil.getinfo("class", name)
      joined_list = joinedclass.split('/')

      filtered_posts = [
          lesson for lesson in lessons if lesson.get('code') in joined_list
      ]

      return render_template('lesson_t.html', postings=filtered_posts)
  except:
    return render_template('error.html')


@app.route('/account', methods=['GET', 'POST'])
def account():
  try:
    name = unquote(request.cookies.get('name'))
    ps = unquote(request.cookies.get('password'))
    res = authutil.verify(name, ps)
    if res:
      school = authutil.getinfo('school', name)
      grade = authutil.getinfo('grade', name)
      if school == "NULL":
        return render_template('account.html',
                               name="정보없음",
                               school="정보없음",
                               grade="정보없음")
      else:
        return render_template('account.html',
                               name=name,
                               school=school,
                               grade=grade)
    else:
      return render_template('error.html')
  except:
    return render_template('account.html')


@app.route('/upload', methods=['GET', 'POST'])
def upload():
  teacher_list = []
  teachers = open('teachers.txt', 'r', encoding="utf-8")
  lines = teachers.readlines()
  for line in lines:
    line = line.strip()
    teacher_list.append(line)
  name = unquote(request.cookies.get('name'))
  if name not in teacher_list:
    return render_template('error.html')
  else:
    ps = unquote(request.cookies.get('password'))
    res = authutil.verify(name, ps)
    if res:
      if request.method == 'POST':
        haha = open('postnum.txt', 'r', encoding="utf-8")
        read = haha.readline()
        haha.close()
        read = int(read) + 1
        haha = open('postnum.txt', 'w', encoding="utf-8")
        haha.write(f"{read}")
        haha.close()
        title = request.form["title"]
        content = request.form["content"]
        teacher = unquote(request.cookies.get('name'))
        classcode = request.form["classcode"]

        with open('posts.json', 'r') as file:
          posts = json.load(file)
        posts_original = posts
        try:
          if classcode == "00":
            posts.append({
                "name": f"[{teacher}T/전체공지] - {title}",
                "class": classcode,
                "num": f"{read}",
                "content": content
            })
            # write back to apps.json
            with open('posts.json', 'w') as file:
              json.dump(posts, file, indent=4, ensure_ascii=False)

            return render_template(
                'message.html',
                msg="공지가 업로드 되었습니다. 삭제는 원장에게 연락하세요. 010-8850-1571",
            )
          else:
            posts.append({
                "name": f"[{teacher}T/{classcode}] - {title}",
                "class": classcode,
                "num": f"{read}",
                "content": content
            })
            # write back to apps.json
            with open('posts.json', 'w') as file:
              json.dump(posts, file, indent=4, ensure_ascii=False)

            return render_template(
                'message.html',
                msg="공지가 업로드 되었습니다. 삭제는 원장에게 연락하세요. 010-8850-1571",
            )
        except:
          return render_template("error.html")
      else:
        return render_template('upload.html')
    else:
      return render_template('error.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
  if request.method == "GET":
    return render_template('login.html')
  else:
    res = authutil.verify(request.form["name"], request.form["password"])
    if res:
      return render_template('index.html',
                             save="true",
                             name=request.form["name"],
                             password=request.form["password"])
    else:
      return render_template('login.html', save="false")


@app.route('/create', methods=['GET', 'POST'])
def create():
  teacher_list = []
  teachers = open('teachers.txt', 'r', encoding="utf-8")
  lines = teachers.readlines()
  for line in lines:
    line = line.strip()
    teacher_list.append(line)
  name = unquote(request.cookies.get('name'))
  if name not in teacher_list:
    return render_template('error.html')
  else:
    ps = unquote(request.cookies.get('password'))
    res = authutil.verify(name, ps)
    if res:
      if request.method == 'POST':
        haha = open('classnum.txt', 'r', encoding="utf-8")
        read = haha.readline()
        haha.close()
        read = int(read) + 1
        haha = open('classnum.txt', 'w', encoding="utf-8")
        haha.write(f"{read}")
        haha.close()
        name = request.form["name"]
        info = request.form["info"]
        week = request.form["week"]
        teacher = unquote(request.cookies.get('name'))

        with open('class.json', 'r') as file:
          posts = json.load(file)
        posts_original = posts
        try:
          code = str(read).zfill(2)
          posts.append({
              "name": name,
              "code": code,
              "week": week,
              "teacher": teacher,
              "info": info
          })
          # write back to apps.json
          with open('class.json', 'w') as file:
            json.dump(posts, file, indent=4, ensure_ascii=False)

          os.mkdir(f'./ClassDB/{code}')
          for i in range(1, int(week) + 1):
            with open(f'./ClassDB/{code}/{i}주차.json', 'w') as file:
              json.dump("", file, ensure_ascii=False)

          usermanager.addclass(teacher, code)
          return render_template(
              'message.html',
              msg="수업이 생성되었습니다. 삭제는 원장에게 연락하세요. 010-8850-1571",
          )
        except:
          return render_template("error.html")
      else:
        return render_template('create.html')
    else:
      return render_template('error.html')


@app.route('/attend')
def attend():
  return render_template('attend.html')


@app.route('/apply', methods=['GET', 'POST'])
def apply():
  if request.method == "GET":
    with open('class.json', 'r') as f:
      data = json.load(f)
    name = unquote(request.cookies.get('name'))
    return render_template('apply.html', lectures=data, name=name)
  elif request.method == "POST":
    name = unquote(request.cookies.get('name'))
    with open('class.json', 'r') as f:
      data = json.load(f)
    for item in data:
      status = request.form.get(item['name'])
      if status:
        usermanager.addclass(name, item['code'])
  return '<script>alert("수강신청 되었습니다.");location.href="https://32fcfb33-7a7b-4b47-8c3d-4e2b0260a1bb-00-3c18wu9dtnmx2.janeway.replit.dev/lesson"</script>'


app.run(host='0.0.0.0', port=8080, debug=True)
