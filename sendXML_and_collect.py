%run NeosClient.py xmlfname # TODO need to get(xmlfname)

try:
    msg = neos.getFinalResults(jobNumber, password).data
    msg=str(msg)
except Exception:
        print 'Error: sth went wrong getting Final Results'
        

# import time
# time.sleep(5) use only if necessary. this can't scale


### find segments beginning with task_active, then within each of those stringify the list of tasks. Call SQL to find task names
def getSelectedTasks():
    import re as re
    pattern = re.compile(r"task_active")
    matchediterator = pattern.finditer(msg)
    
    spanendings = []
    for match in matchediterator:
        spanendings.append(match.span()[1]) #[1] to get the span-end
    outputsegments =[]
    for i in range(len(spanendings)-1):
        startpos=spanendings[i]
        endpos=spanendings[i]+200
        outputsegments.append(msg[startpos:endpos])

    pattern = re.compile(r"\n(\d+)\s+1")
    for s in outputsegments:
        matchediterator = pattern.finditer(s)
    strTasksSelected=[]
    for match in matchediterator:
        strTasksSelected.append(int(match.group(1)))
    strfiedTasksSelected=str(strTasksSelected)
    strlength=len(strfiedTasksSelected)
    # strfiedTasksSelected[1:strlength-1] below holds task1,task2 etc by dropping off the brackets[]

    #listChosenTasks
    import pypyodbc
    connection = pypyodbc.connect('Driver={SQL Server};'
                                    'Server=!!!;' 
                                    'Database=!!!;'
                                    'uid=!!!;pwd=!!!')
    cursor = connection.cursor() 
    SQLCommand = ("SELECT [Name],[FullPacketUrl] "
    "FROM portal.Task   where	Id in (" +strfiedTasksSelected[1:strlength-1] + " )" )   #
    cursor.execute(SQLCommand) 
    tasknames = []
    tasknames.append(list(cursor.fetchone()) )

    i=0
    while tasknames[i] and i <30:
        try:
            tasknames.append(list(cursor.fetchone()) )
            i = i + 1
        except Exception:
            break
    for i in tasknames:
        print str(i)+"/n"

getSelectedTasks()
