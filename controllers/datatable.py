from copy import copy
import simplejson as json
from datetime import datetime
from timer import Timer

pyFileName = "datatable.py"
URL_icon_set = URL("static","img/icons/set1") + "/"

if False:
    from gluon import *

# Shows the datable. 
# @auth.requires_login()  # Should enable this line to ensure security
def show():
    
    if request.args:
        dt_settings = datatable_data(request.args, request.vars)
    else:
        # Build a table that lists all tables
        dt_settings = datatable_data('DatabaseModel', request.vars)
    
    if dt_settings['Success']:
        response.title = f"{dt_settings['PageHeading']} ({request.application})"
        return dict(dt_settings=dt_settings)
    else:
        return dt_settings['Error']

# ----------------------------------------
# @auth.requires_login()
def delete():
    try:
        I="Starting."
        DataTableName = request.args[0]
        dt_settings = GridDefaults(DataTableName) 
        TableName = dt_settings['TableName'] 

        x = len(request.args) 
        if x > 1:
            I="Preparing delete"
            id =  request.args[1]
            Table = db[TableName]

            # It's possible that there is a common filter on the table which may need to be removed
            if not get_deep(dt_settings,'common_filter',True): Table._common_filter  = None

            RecsDeleted = db(Table.id==id).delete()
            RecsDeletedStatus = (RecsDeleted ==1)
            result = {'Success':RecsDeletedStatus, 'Deleted':RecsDeleted>0, 'Message':'%s record deleted' % (RecsDeleted)}
            response.flash = T("Success: %s." % (result['Message']))
        else:
            result = {'Success':False,'Message':'No ID was specified'}
            response.flash = T("Error: Can't delete the record because no ID was supplied.")

        return json.dumps(result)

    except Exception as e:
        return LogError(pyFileName, e, I, ReturnJson = True, FlashError = True)

# @auth.requires_login()
def DeleteAll():
    try:
        I="Starting"
        result = {}
        if request.vars:
            TableName = request.vars.TableName
            if TableName:
                db[TableName].truncate()
                # db.commit()
                result['Message'] = 'Success: All records deleted.'
                result['Success'] = True
            else:
                result['Message'] = 'Error: Tablename not supplied in the list of vars.'
                result['Success'] = False
        else:
            result['Message'] = 'Error: Tablename not identified as no argument specified.'
            result['Success'] = False

        response.flash = result['Message']
        result = json.dumps(result, indent=4, sort_keys=True, default=str)

        return result

    except Exception as e:
        return LogError(pyFileName, e, I, ReturnJson = True, FlashError = True)

# @auth.requires_login()
def add():
    return AddOrEdit(IsAdd = True)

# ----------------------------------------
# @auth.requires_login()
def edit():
    return AddOrEdit(IsAdd = False)

