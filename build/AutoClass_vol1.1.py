from tkinter import *
import networkx as nx

def SEDegreePlan(G):
    """initializing graph"""
    # hardcoding all nodes and edges
    G.add_nodes_from(
        ['ECS1100', 'CS1200', 'CS1436', 'CS1337', 'CS2336', 'SE3340', 'MATH2312', 'MATH2413', 'MATH2414', 'CS2305',
         'SE3306', 'SE3345', 'PHYS2425', 'PHYS2426', 'MATH2418', 'SE3341', 'SE3376', 'SE4348', 'SE3354', 'ECS3390',
         'RHET1302', 'GOVT2305', 'GOVT2306', 'SE4347', 'SE4381', 'SE4352', 'SE3162', 'ECS3361', 'SE4351', 'SE4367',
         'SE4485', 'Core1-x3xx', 'Core2-x3xx', 'history1-x3xx', 'history2-x3xx'])
    G.add_edges_from(
        [('CS1436', 'CS1337'), ('CS1337', 'CS2336'), ('CS1337', 'SE3340'), ('MATH2312', 'CS2305'), ('CS2305', 'SE3306'),
         ('CS2305', 'SE3340'), ('CS2305', 'SE3341'), ('CS2305', 'SE3345'), ('CS2305', 'SE3354'), ('CS2336', 'SE3345'),
         ('CS2336', 'SE3376'), ('CS2336', 'SE3354'), ('SE3306', 'SE4352'), ('SE3306', 'SE4351'), ("SE3306", 'SE4367'),
         ('MATH2413', 'PHYS2425'), ('MATH2413', 'MATH2418'), ('MATH2414', 'PHYS2426'), ('PHYS2425', 'PHYS2426'),
         ('SE3340', 'SE4348'), ('SE3345', 'SE4348'), ('SE3345', 'SE4347'), ('SE3376', 'SE4348'), ('SE3354', 'SE4381'),
         ('SE3354', 'SE4352'), ('SE3354', 'SE4351'), ('SE3354', 'SE4367'), ('RHET1302', 'ECS3390'),
         ('SE4381', 'SE4485'),
         ('SE4352', 'SE4485'), ('SE4351', 'SE4485'), ('SE4367', 'SE4485')])

def SEGuidedElectives(G, domain):
    """add more nodes and edges corresponding to domain chosen"""
    if domain == 'Networks':
        G.add_nodes_from(['CS4390', 'CS4393', 'CS4396'])
        G.add_edges_from([('SE3345', 'CS4390'), ('SE4348', 'CS4393'), ('CS4390', 'CS4396')])
    if domain == 'Information Assurance':
        G.add_nodes_from(['CS4389', 'CS4393', 'CS4398'])
        G.add_edges_from([('SE4347', 'CS4389'), ('SE4348', 'CS4393'), ('SE4348', 'CS4398'), ('CS4390', 'CS4398')])
    if domain == 'Embedded Systems':
        G.add_nodes_from(['CS4441', 'CS4397'])
        G.add_edges_from([('SE3340', 'CS4441'), ('PHYS2426', 'CS4441'), ('SE4348', 'CS4397')])
    if domain == 'Computer Imaging':
        G.add_nodes_from(['CS4361', 'CS4391', 'CS4392'])
        G.add_edges_from([('MATH2418', 'CS4361'), ('CS2336', 'CS4361'), ('SE3345', 'CS4361'), ('SE3345', 'CS4391'),
                          ('MATH2418', 'CS4392'), ('SE3345', 'CS4392')])
    if domain == 'Artificial Intelligence and Cognitive Modeling':
        G.add_nodes_from(['CS4314', 'CS4315', 'CS4365', 'CS4375', 'CS4395'])
        G.add_nodes_from(['CGS4313', 'CGS3342'])
        G.add_edges_from(
            [('CGS3342', 'CGS4313'), ('CGS3342', 'CGS4313'), ('MATH2418', 'CGS4313'), ('SE3341', 'CGS4313'),
             ('CGS4313', 'CS4314'), ('CGS4313', 'CS4315'), ('SE3345', 'CS4365'), ('SE3341', 'CS4375'),
             ('SE3345', 'CS4375'), ('SE3341', 'CS4395'), ('SE3345', 'CS4395')])
    if domain == 'Human-Computer Interaction':
        G.add_nodes_from(['CS4352', 'CS4353', 'CS4361'])
        G.add_edges_from([('MATH2418', 'CS4361'), ('CS2336', 'CS4361'), ('SE335', 'CS4361')])

