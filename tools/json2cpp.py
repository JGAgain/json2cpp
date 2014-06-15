import json
import string
import os
import sys
global have_namespace_protect
have_namespace_protect=True
all_class_list = []
global relative_path

def GetFilenameFromPath(file_path):
	print("GetFilenameFromPath %s" %(file_path))
	startpos = 0
	endpos = -1
	if file_path.rfind('/') != -1:
		startpos = file_path.rfind('/') + 1
	elif file_path.rfind('\\') != -1:
		startpos = file_path.rfind('\\') + 1
	endpos = file_path[startpos:].rfind('.') 
	print(file_path[startpos: endpos])
	return file_path[startpos: endpos]

def GuessArrayType(array, parent_key): 
	array_default_type = None
	guess_type = int
	print (array)
	for element in array:
		if (type(element) is not guess_type):
			guess_type = array_default_type
			break
	if (guess_type != None):
		return "int"

	guess_type = float
	for element in array:
		if (type(element) is int):
			continue
		elif (type(element) is not guess_type):
			guess_type = array_default_type
			break
	if (guess_type != None):
		return "float"

	guess_type = bool
	for element in array:
		if (type(element) is not guess_type):
			guess_type = array_default_type
			break
	if (guess_type != None):
		return "bool"
	
	guess_type = unicode
	for element in array:
		if (type(element) is not guess_type):
			guess_type = array_default_type
			break
	if (guess_type != None):
		return "std::string"

	guess_type = str
	for element in array:
		if (type(element) is not guess_type):
			guess_type = array_default_type
			break
	if (guess_type != None):
		return "std::string"
	
	 #return "Json::Value"
	guess_type = dict
	for element in array:
		if (type(element) is  guess_type):
			FindObject(element, parent_key)
			guess_type =  parent_key
			return guess_type
	guess_type = list
	for element in array:
		if (type(element) is guess_type):
			guess_type = ("std::vector<%s > " %(GuessArrayType(element, parent_key)))
			return guess_type

def FindObject(json_dict, class_name):
	member_table = []
	for key in json_dict:
		member = {}
		var_type = ""
		var_name = ""
		b_is_class = False
		 # print (type(json_dict[key]))
		if (type(json_dict[key]) is dict):
			var_type = key[0].upper() + key[1:]
			FindObject(json_dict[key], var_type)
			b_is_class = True
		elif (type(json_dict[key]) is int):
			var_type = "int"
		elif (type(json_dict[key]) is float):
			var_type = "float"
		elif (type(json_dict[key]) is str or type(json_dict[key]) is unicode):
			var_type = "std::string"
		elif (type(json_dict[key]) is list):
			array_type = GuessArrayType(json_dict[key], key[0].upper() + key[1:])
			var_type = ("std::vector<%s>" %(array_type))
		elif (type(json_dict[key]) is bool):
			var_type = "bool"
		else:
			assert(False)
		var_name = key
		member[var_type] = {}
		member[var_type]["value"] = var_name
		member[var_type]["is_custom_class"] = b_is_class;
		member_table.append(member)
	class_object = {}
	class_object[class_name] = member_table
	all_class_list.append(class_object)
	return
def HaveNamespaceProtect(file_name):
		
	return have_namespace_protect

def GemHFileCode(file_name):
	global relative_path
	print (relative_path + '/' +  file_name + ".h\n")
	fh = open(relative_path + '/' + file_name + ".h", "w")
	fh.write("// Don't Edit it\n")
	fh.write("#ifndef %s_H_\n" %(file_name.upper()))
	fh.write("#define %s_H_\n" %(file_name.upper()))
	fh.write("\n")

	fh.write("#include <string>\n")
	fh.write("#include <vector>\n")
	fh.write("#include <lib_json/json_lib.h>\n")
	fh.write("\n")
	fh.write("\n")
	fh.write("class JsonSerializerHelper;\n")
	fh.write("\n")

  	fh.write("namespace net {\n")
	if HaveNamespaceProtect(file_name):
								fh.write("namespace %s {\n" %(file_name))

	fh.write("\n")

	fh.write("\n")
	print(file_name)
	for class_object in all_class_list:
		print (class_object)
		assert(len(class_object) == 1)
		class_name = ""
		member_table = []
		for key in class_object:
			class_name = key
			member_table = class_object[key]
			break
		fh.write("class %s {\n" %(class_name))
		fh.write(" public:\n")
		fh.write("\t%s();\n" %(class_name))
		fh.write("\t~%s(){}\n" %(class_name))
		fh.write("\n")
		for member in member_table:
			assert(len(member) == 1)
			for key in member:
				var_type = key
				var_name = member[key]["value"]
				if member[key]["is_custom_class"] == True:
					fh.write("\t%s& get_%s() { return %s;}\n" %(var_type, var_name, var_name))
					fh.write("\tconst %s& get_%s() const { return %s;}\n" %(var_type, var_name, var_name))
				else:
					fh.write("\tconst %s& get_%s() { return %s;}\n" %(var_type, var_name, var_name))
					fh.write("\tconst %s& get_%s() const { return %s;}\n" %(var_type, var_name, var_name))
				fh.write("\tvoid set_%s(const %s& %s_a) {\n\t\t %s = %s_a; \n\t}\n" %(var_name, var_type,\
						var_name, var_name, var_name))
				fh.write("\n")

		fh.write("\n")
		fh.write("\tvoid Serialize(JsonSerializerHelper& json_serializer_helper) const;\n")
		fh.write("\tvoid DeSerialize(const JsonSerializerHelper& json_serializer_helper);\n")
		fh.write("\n")
		
		fh.write(" private:\n")
		for member in member_table:
			assert(len(member) == 1)
			for key in member:
				var_type = key
				var_name = member[key]["value"]
				fh.write("\t %s %s;\n" %(var_type, var_name))
		fh.write("\n")
		
		fh.write("}; // class %s\n\n" %(class_name))
	if HaveNamespaceProtect(file_name):
								fh.write("} // namespace %s\n" %(file_name))
	fh.write("} // namespace net\n")
	fh.write("#endif // %s_H_\n" %(file_name.upper()))
	fh.close()
	return 

