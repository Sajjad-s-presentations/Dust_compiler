## Requirements:
```
python3
pip install re
```
## how to run?
- Place your program code named "text.txt" in the path .../testcase/filename
- run follwing script
```
python3 Semantic_analyzer.py
```
## Usage
This program acts as a lexical analyzer. To do this, the following steps are taken:
- Read.py: It is responsible for reading and extracting the elements we need from inside the code
- Semanticـanalyzer.py: It displays the requested items in the project form

### Read.py
First, we prepare a class to read the code.
```
class Read_code:
    def __init__(code, body):
        print("constructor is called!")
        code.body = body
```

After receiving the line number, this function returns the contents of that line.
```
def get_line(code, line_no):
  return code.body[line_no]
```

This function receives the contents of the line and removes the leading spaces for subsequent functions.

```
    def remove_space(code, line_no):
        space_counter = 0
        index = 0
        new_str = code.body[line_no].lstrip()
        #print("Line ", line_no, " is: ", code.body[line_no])
        return new_str
```
This function counts the number of all lines of code.

```
    def line_counter(code):
        counter = 0
        for line in code.body:
            counter += 1
        return counter
```


It specifies how deep we are in the code. For example, if the current class is at depth zero, its subset functions are placed at depth one. Now, if these functions themselves have commands, we consider these commands in depth 2.
```
    def depth_finder(code, line_no):
        space_counter = 0
        index = 0
        #print("Line ", line_no, " is: ", code.body[line_no])
        for survey in code.body[line_no]:
            #print(code.body[line_no][index])
            if(code.body[line_no][index] == " "):
                space_counter += 1
                index += 1
            else:
                return space_counter/4
```
In any part of the code, it tells us the number of parrots left until the next bracket and the completion of the current depth.
```
    def next_braket(code, line_no): 
        current_line = line_no
        last_line = code.line_counter()
        open_braket_counter = 0
        for counter in range(current_line+1, last_line):
            if '{' in code.body[counter]:
                open_braket_counter += 1
            if '}' in code.body[counter]:
                if(open_braket_counter == 0):
                    return counter
                else:
                    open_braket_counter = open_braket_counter-1
```

Specifies the name of the class we are currently in. We will use this function in the following extractions.
```
    def prev_class_name(code, line_no):
        class_name = ""
        for counter in range(line_no, -1, -1):
            s = code.remove_space(counter)            
            if 'class' in s:
                curr_s = s.split()
                curr_s = curr_s[1]
                curr_s = curr_s.split("(")
                class_name = curr_s[0]
                
        if(class_name == ""):
            return("Not found!")
        else:
            return(class_name)
```

Confirms the import
```
    def find_imports(code):
        Line = 0
        imports = []
        for line in code.body:
            if(code.depth_finder(Line) == 0):
                s = code.remove_space(Line)
                if 'import' in s:
                    index = s.find('import')
                    s = code.body[Line][7:]
                    s = s.strip('\n')
                    imports.append(s)

                Line += 1
                
        return(imports)
```
Confirms the existence of the field
```
    def field_confirm(code, line_no):
        keywords = ['int', 'bool', 'float', 'string', 'double']
        s = code.body[line_no]
        s = code.remove_space(line_no)
        s = s.split(" ")
        confirm = any(word in keywords for word in s)
        if(confirm):
            if "=" not in s:
                if "def" not in s:
                    return True
        else:
            if(s[0][0].isupper()):
                if "=" not in s:
                    if "def" not in s:
                        return True
            else:
                return False
```
If it is a field, it returns the field information as an array. This array contains the following information:
- type
- name
- isDefined

```
    def get_field(code, line_no):
        s = code.body[line_no]
        s2 = code.body[line_no]
        s = code.remove_space(line_no).strip('\n').split(" ")
        field_type = s[0]
        field_name = s[1]
        
        if "[" in field_type:
            open_parantes_index = field_type.index("[")
            close_parantes_index = field_type.index("]")
            field_type = field_type[:open_parantes_index] + field_type[close_parantes_index+1:]
           
        
        
        Defined = ['int', 'float', 'string', 'bool']    
        isDefined = False
        if field_type in Defined:
            isDefined = True
            
        return(field_type, field_name, isDefined)
```

They are a confirmation of class and functionality.
```
    def def_confirm(code, line_no):
        s = code.body[line_no]
        if 'def' in s:
            return True
        else:
            return False
        
    def class_confirm(code, line_no):
        s = code.body[line_no]
        if 'class' in s:
            return True
        else:
            return False
```
As its name suggests, it confirms being a scope. The scopes are as follows:
- program
- class
- function
- conditions and loops