def SEProject(s1, s2):
    """SE4485 is available after 2 courses out of [4381, 4352, 4351, 4367] are taken
    s1: classes taken, s2: classes you can take"""
    counter = 0
    for n in s1:
        if n in ['SE4381', 'SE4352', 'SE4351', 'SE4367']:
            counter += 1
            # if 2 of those classes above are taken, add SE4485 into set
            if counter == 2:
                s2.add('SE4485')
                break

def totalCreditHours(S):
    """Return the total number of credit hours taken"""
    creditsHour = 0
    for cls in S:
        # the third digit from end is the number of credit hours of the classes
        creditsHour += int(cls[-3])
    return int(creditsHour)

def yearClassification(hrs):
    """Return year classification based on number of credits taken"""

    # the number of credit hours determines classification of students
    classification_of_student = ''
    if hrs < 30:  # those who have completed fewer than 30 hours is Freshman
        classification_of_student = 'Freshman'
    elif hrs < 54:  # those who have completed 30-53 hours is Sophomore
        classification_of_student = 'Sophomore'
    elif hrs < 90:  # those who have completed 54-89 hours is Junior
        classification_of_student = 'Junior'
    else:  # those who have completed 90  or more hours is Senior
        classification_of_student = 'Senior'
    return classification_of_student

# this method is really restricted to use. this requires some changes
def classificationCut(s1, s2):
    """Based on classification of the student, this method cuts some classes
    s1: classes taken, s2: classes you can take"""
    cls = yearClassification(totalCreditHours(s1))
    if cls == 'Freshman' or cls == 'Sophomore':
        # Freshman and Sophomore can't take ECS3361 or ECS3390
        s2.remove('ECS3361')
        if 'ECS3390' in s2:
            s2.remove('ECS3390')

def removePrereq(S, G):
    """Remove pre-req(s) of classes taken from list
    S: set of classes taken
    G: graph
    Return pre-req of classes"""
    removing = set()
    for n in S:
        for m in G.predecessors(n):
            removing.add(m)
    return removing

def graphMain(classes, domainName):
    """main of graph. print out classes you can take"""
    G = nx.DiGraph()
    SEDegreePlan(G)
    SEGuidedElectives(G, domainName)

    # get successor nodes and put them in a set
    # eliminate classes which have been taken

    duplicated_class_you_can_take = []
    for n in classes:
        for m in list(G.successors(n)):
            # not included classes taken
            if m not in classes:
                duplicated_class_you_can_take.append(m)

    # convert list object to set object to eliminate duplicated classes
    class_you_can_take = set(duplicated_class_you_can_take)
    # make an empty set to hold classes that didn't complete pre-req
    S = set()
    for n in class_you_can_take:
        # check each node's predecessors whether all predecessors have been taken
        for m in list(G.predecessors(n)):
            # if pre-req wasn't completed yet, add it into set
            if m not in classes:
                S.add(n)

    # remove classes that didn't meet requirements from main set, class_you_can_take
    class_you_can_take -= S

    # add classes whose in-degree is 0 (either isolated or nodes that has no edges coming inward)
    for n in G.nodes:
        if n not in classes and G.in_degree(n) == 0:
            class_you_can_take.add(n)

    # add SE4485 if condition are met
    # SEProject(classes, class_you_can_take)

    # In the class_you_can_take shouldn't contain any pre-req courses of classes taken
    for n in removePrereq(classes, G):
        if n in class_you_can_take:
            class_you_can_take.remove(n)

    # however, some classes such as ECS3390 and ECS3361 are restricted for freshman or sophomore
    classificationCut(classes, class_you_can_take)

    message1 = totalCreditHours(classes)
    message2 = yearClassification(totalCreditHours(classes))
    message3 = domainName
    message4 = class_you_can_take
    return message1, message2, message3, message4

