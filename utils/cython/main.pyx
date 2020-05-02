from datetime import datetime

def actions(str action_list):
    cdef list actions = []
    for log in action_list:
        if datetime.utcfromtimestamp(log.created_utc).month == datetime.now().month:
            actions.append(log.action)
        else:
            break
