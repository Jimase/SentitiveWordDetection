l=[1,2,3]
print(id(l))
def a(x):
  print(id(x))
  x.pop()
  print(x)
  print(id(x))
  x=x+[3]
  print(x)
  print(id(x))
a(l)