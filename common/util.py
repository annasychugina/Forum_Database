def getSqlVariable(var):
    if var == None:
        return "NULL"
    else:
        return "'%s'" % var