def AddOrEdit(IsAdd = False):  # Add or edit records by getting a form and displaying it in the datatable modal
    try:
        I="Starting."
        if not request.args:
            I="Error: No args have been supplied so the table to add or edit cannot be determined."
            LogError(pyFileName, ExtraInfo = I)
            response.flash = I
        else:
            if request.args[-1] == 'UploadFile':
                # A file associated with this form has been sent. This gets sent in a second request after the form has been initially processed.
                # It is always an update to the record because a new record has been saved on a previous call
                f = request.post_vars.file
                id = request.post_vars.id
                TableName = request.post_vars.TableName
                FieldName = request.post_vars.FieldName
                UpdateDict = {FieldName:f}
                db[TableName][id] = UpdateDict
                response.flash = 'Success: File saved successfully. Refresh the table to see it.'

            else:
                I="Initialising dt_settings."
                DataTableName = request.args[0]
                dt_settings = GridDefaults(DataTableName)
                TableName = dt_settings['TableName'] 
                DisabledFields = dt_settings['DisabledFields']

                if len(request.args) > 1:
                    id =  request.args[1]
                else:
                    id = None

                if TableName:
                    Table = db[TableName]

                    I="It's possible that there is a common filter on the table which may need to be removed"
                    if not get_deep(dt_settings,'common_filter',True): Table._common_filter = None

                    if id:
                        rows = db(Table.id==id).select()
                    else:
                        rows = None

                    I="Check if the datatable is filtered. If it is, we want to make the filter field (say UserID) readonly."
                    vars = request.post_vars
                    if vars:
                        for key in vars:
                            if key in Table.fields:
                                DisabledFields.append(f'{TableName}_{key}')

                    rec = rows[0] if rows else None

                    form = SQLFORM(Table, rec,
                                    deletable=False, 
                                    readonly=False,
                                    buttons=[''],
                                    _class="sd-form"
                                    )

                    I="Check if the datatable is filtered. If it is, we want to use the filter to set the default value."
                    if vars:
                        for key in vars:
                            if key in Table.fields:
                                form.vars[key] = vars[key]

                    if form.accepts(request):
                        I="Form has been accepted."
                        result = {}
                        if id: 
                            ResultMessage = 'Success. Record has been updated.'
                        else:
                            ResultMessage = 'Success. Record has been added.'
                            id = form.vars.id  # No id means that an insert is happening.
                        
                        rec = db(Table.id==id).select().first()
                        if not rec:
                            I='Error. The form was successfully processed but the record can no longer be found. Its possible that some filtering is hiding it.'
                            ResultMessage = I
                            LogError(pyFileName, ExtraInfo=I)
                            result['Success'] = False
                        else:
                            result['id'] = rec.id
                            rec = rec.as_dict()

                            # Get the new or updated record so it can be returned to the page for display.
                            dt_settings = datatable_data([TableName],{'id':id})
                            
                            if dt_settings:
                                result['Success'] = True
                                result['record'] = dt_settings['data'][0]
                            else:
                                I='Error: The new/updated record could not be found.'
                                result['Success'] = False

                        response.flash = ResultMessage

                        result = json.dumps(result, indent=4, sort_keys=True, default=str)
                        return result

                    elif form.errors:
                        I=StringifyFormErrors(form.errors) 
                        LogError(pyFileName, ExtraInfo=I)
                        response.flash = I
                        result = json.dumps(dict(success = False, message = form.errors))
                        return result
                    else:
                        f = XML(form)
                        result = {}
                        result['form'] = f
                        result['Success'] = False
                        result['DisabledFields'] = DisabledFields
                        result = json.dumps(result, indent=4, sort_keys=True, default=str)
                        return result

                else:
                    I='Error: No table has been specified.'
                    LogError(pyFileName, ExtraInfo=I)
                    response.flash = 'Error: No table has been specified.'
    
    except Exception as e:
        return LogError(pyFileName, e, I, ReturnJson = True, FlashError = True)

def duplicate():  # Duplicates any record give the TableName and the id of the record to be duplicated
    try:
        I="Starting."
        result = {}
        if not request.vars:
            I="Error: No vars have been supplied so the record to duplicate cannot be determined."
            LogError(pyFileName, ExtraInfo = I)
        else:
            TableName = request.vars.TableName
            id = request.vars.id
            if TableName and id:
                I="Duplicating record."
                rec = db[TableName][id]
                if rec:
                    NewRecValues = {}
                    for f in db[TableName].fields:
                        if f != 'id':
                            if db[TableName][f].type == 'string' and 'name' in f.lower():
                                NewRecValues[f] = f"{rec[f]}-copy"
                            else:
                                NewRecValues[f] = rec[f]
                    NewID = db[TableName].insert(**NewRecValues)
                    if NewID:
                        # Get the new or updated record so it can be returned to the page for display.
                        dt_settings = datatable_data([TableName],{'id':NewID})
                        
                        if dt_settings:
                            result['Success'] = True
                            result['record'] = dt_settings['data'][0]
                            I=f"Success: Record duplicated. New id={NewID}"
                        else:
                            I='Error: The new/updated record was added but could not be found.'
                            result['Success'] = False
                    else:
                        I=f"Error: We tried to insert a new record but no ID was returned. That probably means the insert didn't work."
                        LogError(pyFileName, ExtraInfo = I)
                else:
                    I=f"Error: The record with id={id} could not be found so the record could not be duplicated."
                    LogError(pyFileName, ExtraInfo = I)
            else:
                I=f"Error: The table name ({TableName}) or id ({id}) has not been supplied so the record to duplicate cannot be determined."
                LogError(pyFileName, ExtraInfo = I)

        response.flash = I
        result = json.dumps(result, indent=4, sort_keys=True, default=str)
        return result
    
    except Exception as e:
        return LogError(pyFileName, e, I, ReturnJson = True, FlashError = True)

def files():  # This function is needed for the files.load action which loads all the files needed for datatables.
    return locals()

