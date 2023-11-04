import redis   # 导入redis 模块

r = redis.Redis(host='127.0.0.1', port= 6379, password= 'QsYGF4sqpKIejBrTukYxzZW5DYnHhDZ8', db= 0)

r.set('name', 'runoob')  # 设置 name 对应的值
print(r['name'])
print(r.get('name'))  # 取出键 name 对应的值
print(type(r.get('name')))  # 查看类型