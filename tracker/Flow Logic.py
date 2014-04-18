'''
Let the outcome variable passed into getNextStep() be a dictionary, with keys of
strings naming variables, and values with the appropriate outcome value. The
outcome dictionary passed in must contain all of the form_data labels which
thus far have values, so that the conditions may be properly checked.

Let the history variable passed in be any data structure which can hold strings
naming all of the steps that have been done so far, preferably ordered but for
my uses that's not necessary. For now I assume it's a list.

Self.flow_dict is a dictionary with the entered step names as string keys, and
a list of tuples as a value, with t[0] containing a list of conditions to be met,
and t[1] the order to carry out if those conditions are met.

self.form_data is a dictionary constructed at the start of the day, intended
to be transferred to the GUI's memory. The keys of the dictionary are
strings of step names, and the values are lists of tuples, with t[0]
being a string identifying the input label, and t[1] being a string
identifying the python data type of input expected for that label.

Self.step_order is a list of the steps, in the order given in the file.

getNextStep() returns a tuple of two strings: the step name, and the flag. The
flag will most often be a null string.
'''

# Took out the Step class. Form data will be given to GUI at the start of each Day.
# Step name strings and flags will be passed as a return tuple from getNextStep().
'''
class Step(object):

    def __init__(self, name, flag, form_data): 
        self.name = name
        self.flag = flag
        # Form data is a list of tuples
        self.form_data = form_data

    def setFlag(self, flag):
        self.flag = flag

    def set_Form(self, form_data):
        self.form_data = form_data
'''

