import ast

in_file = 'all_city.txt'
with open(in_file) as f:
    row = f.readlines()

uniq_city = set()
uniq_data = []

rows = [x for x in row]
for row in rows:
    dict_city = ast.literal_eval(row)
    if dict_city['name'] not in uniq_city:
        #print(dict_city)
        uniq_city.add(dict_city['name'])
        uniq_data.append(dict_city)

out_file = 'good_city.txt'
with open(out_file, "w") as out_f:
    for row in uniq_data:
        out_f.write(str(row) + '\n')
