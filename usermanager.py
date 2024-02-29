import json


def addclass(nameinput, classcode):
  with open('user.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

  for user in data:
    if user['name'] == nameinput:
      nowclass = user['class']
      nowclass = nowclass.split('/')
      nowclass.append(classcode)
      user['class'] = '/'.join(nowclass)

  with open('user.json', 'w', encoding='utf-8') as file:
    json.dump(data, file, indent=4, ensure_ascii=False)
