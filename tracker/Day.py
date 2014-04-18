from Flow Logic.py import Flowchart

class Day(object):

    def __init__(self, date, flow_doc_fn):
        self.date = date #This is totally optional, but might be useful
        self.patient_list = [] # This will be list of patient objects.

        self.flow = Flowchart(flow_doc_fn)

    def add_patient(self, name, DOB, incStep):
        
        p = Patient(name, DOB, incStep)
        self.patient_list.append(p)

    def get_next_step(self, name, DOB, outcome):
        #outcome in this case is a list of tuples
        p = self._fetch_patient(name, DOB)
        if p == False:
            return False, False
        else:
            for t in outcome:
                label = t[0]
                result = t[1]
                p.addOutcome(label, result)
                
            next_step, flag = self.flow.getNextStep(p)
            p.setStep(next_step)
            return next_step, flag

    def get_current_step(self, name, DOB):
        p = self._fetch_patient(name, DOB)
        if p == False:
            return False
        else:
            return p.step

    def get_form_data(self):
        # Returns the form data dictionary.
        f_d = self.flow.getFormData()
        return f_d

    def get_step_order(self):
        s_o = self.flow.getStepOrder()
        return s_o

    def _fetch_patient(self, name, DOB):
        '''
        Returns the patient object corresponding to the name passed in
        if it exists, and if none exist then it returns False.
        '''
        for p in self.patient_list:
            if p.name == name and p.DOB == DOB:
                return p
        return False
        



class Patient(object):

    def __init__(self, name, DOB, step):
        self.name = name
        self.DOB = DOB
        self.step = step
        '''
        Create a list of the step names done so far.
        Create an empty dict to use as this patient's outcome data. The
        dictionary keys are input labels, and the values are the data type
        which that label needs to use.
        I'm not sure how this might relate to Professor Gillman's history
        setup. Hopefully this could easily be changed to fit that.
        '''
        self.step_history = []
        self.outcome = dict()
        #self.history = Prof. Gillman's history thingymabobberoono.

    def setStep(self, new_step):

        # Add the step that the patient was on, to the step history.
        self.step_history.append(self.step.name)

        # Change the class variable to the new step object.
        self.step = new_step

    def addOutcome(self, label, result):
        # Maybe add this to Prof. Gillman's history thingy here.
        self.outcome[label] = result
