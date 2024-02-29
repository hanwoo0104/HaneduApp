import hashlib, json


def verify(nameinput, passwordinput):  #여기 JSON으로 바꾸기
  try:
    lock_ps = hashlib.sha256(passwordinput.encode())
    ps_result = lock_ps.hexdigest()
    with open('user.json', 'r') as f:
      data = json.load(f)
    for item in data:
      if item['name'] == nameinput:
        ps_get = item['password']

    return ps_result == ps_get
  except:
    return False


def getinfo(infoname, nameinput):
  try:
    with open('user.json', 'r') as f:
      data = json.load(f)
    for item in data:
      if item['name'] == nameinput:
        school = item['school']
        grade = item['grade']
        joinedclass = item['class']

    if infoname == 'school':
      return school
    if infoname == 'grade':
      return grade
    if infoname == 'class':
      return joinedclass

  except Exception as e:
    return e

  #뒤에 이어서 작성


def getClassName(nameinput):
  student = open('./DB/Class/student.txt', 'r', encoding="UTF-8")
  lines = student.readlines()
  line_list = []
  dataindexes = []
  for line in lines:
    line = line.strip()
    line_list.append(line)
  for line in lines:
    linestrip = line.split('/')
    if nameinput in linestrip:
      dataindexes.append(line_list.index(line))

  name = open('./DB/Class/name.txt', 'r', encoding="UTF-8")
  lines = name.readlines()
  names_list = []
  for line in lines:
    line = line.strip()
    names_list.append(line)

  joinedclasslist = []
  for index in dataindexes:
    joinedclasslist.append(names_list[index])

  return joinedclasslist


#작성예정
def getClassCode(nameinput):
  student = open('./DB/Class/student.txt', 'r', encoding="UTF-8")
  lines = student.readlines()
  line_list = []
  for line in lines:
    line = line.strip()
    line_list.append(line)
  for line in lines:
    linestrip = line.split('/')
    if nameinput in linestrip:
      dataindex = line_list.index(line)

  classcode = open('./DB/User/class.txt', 'r', encoding="UTF-8")
  lines = joinedclass.readlines()
  joinedclass_list = []
  for line in lines:
    line = line.strip()
    joinedclass_list.append(line)
