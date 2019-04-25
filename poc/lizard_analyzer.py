#from lizard import analyze_file
import lizard
#analyze_file.analyze_source_code('repo/terrame/packages/base/lua/CellularSpace.lua', source_code).function_list

i = lizard.analyze_file('repo/terrame/packages/base/lua/Cell.lua')
#print(i.function_list)

for func in i.function_list:
	print(func.name)
	#print(func.long_name)