class Flowchart(object):

    def __init__(self, flowchart_filename):
        self.flow_dict = {} # Dictionary handling conditions and orders
        self.form_data = {} # Dictionary handling input fields for form data
        self.step_order = [] # List of the steps, in order
        with open(flowchart_filename) as f:
            data = f.read().split('\n') # list of line strings
        self._parseFile(data)

    def getFormData(self):
        '''
        Get the form data dictionary for the day. 
        '''
        return self.form_data

    def get_StepOrder(self):
        return self.step_order

    def getNextStep(self, Patient): #Patient here is a patient object
        '''
        Returns the next step's name, and a flag string.
        '''
        flag = ''
        current_step = Patient.step # This should be a string.
        outcome = Patient.outcome # This should be a dictionary.
        step_history = Patient.step_history # This should be a list.

        
        for t in self.flow_dict.get(current_step, []): # for each if statement tuple
          condition_list = t[0]
          order = t[1]

          c_met = 0
          for c in condition_list: # Check each condition.
              var_name = c[0]
              operator = c[1]
              value = c[2]

              if operator == 'error':
                  break
                  
              elif operator == '>':
                  if not var_name in outcome:
                      break
                  else:
                      if outcome[var_name] > value:
                          c_met += 1

              elif operator == '<':
                  if not var_name in outcome:
                      break
                  else:
                      if outcome[var_name] < value:
                          c_met += 1

              elif operator == '==':
                  if not var_name in outcome:
                      break
                  else:
                      if outcome[var_name] == value:
                          c_met += 1

              elif operator == 'bool':
                  if not var_name in outcome:
                      break
                  else:
                      if outcome[var_name] == value:
                          c_met += 1

              elif operator == 'not done':
                  if not var_name in history:
                      c_met += 1

              elif operator == 'done':
                  if var_name in history:
                      c_met += 1
                      

          if c_met == len(condition_list): # If all conditions met, execute order.
              next_step, fl = self._interpret_order(order)
              if next_step == '' and fl == '':
                  #This would indicate an error in the parsing, or the data inputted.
                  pass
              elif fl != '':
                  flag = fl
              elif next_step != '':
                  return next_step, flag

        # If none of the if statement tuples are met. Could mean that there are no
        # more steps, or it could mean there was an error.

        return current_step, flag
            

    def _interpret_order(self, order): #order is a string
        next_step = ''
        flag = ''
        if order.startswith("GoTo"):
            next_step = order[5:]
        elif order.startswith("Flag"):
            flag = order[5:]
        else: #FREAK OUT
            pass
        return next_step, flag




    def _parseFile(self, data):
        current_step = ''
        for line in data:
            if line == '':
                continue
            elif line.startswith("step: "):
                current_step = line[6:]
                self.step_order.append(current_step) #Build ordered list of steps.

            elif line.startswith("input: "):
                
                input_fields = line[7:]
                if input_fields != "None": 
                    while(True):
                        split_ind = input_fields.find(';')
                        if split_ind == -1:
                            ind = input_fields.find(', ')
                            label = input_fields[:ind]
                            data_type = input_fields[ind+1:]
                        
                            input_list = self.form_data.get(current_step, [])
                            t = (label, data_type)
                            input_list.append(t)
                            self.form_data[current_step] = input_list
                        
                            break
                        else:
                            ind = input_fields.find(', ', 0, split_ind)
                            label = input_fields[:ind]
                            data_type = input_fields[ind+1:split_ind]
                        
                            input_list = self.form_data.get(current_step, [])
                            t = (label, data_type)
                            input_list.append(t)
                            self.form_data[current_step] = input_list

                            input_fields = input_fields[split_ind+2:]
                        
                
            elif line.startswith("GoTo "):
                c_list = []
                order_s = line
                t = (c_list, order_s)
                
                cur_list = self.flow_dict.get(current_step, [])
                cur_list.append(t)
                self.flow_dict[current_step] = cur_list

            elif line.startswith("if "):
                c_list = []
                condition = line[3:line.find('then') - 1]
                while(True):
                    ind = condition.find(' and ')
                    if ind == -1:
                        t = self._parseCondition(condition)
                        c_list.append(t)
                        break
                    else:
                        t = self._parseCondition(condition[:ind])
                        c_list.append(t)
                        condition = condition[ind+5:]

                order_s = line[line.find('then ')+5:]

                t = (c_list, order_s)
                cur_list = self.flow_dict.get(current_step, [])
                cur_list.append(t)
                self.flow_dict[current_step] = cur_list
                
                

    def _parseCondition(self, c):
        '''
        Returns a tuple with three values: the variable name, the operator, and the value to check.
        '''
        rt = ('','error',0)

        if (' > ') in c:
            ind = c.find(' > ')
            var_name = c[:ind]
            value = float(c[ind+3:])
            rt = (var_name, '>', value)

        elif (' < ') in c:
            ind = c.find(' < ')
            var_name = c[:ind]
            value = float(c[ind+3:])
            rt = (var_name, '<', value)

        elif (' == ') in c:
            ind = c.find(' == ')
            var_name = c[:ind]
            value = float(c[ind+4:])
            rt = (var_name, '==', value)

        elif (' is ') in c:
            ind = c.find(' is ')
            var_name = c[:ind]
            value_s = c[ind+4:]
            if value_s == "True":
                value = True
                rt = (var_name, 'bool', value)
            elif value_s == "False":
                value = False
                rt = (var_name, 'bool', value)

            elif value_s == "not done":
                rt = (var_name, 'not done', 0)

            elif value_s == "done":
                rt = (var_name, 'done', 0)

            else: #This shouldn't happen with proper doc usage
                pass

        return rt


    def get_Form_Data(self, stepname):
        form = self.step_inputs.get(stepname, [])
        return form
        

    def __str__(self):
        pass # I'm supposed to make a pretty picture printout here..how?
        # This doesn't seem necessary right now.




def sample_main(step_name, outcome, history):

    current_step = Step(step_name, '', Flow.get_Form_Data(step_name) )

    next_step = Flow.getNextStep(current_step, outcome, history)
    
    flag = next_step.flag
    form_data = next_step.form_data

    print "The step passed in was:", step_name
    
    if flag != '':
        print "The flag is:", flag
        #current_patient.setFlag(flag)
    else:
        print "There is no flag."

    print "The next step is:", next_step.name
    print "And the GUI will be told to display this information: ", str(form_data)
    print "\n"


#change this to the location of the example file to run a test.
flow_doc_filename = "C:/Users/Noah/Desktop/Abortion Day Tracking/Flowchart Doc.txt"
Flow = Flowchart(flow_doc_filename)


outcome = dict()
history = []
step_name = Flow.step_order[1]
outcome["USVALUE"] = 12.5
sample_main(step_name, outcome, history)


step_name = Flow.step_order[3]
outcome["Consent"] = False
history.append(Flow.step_order[1])
sample_main(step_name, outcome, history)

step_name = Flow.step_order[7]
history.append(Flow.step_order[3])
sample_main(step_name, outcome, history)

step_name = Flow.step_order[9]
history.append(Flow.step_order[7])
sample_main(step_name, outcome, history)
