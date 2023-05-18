from Read import Read_code
import re




class Hash_Table:
    def __init__(table, record):
        table.record = record
        
    
    def insert(table, idefNmae, attributes):
        table.record.append([idefNmae, attributes])            
            
        
    def lookout(table, ID):
        return(table.record[ID])
        
        
    def get_table(table):
        return(table.record)
    
    
    
class Sematic_analyzer:
    
    def __init__(program, code, key):
        print("---------program: 1---------")
        
        
        program.key = key
        program.code = Read_code(code)
        program.numberOfLines = program.code.line_counter()
        conditions = ['if', 'else if', 'else']
        loops = ['for', 'while']
        class_name = []
        constructor_name = []
        method_name = []
        for Line_counter in range(0, program.numberOfLines):
            if(program.code.class_confirm(Line_counter)):
                classes = program.code.extract_class(Line_counter)
                class_name.append(classes[3])
                
                parent = ""
                for par_counter in classes[4]:
                    parent = parent + classes[4][classes[4].index(par_counter)]
                print("key: Class_", classes[3], " | vlue: class(name: ", classes[3], ") (parent: [", parent, "])", sep="")
                
                methods = classes[6]
                for Line in methods:
                    if(methods[methods.index(Line)][3] == 'constructor'):
                        constructor_name.append(methods[methods.index(Line)][4])
                    else:
                        method_name.append(methods[methods.index(Line)][4])
                    
        print("=============================================================================")

        program.key.append(conditions) #key[0]
        program.key.append(loops) #key[1]
        program.key.append(class_name) #key[2]
        program.key.append(constructor_name) #key[3]
        program.key.append(method_name) #key[4]
                
        
    def insert(program):
        HT = Hash_Table([])
        for Line_counter in range(0, program.numberOfLines):
            LINE = program.code.get_line(Line_counter)
            scope = program.code.extract_scope(Line_counter)
            if(scope != False):
                HT.insert(scope[0], scope[1])
            
        table = HT.get_table()
        return(table)
    
    
    def printer(program):
        HT = program.insert()
        for counter in HT:
            if(HT[HT.index(counter)][0] == 'class'):
                print("---------", HT[HT.index(counter)][1][3], ": ", HT[HT.index(counter)][1][1], "---------", sep = "")
                fields = HT[HT.index(counter)][1][5]
                for counter2 in fields:
                    print("key : Field_", fields[fields.index(counter2)][1], " | Values : ClassField(name:",fields[fields.index(counter2)][1], ") (type : ", fields[fields.index(counter2)][0], ")", sep = "")
                
            if(HT[HT.index(counter)][0] == 'constructor'):
                cunstructor = HT[HT.index(counter)][1]
                
                name = cunstructor[4]
                value = cunstructor[3]
                return_type = "[]"
                parameter_type = cunstructor[5]
                parameter_name = cunstructor[6]
                for par_counter in parameter_type:
                    parameter = "[name: " + parameter_name[parameter_type.index(par_counter)] + ", type: " + parameter_type[parameter_type.index(par_counter)] + ", index: " + str(parameter_type.index(par_counter)+1) + "]"
                print("key : Constructor_", name, " | Values : ", value, "(name:", parameter_type, ") (returntype: []",  ") (parameterlist: ", parameter, sep = "")
                
            if(HT[HT.index(counter)][0] == 'method'):
                method = HT[HT.index(counter)][1]
                
                name = method[4]
                value = "method"
                return_type = method[3]
                parameter_type = method[5]
                parameter_name = method[6]
                
                if(len(parameter_type) > 1):
                    ans = ""
                    for par_counter in parameter_type:
                        parameter = "[name: " + parameter_name[parameter_type.index(par_counter)] + " type: " + parameter_type[parameter_type.index(par_counter)] + ", index: " + str(parameter_type.index(par_counter)+1) + "]"
                        ans = ans + parameter
                else:
                    ans = "[]"
                
                print("key : Method_", name, " | Values : ", value, "(name: ", name, ") (return type: [", return_type,"]",  ") (parameterlist: ", ans, ")", sep = "")
                
        
    def get_value(program):
        HT = program.insert()
        for counter in HT:
            if(HT[HT.index(counter)][0] == 'class'):
                fields = HT[HT.index(counter)][1][5]
                val = []
                string = "---------" + HT[HT.index(counter)][1][3] + ": " + str(HT[HT.index(counter)][1][1]) + "---------"
                val.append(string)
                for counter2 in fields:
                    string = "key : Field_" + fields[fields.index(counter2)][1] + " | Values : ClassField(name:" + fields[fields.index(counter2)][1] + ") (type : " + fields[fields.index(counter2)][0] + ", isDefined:" + str(fields[fields.index(counter2)][2]) + ")"
                    val.append(string)
                method = HT[HT.index(counter)][1][6]
                for m_counter in method:
                    curr_method = method[method.index(m_counter)]
                    print(curr_method)
                    if(curr_method[3] == 'constructor'):
                        cunstructor = curr_method
                        name = cunstructor[4]
                        value = cunstructor[3]
                        return_type = "[]"
                        parameter_type = cunstructor[5]
                        parameter_name = cunstructor[6]
                        for par_counter in parameter_type:
                            parameter = "[name: " + parameter_name[parameter_type.index(par_counter)] + ", type: " + parameter_type[parameter_type.index(par_counter)] + ", index: " + str(parameter_type.index(par_counter)+1) + "]" + ")"
                        string = "key : Constructor_" + name + " | Values : " + value + "(name:" + name + ") (returntype: []" +  ") (parameterlist: " + parameter
                        val.append(string)
                        
           
                        
                    else:
                        m = curr_method
                        name = m[4]
                        value = "method"
                        return_type = m[3]
                        parameter_type = m[5]
                        parameter_name = m[6]

                        if(len(parameter_type) > 1):
                            ans = ""
                            for par_counter in parameter_type:
                                parameter = "[name: " + parameter_name[parameter_type.index(par_counter)] + " type: " + parameter_type[parameter_type.index(par_counter)] + ", index: " + str(parameter_type.index(par_counter)+1) + "]"
                                ans = ans + parameter
                        else:
                            ans = "[]"

                        string = "key : Method_" + name + " | Values : " + value + "(name: " + name + ") (return type: [" + return_type + "]" +  ") (parameterlist: " + ans + ")"
                        val.append(string)
                    
                 
                    
            if(HT[HT.index(counter)][0] == 'constructor'):
                L = "============================================================================="
                val.append(L)  
                cunstructor = HT[HT.index(counter)][1]
                
                name = cunstructor[4]
                value = cunstructor[3]
                return_type = "[]"
                parameter_type = cunstructor[5]
                parameter_name = cunstructor[6]
                for par_counter in parameter_type:
                    parameter = "[name: " + parameter_name[parameter_type.index(par_counter)] + ", type: " + parameter_type[parameter_type.index(par_counter)] + ", index: " + str(parameter_type.index(par_counter)+1) + "]"
                string = "key : Constructor_" + name + " | Values : " + value + "(name:" + name + ") (returntype: []" +  ") (parameterlist: " + parameter
                val.append(string)
            
            
            
            
            if(HT[HT.index(counter)][0] == 'method'):
                L = "============================================================================="
                val.append(L)
                defined = ['int', 'float', 'string', 'bool']
                method = HT[HT.index(counter)][1]
                print(method)
                string = "---------" + method[4] + ": " + str(method[1]) + "---------"
                val.append(string)
                
                
                
                
                param_type = method[5]
                param_name = method[6]
                
                param_size = len(param_name)
                param = ""
                if(param_size > 0):
                    for f_counter in param_type:
                        if param_type[param_type.index(f_counter)] in defined:
                            d = True
                        else:
                            d = False
                        param = "Key: Field_" + param_name[param_type.index(f_counter)] + " |  Value : ParamField(name:" + param_name[param_type.index(f_counter)] + ")" + "(type:" + param_type[param_type.index(f_counter)] +", isDefined:" + str(d) + ")"
                        val.append(param)
                
                filed_type = method[7]
                filed_name = method[8]
                filed_def = method[9]
                field_size = len(filed_type)
                fields = ""
                if(field_size > 0):
                    for f_counter in filed_type:
                        fields = "Key: Field_" + filed_name[filed_type.index(f_counter)] + " |  Value : MethodVar(name:" + filed_name[filed_type.index(f_counter)] + ")" + "(type:" + filed_type[filed_type.index(f_counter)] +", isDefined:" + str(filed_def[filed_type.index(f_counter)]) + ")"
                        val.append(fields)
                
                
                        
            
            
            if(HT[HT.index(counter)][0] == 'loop'):
                name = HT[HT.index(counter)][1][1]
                l = HT[HT.index(counter)][1][2]
                string = "---------" + name + ": " + str(l) + "---------"
                val.append(string)
                L = "============================================================================="
                val.append(L)
                
            
            if(HT[HT.index(counter)][0] == 'condition'):
                name = HT[HT.index(counter)][1][1]
                l = HT[HT.index(counter)][1][2]
                string = "---------" + name + ": " + str(l) + "---------"
                val.append(string)
                L = "============================================================================="
                val.append(L)
            
        return(val)
        
    def toString(program):
        string = program.get_value()
        for counter in string:
            print(string[string.index(counter)])
        
    def get_key(program):
        print(program.key)







f = open("testcase/test.txt", "r")
text = f.readlines()

c1 = Sematic_analyzer(text, [])
c1.toString()