def newWindow():
    """this method add classes selected/taken into a list"""
    child = Toplevel(master)
    # corresponding S1 to S2
    S1 = [varECS1100, varCS1200, varCS1436, varCS1337, varMATH2413, varMATH2414, varPHYS2425, varPHYS2426,
          varMATH2312, varCS2305, varCS2336, varSE3340, varSE3306, varSE3341, varSE3345, varSE3376,
          varMATH2418, varSE4348, varSE3354, varECS3390, varSE4347, varSE3162, varECS3361, varSE4485,
          varSE4381, varSE4352, varSE4351, varSE4367, varRHET1302, varGOVT2305, varGOVT2306]
    S2 = ['ECS1100', 'CS1200', 'CS1436', 'CS1337', 'MATH2413', 'MATH2414', 'PHYS2425', 'PHYS2426',
          'MATH2312', 'CS2305', 'CS2336', 'SE3340', 'SE3306', 'SE3341', 'SE3345', 'SE3376',
          'MATH2418', 'SE4348', 'SE3354', 'ECS3390', 'SE4347', 'SE3162', 'ECS3361', 'SE4485',
          'SE4381', 'SE4352', 'SE4351', 'SE4367', 'RHET1302', 'GOVT2305', 'GOVT2306']
    # classes holds classes which have checked, meaning have been taken
    classes = []
    i = 0
    # when the variable of a class is 1, meaning selected, add the class to a list
    for n in S1:
        if n.get() == 1:
          classes.append(S2[i])
        i += 1

    S1_core1 = [varAHST1303, varAHST1304, varAHST2331, varARTS1301,
                varDANC1310, varDRAM1310, varFILM2332, varMUSI1306]
    S1_core2 = [varAMS2300, varAMS2341, varHUMA1301, varLIT2331, varPHIL1301, varPHIL2316, varPHIL2317]
    S1_history = [varHIST1301, varHIST1302, varHIST2301, varHIST2330, varHIST2332]

    for n in S1_core1:
        if n.get() == 1:
            # the reason x3xx is take the third from last character to calculate credit hours
            classes.append('Core1-x3xx')

    for n in S1_core2:
        if n.get() == 1:
            # the reason x3xx is take the third from last character to calculate credit hours
            classes.append('Core2-x3xx')

    i = 0
    for n in S1_history:
        if i == 0:
            if n.get() == 1:
                i += 1
                classes.append('history1-x3xx')
        if i == 1:
            if n.get() == 1:
                classes.append('history2-x3xx')

    # add classes to a list for networks
    if varDomain.get() == 'Networks':
        S1_NW = [varCS4390, varCS4393, varCS4396]
        S2_NW = ['CS4390', 'CS4393', 'CS4396']
        i = 0
        # when the variable of a class is 1, meaning selected, add the class to a list
        for n in S1_NW:
            if n.get() == 1:
                classes.append(S2_NW[i])
            i += 1
    # add classes to a list for information assurance
    if varDomain.get() == 'Information Assurance':
        S1_IA = [varCS4389, varCS4393, varCS4398]
        S2_IA = ['CS4389', 'CS4393', 'CS4398']
        i = 0
        # when the variable of a class is 1, meaning selected, add the class to a list
        for n in S1_IA:
            if n.get() == 1:
                classes.append(S2_IA[i])
            i += 1
    # add classes to a list for Embedded Systems
    if varDomain.get() == 'Embedded Systems':
        S1_ES = [varCS4441, varCS4397]
        S2_ES = [['CS4441', 'CS4397']]
        i = 0
        # when the variable of a class is 1, meaning selected, add the class to a list
        for n in S1_ES:
            if n.get() == 1:
                classes.append(S2_ES[i])
            i += 1

    if varDomain.get() == 'Artificial Intelligence and Cognitive Modeling':
        S1_AI = [varCS4314, varCS4315, varCS4365, varCS4375, vraCS4395, varCGS4313, varCGS3342]
        S2_AI = ['CS4314', 'CS4315', 'CS4365', 'CS4375', 'CS4395', 'CGS4313', 'CGS3342']
        i = 0
        # when the variable of a class is 1, meaning selected, add the class to a list
        for n in S1_AI:
            if n.get() == 1:
                classes.append(S2_AI[i])
            i += 1
    # add classes to a list for Human computer interaction
    if varDomain.get() == 'Human-Computer Interaction':
        S1_HCI = [varCS4352, varCS4353, varCS4361]
        S2_HCI = ['CS4352', 'CS4353', 'CS4361']
        i = 0
        # when the variable of a class is 1, meaning selected, add the class to a list
        for n in S1_HCI:
            if n.get() == 1:
                classes.append(S2_HCI[i])
            i += 1

    message1, message2, message3, message4 = graphMain(classes, varDomain.get())
    msg1 = 'Total credit hours: ' + str(message1)
    msg2 = 'Classification: ' + message2
    msg3 = 'Domain: ' + message3
    msg4 = 'Classes you can take: ' + str(message4)
    Label(child, text=msg1).grid(row=0, sticky=W)
    Label(child, text=msg2).grid(row=1, sticky=W)
    Label(child, text=msg3).grid(row=2, sticky=W)
    Label(child, text=msg4).grid(row=3, sticky=W)

