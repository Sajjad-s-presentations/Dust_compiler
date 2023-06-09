class Read_code:
    def __init__(code, body):
        print("constructor is called!")
        code.body = body
        
    def __str__(code):
        return f"{code.body}"
    
    def get_line(code, line_no):
        return code.body[line_no]
    
    def remove_space(code, line_no):
        space_counter = 0
        index = 0
        new_str = code.body[line_no].lstrip()
        #print("Line ", line_no, " is: ", code.body[line_no])
        return new_str
        
    def line_counter(code):
        counter = 0
        for line in code.body:
            counter += 1
        return counter
    
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
    
    
    def extract_global_def(code, line_no, class_name):
        print(class_name)
        def_depth = code.depth_finder(line_no)#find depth
        start_line = line_no#initail line of function
        end_line = code.next_braket(line_no)#final line of function
        
        #The initial spaces of the string are removed for better calculations.      
        s = code.remove_space(line_no)#a space is created between the parentheses so that they are recognized as an independent element in the list
        line = s.replace("(", " ( ").replace(")", " ) ")#elements separated by space become independent Example: eat(Food food, int c) -> eat ( Food food, int c )
        line = line.split(" ")
        
        
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
            	l = (line_no+1,)
            	scope = scope + l
            	resault = (scope[0], scope)
            if(scope2 == 'loop'):
            	l = (line_no+1,)
            	scope = scope + l
            	resault = (scope[0], scope)
                
            return(resault)
        else:
            return False
        