def GemCppFileCode(file_name): 
	global relative_path
	print (relative_path + '/' +  file_name + ".cpp\n")
	fcpp = open(relative_path + '/' +  file_name + ".cpp", "w")
	fcpp.write("//Don't Edit it\n\n")
	fcpp.write("#include \"%s.h\"\n" %(file_name))
	fcpp.write("#include \"network/net_util/json_serializer_helper.hpp\"\n")
	fcpp.write("\n")    
	
	fcpp.write("\n")


	fcpp.write("namespace net {\n")
	if HaveNamespaceProtect(file_name):
								fcpp.write("namespace %s {\n" %(file_name))
	fcpp.write("\n") 

	for class_object in all_class_list:
		print (class_object)
		assert(len(class_object) == 1)
		class_name = ""
		member_table = []
		for key in class_object:
			class_name = key
			member_table = class_object[key]
			break
		have_init_memeber = False
		for i in range(len(member_table)):
			member = member_table[i]
			assert(len(member) == 1)
		
			for key in member:
				var_type = key
				var_name = member[key]["value"]
				if (var_type == "int" or var_type == "bool" or var_type == "float"):
					have_init_memeber = True
					break
			if (have_init_memeber == True):
				break
			
		if (have_init_memeber == True):
			fcpp.write("%s::%s():" %(class_name, class_name))
		else:
			fcpp.write("%s::%s()" %(class_name, class_name))

		
		first_member = True
		for i in range(len(member_table)):
			member = member_table[i]
			assert(len(member) == 1)
		
			for key in member:
				var_type = key
				var_name = member[key]["value"]
				var_value = None
				if (var_type == "int"):
					var_value = "0"
				elif (var_type == "bool"):
					var_value = "false"
				elif (var_type == "float"):
					var_value = "0.0"

				if var_value != None:
					if not first_member:
						fcpp.write(",\n")
					fcpp.write(("\t\t%s(%s)" %(var_name, var_value)))
					first_member = False
				break

		fcpp.write("{\n}\n")
		fcpp.write("\n")
		fcpp.write("void %s::Serialize(\n\t\t\
JsonSerializerHelper& json_serializer_helper) const {\n" %(class_name)) 
		for i in range(len(member_table)):
			member = member_table[i]
			assert(len(member) == 1)
			for key in member:
				var_name = member[key]["value"]
				fcpp.write("\tjson_serializer_helper.SerializeNVP(%s);\n" %(var_name))
		fcpp.write("}\n\n")
	
		fcpp.write("void %s::DeSerialize(\n\t\t\
const JsonSerializerHelper& json_serializer_helper) {\n" %(class_name)) 
		for i in range(len(member_table)):
			member = member_table[i]
			assert(len(member) == 1)
			for key in member:
				var_name = member[key]["value"]
				fcpp.write("\tjson_serializer_helper.DeSerializeNVP(%s);\n" %(var_name))
		fcpp.write("}\n\n")
		fcpp.write("\n")
	if HaveNamespaceProtect(file_name):
			fcpp.write("} // namespace %s\n" %(file_name))
	fcpp.write("} // namespace net\n")
	fcpp.close()

def GemCode(file_name):
	GemHFileCode(file_name)
	GemCppFileCode(file_name)
	return 

def Parse(file_path, file_name):
	del all_class_list[:]
	fp = open(file_path,"r")
	json_dict = json.load(fp)
	fp.close()
	#print (root_class_name)
	root_class_name = file_name[0].upper() + file_name[1:]
	FindObject(json_dict, root_class_name)
	print(len(all_class_list))
	GemCode(file_name)
	print("Success!!!!!!!!!!!\n")
	return
def GemProtoCpp(proto_dir_path, proto_out_path):
	global relative_path
	relative_path = proto_out_path
	print (relative_path)
	for top, dirs, nondirs in os.walk(proto_dir_path):
		for file_name in nondirs:
			file_path = top + '/' + file_name
			print (file_path)
			endpos = file_name.rfind('.json')
			if (endpos != -1 ):
			  Parse(file_path, file_name[:endpos])

for i in range(1, len(sys.argv)):
	if (sys.argv[i] == "-h" or sys.argv[i] == "--help"):
		print ("Usage--:\n python json2cpp.py in.json\n\
				--output $pwd/in.h $pwd/in.cpp\n")
		break
	startpos = 0
	endpos = sys.argv[i].rfind('.')
	if sys.argv[i].rfind('/') != -1:
		startpos = sys.argv[i].rfind('/') + 1
	elif sys.argv[i].rfind('\\') != -1:
		startpos = sys.argv[i].rfind('\\') + 1
	file_name = sys.argv[i][startpos:endpos]
	relative_path = sys.argv[i][:startpos]
	Parse(sys.argv[i], file_name)
	print ("Success!!!!!!!\n")