def addElectives():
    """By pushing this button, it will add classes corresponding to the chosen domain on UI"""

    if varDomain.get() == 'Networks':
        # G.add_nodes_from(['CS4390', 'CS4393', 'CS4396'])
        Checkbutton(master, text='CS4390', variable=varCS4390).grid(row=19, column=0)
        Checkbutton(master, text='CS4393', variable=varCS4393).grid(row=19, column=1)
        Checkbutton(master, text='CS4396', variable=varCS4396).grid(row=19, column=2)

    if varDomain.get() == 'Information Assurance':
        # G.add_nodes_from(['CS4389', 'CS4393', 'CS4398'])
        Checkbutton(master, text='CS4389', variable=varCS4389).grid(row=19, column=0)
        Checkbutton(master, text='CS4393', variable=varCS4393).grid(row=19, column=1)
        Checkbutton(master, text='CS4398', variable=varCS4398).grid(row=19, column=2)
    if varDomain.get() == 'Embedded Systems':
        # G.add_nodes_from(['CS4441', 'CS4397'])
        Checkbutton(master, text='CS4441', variable=varCS4441).grid(row=19, column=0)
        Checkbutton(master, text='CS4397', variable=varCS4397).grid(row=19, column=1)
    if varDomain.get() == 'Computer Imaging':
        # G.add_nodes_from(['CS4361', 'CS4391', 'CS4392'])
        Checkbutton(master, text='CS4361', variable=varCS4361).grid(row=19, column=0)
        Checkbutton(master, text='CS4391', variable=varCS4391).grid(row=19, column=1)
        Checkbutton(master, text='CS4392', variable=varCS4392).grid(row=19, column=2)
    if varDomain.get() == 'Artificial Intelligence and Cognitive Modeling':
        # G.add_nodes_from(['CS4314', 'CS4315', 'CS4365', 'CS4375', 'CS4395'])
        # G.add_nodes_from(['CGS4313', 'CGS3342'])
        Checkbutton(master, text='CS4314', variable=varCS4314).grid(row=19, column=0)
        Checkbutton(master, text='CS4315', variable=varCS4315).grid(row=19, column=1)
        Checkbutton(master, text='CS4365', variable=varCS4365).grid(row=19, column=2)
        Checkbutton(master, text='CS4375', variable=varCS4375).grid(row=19, column=3)
        Checkbutton(master, text='CS4395', variable=vraCS4395).grid(row=19, column=4)

        Checkbutton(master, text='CGS4313', variable=varCGS4313).grid(row=20, column=0)
        Checkbutton(master, text='CGS3342', variable=varCGS3342).grid(row=20, column=0)
    if varDomain.get() == 'Human-Computer Interaction':
        # G.add_nodes_from(['CS4352', 'CS4353', 'CS4361'])
        Checkbutton(master, text='CS4352', variable=varCS4352).grid(row=19, column=0)
        Checkbutton(master, text='CS4353', variable=varCS4353).grid(row=19, column=1)
        Checkbutton(master, text='CS4361', variable=varCS4361).grid(row=19, column=2)