```
    def scope_confirm(code, line_no):
        
        s = code.body[line_no]
        curr_string = code.remove_space(line_no)
        first_word = curr_string.split('(')
        first_word = first_word[0]
        
        conditions = ['if', 'else if', 'else']
        loops = ['for', 'while']
        
        confirm = 0
        scope = ""
        
        if(code.def_confirm(line_no)):
            confirm = 1
            scope = "method"
        
        if(code.class_confirm(line_no)):
            confirm = 1
            scope = "class"
        
        if first_word in conditions:
            confirm = 1
            scope = ("condition", first_word)
        
        if first_word in loops:
            confirm = 1
            scope = ("loop", first_word)
        
        if(confirm == 1):
            return (True, scope)
        else:
            return (False, 'null')
```
It returns all the information we need that are in a function as an array.
```
def extract_def(code, line_no, class_name):
        def_depth = code.depth_finder(line_no)#find depth
        start_line = line_no#initail line of function
        end_line = code.next_braket(line_no)#final line of function
        
        #The initial spaces of the string are removed for better calculations.      
        s = code.remove_space(line_no)#a space is created between the parentheses so that they are recognized as an independent element in the list
        line = s.replace("(", " ( ").replace(")", " ) ")#elements separated by space become independent Example: eat(Food food, int c) -> eat ( Food food, int c )
        line = line.split(" ")
        
        
        if(line[1] == class_name):
            Type = "constructor"
            name = line[1]
            input_type = []
            input_name = []
            p_index = line.index(')')
            for i in range(3, p_index):
                if(i %2 == 0):
                    input_name.append(line[i])
                else:
                    input_type.append(line[i])
                    
        else:
            Type = line[1]
            name = line[2]
            input_type = []
            input_name = []
            p_index = line.index(')')
            for i in range(4, p_index):
                if(i %2 == 0):
                    input_type.append(line[i])
                else:
                    input_name.append(line[i])
                    
        field_type = []
        field_name = []
        field_defined = []
        for counter in range(start_line+1, end_line):      
            if(code.field_confirm(counter)):
                field = code.get_field(counter)
                field_type.append(field[0])
                field_name.append(field[1])
                field_defined.append(field[2])
            
        return(def_depth, start_line, end_line, Type, name, input_type, input_name, field_type, field_name, field_defined)
```

This array is as follows:
```
return(def_depth, start_line, end_line, Type, name, input_type, input_name, field_type, field_name, field_defined)
```
It returns all the information we need that are in a class as an array.
```
    def extract_class(code, line_no):
        def_depth = code.depth_finder(line_no)#find depth
        start_line = line_no#initail line of function
        end_line = code.next_braket(line_no)#final line of function
        
        s = code.remove_space(line_no)#a space is created between the parentheses so that they are recognized as an independent element in the list
        line = s.replace("(", " ( ").replace(")", " ) ")#elements separated by space become independent Example: eat(Food food, int c) -> eat ( Food food, int c )
        line = line.split(" ")
        
        name = line[1]
        parents =[]
        fields = []
        functions = []
        open_arantes_index = line.index("(")
        close_arantes_index = line.index(")")
        
        for counter in range(open_arantes_index+1, close_arantes_index):
            parents.append(line[counter])
            
        for counter in range(start_line+1, end_line):  
            if(code.field_confirm(counter)):
                fields.append(code.get_field(counter))
                
            if(code.def_confirm(counter)):
                functions.append(code.extract_def(counter, name))
                
        return(def_depth, start_line, end_line, name, parents, fields, functions)
```
This array is as follows:
The element of the function that you saw above is the same as the previous extraction function that we saw earlier
```
return(def_depth, start_line, end_line, name, parents, fields, functions)
```
According to the previous functions, it identifies the scopes and extracts them
```
    def extract_scope(code, line_no):
        resault = ""
        if(code.scope_confirm(line_no)[0]):
            scope = code.scope_confirm(line_no)[1]
            scope2 = code.scope_confirm(line_no)[1][0]
            if(scope == 'class'):
                resault = (scope, code.extract_class(line_no))
            if(scope == 'method'):
                class_name = code.prev_class_name(line_no)
                resault = (scope, code.extract_def(line_no, class_name))
            if(scope2 == 'condition'):
                resault = (scope, line_no+1)
            if(scope2 == 'loop'):
                resault = (scope, line_no+1)
                
            return(resault)
        else:
            return False
```

### Semanticـanalyzer.py

We call the required libraries and classes.
```
from Read import Read_code
import re
```

We use hash table to store information. This class includes insert and lookup functions to communicate with the hash table. Also, a get function is written to get all the records.
```
class Hash_Table:
    def __init__(table, record):
        table.record = record
        
    
    def insert(table, idefNmae, attributes):
        table.record.append([idefNmae, attributes])            
            
        
    def lookout(table, ID):
        return(table.record[ID])
        
        
    def get_table(table):
        return(table.record)
```

The constructor function prints the initial and starting lines of the program. This action is performed during the construction of the object.
```
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
```

It parses the program line by line and if it finds a scope, it stores it in the hash table.

```
    def insert(program):
        HT = Hash_Table([])
        for Line_counter in range(0, program.numberOfLines):
            LINE = program.code.get_line(Line_counter)
            scope = program.code.extract_scope(Line_counter)
            if(scope != False):
                HT.insert(scope[0], scope[1])
            
        table = HT.get_table()
        return(table)
```

It examines the scopes and generates strings for them. Finally, it puts these strings in an array and is ready to print
```
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
```
Gets the information from the get function and prints them
```
    def toString(program):
        string = program.get_value()
        for counter in string:
            print(string[string.index(counter)])
```


With this script, you can read the code related to the program
```
f = open("testcase/test.txt", "r")
text = f.readlines()
```
We build the desired object according to the code
```
c1 = Sematic_analyzer(text, [])
```
We do the conversion to string

```
c1.toString()
```
