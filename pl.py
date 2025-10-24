persons = [
  {"id":1,"name":"tanaka1"},
  {"id":2,"name":"tanaka2"},
  {"id":3,"name":"tanaka3"},
]

# for person in persons:
#   for i,v in person.items():
#     print(i,v)

# for person in persons:
#   print(person["name"])

# persons[0]["name"]="yamada"
# print(persons[0])

for person in persons:
    if person["id"]==1:
        persons.pop(1-1)

print(persons)