if __name__ == '__main__':
    master = Tk()
    master.title('Auto Class Recommender')

    # initialize all guided electives
    varCS4390, varCS4393, varCS4396 = IntVar(), IntVar(), IntVar()
    varCS4389, varCS4393, varCS4398 = IntVar(), IntVar(), IntVar()
    varCS4441, varCS4397, = IntVar(), IntVar()
    varCS4361, varCS4391, varCS4392 = IntVar(), IntVar(), IntVar()
    varCS4314, varCS4315, varCS4365, varCS4375 = IntVar(), IntVar(), IntVar(), IntVar()
    vraCS4395, varCGS4313, varCGS3342 = IntVar(), IntVar(), IntVar()
    varCS4352, varCS4353, varCS4361 = IntVar(), IntVar(), IntVar()

    # option menu returns string
    varDomain = StringVar(master)
    varDomain.set('Select one domain')  # default value

    guided_electives_options = ['Networks', 'Information Assurance', 'Embedded Systems', 'Computer Imaging',
                                'Artificial Intelligence and Cognitive Modeling', 'Human-Computer Interaction',
                                'Undecided']

    option = OptionMenu(master, varDomain, *guided_electives_options)
    option.grid(row=0, sticky=W)
    button = Button(master, text='Add guided electives to the list', command=addElectives)
    button.grid(row=0, column=1)

    Label(master, text="Choose classes you have taken").grid(row=1, sticky=W)

    Label(master, text="Core classes 1").grid(row=2, sticky=W)
    varAHST1303, varAHST1304, varAHST2331, varARTS1301, varDANC1310 = IntVar(), IntVar(), IntVar(), IntVar(), IntVar()
    Checkbutton(master, text='AHST1303', variable=varAHST1303).grid(row=3, column=0)
    Checkbutton(master, text='AHST1304', variable=varAHST1304).grid(row=3, column=1)
    Checkbutton(master, text='AHST2331', variable=varAHST2331).grid(row=3, column=2)
    Checkbutton(master, text='ARTS1301', variable=varARTS1301).grid(row=3, column=3)
    Checkbutton(master, text='DANC1310', variable=varDANC1310).grid(row=3, column=4)

    varDRAM1310, varFILM2332, varMUSI1306 = IntVar(), IntVar(), IntVar()
    Checkbutton(master, text='DRAM1310', variable=varDRAM1310).grid(row=4, column=0)
    Checkbutton(master, text='FILM2332', variable=varFILM2332).grid(row=4, column=1)
    Checkbutton(master, text='MUSI1306', variable=varMUSI1306).grid(row=4, column=2)

    Label(master, text="Core classes 2").grid(row=5, sticky=W)
    varAMS2300, varAMS2341, varHUMA1301, varLIT2331, varPHIL1301 = IntVar(), IntVar(), IntVar(), IntVar(), IntVar()
    Checkbutton(master, text='AMS2300', variable=varAMS2300).grid(row=6, column=0)
    Checkbutton(master, text='AMS2341', variable=varAMS2341).grid(row=6, column=1)
    Checkbutton(master, text='HUMA1301', variable=varHUMA1301).grid(row=6, column=2)
    Checkbutton(master, text='LIT2331', variable=varLIT2331).grid(row=6, column=3)
    Checkbutton(master, text='PHIL1301', variable=varPHIL1301).grid(row=6, column=4)

    varPHIL2316, varPHIL2317 = IntVar(), IntVar()
    Checkbutton(master, text='PHIL2316', variable=varPHIL2316).grid(row=7, column=0)
    Checkbutton(master, text='PHIL2317', variable=varPHIL2317).grid(row=7, column=1)

    Label(master, text="History").grid(row=8, sticky=W)
    varHIST1301, varHIST1302, varHIST2301, varHIST2330, varHIST2332 = IntVar(), IntVar(), IntVar(), IntVar(), IntVar()
    Checkbutton(master, text='HIST1301', variable=varHIST1301).grid(row=9, column=0)
    Checkbutton(master, text='HIST1302', variable=varHIST1302).grid(row=9, column=1)
    Checkbutton(master, text='HIST2301', variable=varHIST2301).grid(row=9, column=2)
    Checkbutton(master, text='HIST2330', variable=varHIST2330).grid(row=9, column=3)
    Checkbutton(master, text='HIST2332', variable=varHIST2332).grid(row=9, column=4)

    Label(master, text='Other cores').grid(row=10, sticky=W)
    varRHET1302, varGOVT2305, varGOVT2306 = IntVar(), IntVar(), IntVar()
    Checkbutton(master, text='RHET1302', variable=varRHET1302).grid(row=11, column=0)
    Checkbutton(master, text='GOVT2305', variable=varGOVT2305).grid(row=11, column=1)
    Checkbutton(master, text='GOVT2306', variable=varGOVT2306).grid(row=11, column=2)
    # Checkbutton returns int variable: 1 as selected and 0 as non-selected
    # this int variables are used in var_state to add classes into a list
    Label(master, text="Major classes").grid(row=12, sticky=W)
    varECS1100, varCS1200, varCS1436, varCS1337, varCS2305 = IntVar(), IntVar(), IntVar(), IntVar(), IntVar()
    Checkbutton(master, text='CS1100', variable=varECS1100).grid(row=13, column=0)
    Checkbutton(master, text='CS1200', variable=varCS1200).grid(row=13, column=1)
    Checkbutton(master, text='CS1436', variable=varCS1436).grid(row=13, column=2)
    Checkbutton(master, text='CS1337', variable=varCS1337).grid(row=13, column=3)
    Checkbutton(master, text='CS2305', variable=varCS2305).grid(row=13, column=4)

    varMATH2312, varMATH2413, varMATH2414, varPHYS2425, varPHYS2426= IntVar(), IntVar(), IntVar(), IntVar(), IntVar()
    Checkbutton(master, text='MATH2312', variable=varMATH2312).grid(row=14, column=0)
    Checkbutton(master, text='MATH2413', variable=varMATH2413).grid(row=14, column=1)
    Checkbutton(master, text='MATH2414', variable=varMATH2414).grid(row=14, column=2)
    Checkbutton(master, text='PHYS2425', variable=varPHYS2425).grid(row=14, column=3)
    Checkbutton(master, text='PHYS2426', variable=varPHYS2426).grid(row=14, column=4)

    varCS2336, varSE3340, varSE3306, varSE3341, varSE3345 = IntVar(), IntVar(), IntVar(), IntVar(), IntVar()
    Checkbutton(master, text='CS2336', variable=varCS2336).grid(row=15, column=0)
    Checkbutton(master, text='SE3340', variable=varSE3340).grid(row=15, column=1)
    Checkbutton(master, text='SE3306', variable=varSE3306).grid(row=15, column=2)
    Checkbutton(master, text='SE3341', variable=varSE3341).grid(row=15, column=3)
    Checkbutton(master, text='SE3345', variable=varSE3345).grid(row=15, column=4)

    varSE3376, varMATH2418, varSE4348, varSE3354, varECS3390 = IntVar(), IntVar(), IntVar(), IntVar(), IntVar()
    Checkbutton(master, text='SE3376', variable=varSE3376).grid(row=16, column=0)
    Checkbutton(master, text='MATH2418', variable=varMATH2418).grid(row=16, column=1)
    Checkbutton(master, text='SE4348', variable=varSE4348).grid(row=16, column=2)
    Checkbutton(master, text='SE3354', variable=varSE3354).grid(row=16, column=3)
    Checkbutton(master, text='ECS3390', variable=varECS3390).grid(row=16, column=4)

    varSE4347, varSE3162, varECS3361, varSE4485, varSE4381 = IntVar(), IntVar(), IntVar(), IntVar(), IntVar()
    Checkbutton(master, text='SE4347', variable=varSE4347).grid(row=17, column=0)
    Checkbutton(master, text='SE3162', variable=varSE3162).grid(row=17, column=1)
    Checkbutton(master, text='ECS3361', variable=varECS3361).grid(row=17, column=2)
    Checkbutton(master, text='SE4485', variable=varSE4485).grid(row=17, column=3)
    Checkbutton(master, text='SE4381', variable=varSE4381).grid(row=17, column=4)

    varSE4352, varSE4351, varSE4367 = IntVar(), IntVar(), IntVar()
    Checkbutton(master, text='SE4352', variable=varSE4352).grid(row=18, column=0)
    Checkbutton(master, text='SE4351', variable=varSE4351).grid(row=18, column=1)
    Checkbutton(master, text='SE4367', variable=varSE4367).grid(row=18, column=2)

    Button(master, text='Quit', command=master.quit).grid(row=21, column=0)
    Button(master, text='Show', command=newWindow).grid(row=21, column=1)

    mainloop()
