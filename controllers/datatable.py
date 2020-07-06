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

    return dict(dt_settings=dt_settings)

# ----------------------------------------
@auth.requires_login()
def delete():
    try:

        DataTableName = request.args[0]
        dt_settings = TableDefaults(DataTableName)
        TableName = dt_settings['TableName'] 

        x = len(request.args) 
        if x > 1:
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
        LogError(pyFileName, e)

@auth.requires_login()
def add():
    return AddOrEdit(IsAdd = True)

# ----------------------------------------
@auth.requires_login()
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

# ------------------------------------------------------------------------------------------------------------------
def datatable_data(args, vars = None, custom_settings = None):  # Initialises the settings and gets the data for the requested table

    I="Starting."

    # ----------------------------------------
    def GetColumnName(FieldName, ColumnNames):

        if FieldName in ColumnNames:
            return ColumnNames[FieldName]
        else:
            return FieldName
    # -----------------------------------------
    def BuildDataTableHTML(table, dt_settings):

        Fields = copy(dt_settings['Fields'])

        FieldList = Fields

        ColNames = dt_settings['ColumnNames'] 
        # Replace any fields with special column headings
        for cn in ColNames:
            for i, f in enumerate(FieldList):
                if f == cn:
                    FieldList[i] = ColNames[cn]

        fld_tags = ""
        for f in FieldList:
            fld_tags += "<th>%s</th>" % (f)

        dt_settings['fld_tags'] = fld_tags

        HeaderHtml = f"<thead><tr>{fld_tags}</tr></thead>"
        FooterHtml = f"<tfoot><tr>{fld_tags}</tr></tfoot>"
        # FooterHtml = f"<tfoot><tr>{fld_tags}</tr></tfoot>" if dt_settings['ShowFooter'] else ""

        # We dont really need the dialog in this section of text. One dialog per page should be sufficient. But will leave it here for the moment since it works!
        html = f"""
                <div class="flex-container">
                    <div class="top-text">
                        <span id="{dt_settings['ElementID']}-datatable-icon" class="datatable-icon"></span>
                        <span id="{dt_settings['ElementID']}-datatable-heading1" class="datatable-heading"></span>
                        <span id="{dt_settings['ElementID']}-datatable-subheading1" class="datatable-subheading"></span>
                    <div id="{dt_settings['ElementID']}-datatable-info" class="datatable-heading-info"></div>
                    </div>
                    <div id="datatable-div" class="table-responsive">
                        <table id="{dt_settings['ElementID']}" class="web2py-datatable display table table-striped table-bordered responsive nowrap" width="100%">
                            {HeaderHtml}
                            {FooterHtml}
                        </table>

                        <!-- Dialog -->
                        <div id="{dt_settings['ElementID']}-dialog" class="modal fade" role="dialog">
                            <div class="modal-dialog modal-dialog-centered modal-lg">
                            
                                <!-- Modal content-->
                                <div class="modal-content">
                                <div class="modal-header">
                                    <h4 id="{dt_settings['ElementID']}-dialog-title" class="modal-title">{dt_settings['PageHeading']}</h4>
                                    <button type="button" data-dismiss="modal">&times;</button>
                                </div>
                                <div id="{dt_settings['ElementID']}-dialog-form-div" class="modal-body">
                                    'Form goes here'
                                </div>
                                <div class="modal-footer">
                                        <div>
                                            <button class="btn-primary btn" type="submit" value="submit" class="btn btn-primary" >Submit</button>
                                        </div>
                                        <button type="button" class="btn btn-default" data-dismiss="modal">Close</button>
                                </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
        """  #.format(**dt_settings)   # % (fld_tags, fld_tags)

        return html

    def TmpDatabaseModel():
        table = db.define_table('DatabaseModel', Field('TableName'))
        # table.truncate()
        for t in db.tables:
            table.update_or_insert(TableName=t)

        return table

    try:
        Timer1, Timer2, Timer3, Timer4, Timer5 = Timer(), Timer(), Timer(), Timer(), Timer()
        Timer1.start()

        session.ReturnURL = request.url

        if args:
            if isinstance(args,str):
                DataTableName = args
            else:    
                DataTableName = args[0]

        if DataTableName == 'DatabaseModel':
            TmpDatabaseModel()

        dt_settings = GridDefaults(DataTableName, custom_settings, vars)
        TableName = dt_settings['TableName']
        table = db[TableName]
        
        I="Initialise the ColumnNames from the DAL labels."
        for fld in table.fields:
            if table[fld].label:
                try:
                    l = table[fld].label   # This is weird. The built in fields have a type of 'lazyT'. Appending them to the dictionary adds the whole object which breaks thinng. I cant find how to determine their type.
                    l = l.m
                except:
                    l = table[fld].label
                I="If we havent already set the column name then set it here."
                if fld not in dt_settings['ColumnNames']:
                    dt_settings['ColumnNames'][fld] = l
        
        # There are some tasks that can be prepared before the record loop and just use string substituion to build the final cell text
        I="Build the link template for referenced tables."
        if ':references' in dt_settings['Fields']:  
            ReferenceCnt = {}
            cell_reference_template = SeparatorChar = ''
            for ref in table._referenced_by:
                # First pass we need to build a dictionary so we know how many times a table is referenced. If it is only once
                # then we don't need to show the fieldname.                         
                if (dt_settings['ShowReferences'] == 'All' or ref.longname in dt_settings['ShowReferences']) and (ref.longname not in dt_settings['HideReferenceFields']):
                    LinkTableName, LinkFieldName = ref.longname.split('.')
                    if LinkFieldName not in dt_settings['HideReferenceFields']:
                        ReferenceCnt[LinkTableName] = ReferenceCnt[LinkTableName] + 1 if ReferenceCnt.get(LinkTableName,False) else 1

            for ref in table._referenced_by:
                # Second pass we need to build the template for cell text
                if (dt_settings['ShowReferences'] == 'All' or ref.longname in dt_settings['ShowReferences']) and (ref.longname not in dt_settings['HideReferenceFields']):
                    LinkTableName, LinkFieldName = ref.longname.split('.')
                    if LinkFieldName not in dt_settings['HideReferenceFields']:
                        LinkTableDisplayName = ref._table._plural if ref._table._plural else LinkTableName
                        if ReferenceCnt[LinkTableName] > 1:
                            FieldLinkName = f'.{LinkFieldName}'
                        else:
                            FieldLinkName = ''

                        if dt_settings['ShowReferenceIcons']:
                            TableIcon = db[LinkTableName].get('_Icon',None)
                            if TableIcon:
                                TableIconImg = f'<img src="{TableIcon}" class="dt-row-images">'
                                link_html = f'{TableIconImg}<span>{LinkTableDisplayName}{FieldLinkName}</span>'
                                SeparatorChar = ''
                            else:
                                link_html = f'{LinkTableDisplayName}{FieldLinkName}'
                                SeparatorChar = ', '
                        else:
                            link_html = f'{LinkTableDisplayName}{FieldLinkName}'
                            SeparatorChar = ', '

                        link_vars = {}
                        link_vars[LinkFieldName] = 777  # Just need a placeholder for substituion purposes later on                    
                        Link = A(XML(link_html),_href=URL('datatable','show',args=[LinkTableName], vars=link_vars))
                        Link = f'<span class="reference_link">{Link}</span>' # div needed for onhover popup
                        cell_reference_template = str(Link) if cell_reference_template == '' else cell_reference_template + SeparatorChar + str(Link)

        I="Build the filter query based on request.vars"
        SubTitle = {}
        query_parts = []
        OrderFields = table['id']
        LimitBy = (0,9999999)
        if vars:
            query = None
            for key in vars:
                k = None
                if vars[key]:
                    # The supplied variable is in a 'normal' format (eg id=5). This gets split into a normal dictionary entry with key and value. So we can use it
                    k = key
                    v = vars[key]
                    op = '='
                else:
                    # there is no value for this key so check if it is a special type of criteria (eg id>10)
                    for op in ['<=','>=','<','>']:
                        kv = key.split(op)
                        if len(kv) > 1: 
                            k = kv[0]
                            v = kv[1]
                            break
                if k:
                    if k in table.fields:
                        if table[k].type == 'list:string':
                            query_parts.append((table[k].contains(v, all=True))) 
                        else:
                            if op == '=': query_parts.append((table[k] == v)) 
                            elif op == '>=':query_parts.append((table[k] >= v)) 
                            elif op == '<=':query_parts.append((table[k] <= v)) 
                            elif op == '<':query_parts.append((table[k] < v)) 
                            elif op == '>':query_parts.append((table[k] > v)) 

                        SubTitle[k] = f"{op}{v}"
                    else:
                        if k == 'LAST':
                            OrderFields = ~table['id']
                            LimitBy=(0,int(v))

            query = (table.id>=0)
            for q in query_parts:
                query = q if query is None else query & q
        else:
            query = table

        I="Get table records"  # --------------------------------------------------------------------------------
        if not dt_settings['common_filter']: table._common_filter  = None  
        Timer2.start()
        recs = db(query).select(cacheable=False, orderby=OrderFields, orderby_on_limitby = False, limitby=LimitBy)
        Timer2.stop()
        print(db._lastsql)
        data = []
        row_num = 0

        I="Process the records "
        Timer3.start()
        if dt_settings['UseRepresent']:
            Records = recs.render()
        else:
            Records = recs
        for r in Records:
            I="Put each row into a 'row' dictionary"
            row = {}
            for f in dt_settings['Fields']:
                ShowImage = False
                cell = ""
                
                I="Check if any text is to be prepended to the column cell"
                if f in dt_settings['PrependText']:
                    cell += dt_settings['PrependText'][f]
                
                I="Check if an image is to be included in this column cell"
                if f in dt_settings['Images']:
                    css_class ='dt-row-images'
                    style= ''
                    width = get_deep(dt_settings['Images'][f],'width',None)
                    if width: style += 'width:' + width + ';'
                    cell += str(IMG(_class=css_class, _style=style, _src=dt_settings['Images'][f]['url']))
                
                I="Add links for each referenced table."
                if f == ':references':  
                    cell = cell_reference_template.replace("777",str(r.id))
                
                I="Include the row data"
                Timer5.start()
                if r.get(f,'!MiSsInG!') != '!MiSsInG!':  # VirtualFields are not in the list of table fields. So we can't check using 'in table.fields'. Need to look at the row itself. Check for '!MiSsInG!' because hopefully that is never an actual field value!
                    I = f"Process field {f} in the row."
                    if r[f] is None:
                        cell += ''
                    elif isinstance(r[f], list):  # If the field is a list then convert it into CSV format
                        I = "Field is a list."
                        cell += ",".join(map(str,r[f]))
                    elif table[f].type == 'boolean':
                        I = "Field is a boolean."
                        values = {}
                        values['checked'] = 'checked' if r[f] else ''
                        values['label'] = get_deep(dt_settings['BooleanReplacment'],r[f],'No')  # 'Yes' if r[f] else 'No'
                        cell += '<div class="dt-boolean">{label}</div><input type="checkbox" value="" {checked} onclick="return false;" onkeydown="return false;">'.format(**values)
                    elif table[f].type[:6] in ['double','decimal']:  # Checking the type wont work for virtual fields.
                        I = "Field is a decimal."
                        if r[f]:
                            cell += '{0:.2f}'.format(r[f])
                        else:
                            cell += ''
                    elif table[f].type == 'upload':
                        I="Processing an upload field."
                        if DetermineMediaRepresentation(r, FieldName = f) == 'Image':
                            ShowImage = True
                        else:
                            I="Not sure what to do with fields that are not images."
                            cell += str(r[f])
                    elif get_deep(dt_settings['FieldTypes'],f,'') == 'image':
                        I = "Field is an image."
                        ShowImage = True
                    else:
                        cell += str(r[f])
                    if ShowImage:
                        I = "Show the image."
                        if r[f]:
                            url = URL('default','image_download',args=[r[f]])
                            cell += '<img src="%s" class="dt-row-images">' % (url)
                Timer5.pause()

                I="Build links"
                if f in dt_settings['Links']:
                    I = f"Building link {f}."
                    link = ParseLink(dt_settings['Links'][f], recs.records[row_num][TableName])
                    if link == "edit_dialog":
                        cell = f"""<a class="edit-icon" RowID="{r['id']}" href="javascript:void(0);"> {XML(cell)} </a>""" 
                        # cell = """<a href="javascript:void(0);" onclick="DatatableGrid.HandleTableEvent('edit','#%s-dialog',%s)"> %s </a>""" % (dt_settings['ElementID'], r['id'], XML(cell))
                    else:
                        if cell == '': cell = f
                        cell = A(XML(cell), _href='%s'% (link)) 

                I="Get the correct heading name"
                ColName = GetColumnName(f, dt_settings['ColumnNames'])

                row[ColName] = cell
            data.append(row)
            row_num += 1
        Timer3.stop()
        I="Build the Title and subtitle"
        t = ""
        Timer4.start()
        for k in SubTitle:
            if t != "": t += " and "
            # t = t + "%s %s" % (get_deep(SubTitle[k],'Column',''), get_deep(SubTitle[k],'Value',''))
            t = t + "%s %s" % (k, SubTitle[k])
            dt_settings['PageSubHeading'] += t

        if dt_settings['PageSubHeading']:
            dt_settings['PageSubHeading'] = IMG(_class='datatable-subheading-filter', _src=URL_icon_set + 'svg/filter.svg') + dt_settings['PageSubHeading']

        if not dt_settings['Icon']: dt_settings['Icon'] = get_deep(table,'_Icon',None)
        if dt_settings['Icon']: dt_settings['Icon'] = IMG(_class='datatable-icon', _src=dt_settings['Icon'])

        I="Build the columnDef data to hide,order,search columns etc"
        columns = []
        columnDefs = []
        ordering = []
        for i,fld in enumerate(dt_settings['Fields']):
            col = {}
            col['className'] = ''

            I="Get the correct heading name"
            ColName = GetColumnName(fld, dt_settings['ColumnNames'])

            columns.append({'data':ColName})

            I="Build the orderby property"
            if fld in dt_settings['Orderable']:
                ordering.append([dt_settings['Fields'].index(fld),'asc'])
            else:
                col['orderable'] = False

            I="Set alignment class"
            col['className'] += get_deep(dt_settings['Alignment'],fld,'') + ' '

            I="Hide fields"
            if fld in dt_settings['HiddenFields']:
                col['visible'] = False
                col['className'] += 'never '

            I="Set child fields"
            if fld in dt_settings['ChildFields']:
                col['className'] += 'none '
            
            I="Set widths"
            if fld in dt_settings['Widths']:
                col['width'] = dt_settings['Widths'][fld]

            I="Set Searchable"
            col['searchable'] = (fld in dt_settings['Searchable'] or dt_settings['Searchable'] == [] or dt_settings['Searchable'][0]=='ALL')

            col['responsivePriority']= i
            col['targets'] = i

            if col:
                columnDefs.append(col)
        Timer4.stop()

        I="Get html table template"
        html = BuildDataTableHTML(table, dt_settings)

        dt_settings['order'] = ordering
        dt_settings['tablename'] = TableName
        dt_settings['html'] = html
        dt_settings['data'] = data
        dt_settings['columns'] = columns
        dt_settings['columnDefs'] = columnDefs
        
        Timer1.stop()
        
        print(Timer1.Time)
        Timers = {'Total Time':Timer1.Time,'Query':Timer2.Time,'Collate Data':Timer3.Time,'Cleanup':Timer4.Time,'FieldLoop':Timer5.Time}
        if DataTableName != 'EventLog' and True is False:
            AddLogEntry(LogType='Datatable Build', LogFunction = "datatable_data", LogMessage = Timers, EventAction = DataTableName, Settings='Cnt:' + f"{row_num}" + '   Time:' + Timer1.Time)
            
        return dt_settings

    except Exception as e:
        return LogError(pyFileName, e, I, FlashError=True)

# --------------------------------------
def ParseLink(Link, rec=None):
    
    # Two things happen here.
    # 1. We substitue an id in a link in a row to the correct value. This means we dont have to do it in the view
    # 2. We fix the escaped chars problems created by the URL function. This is needed for links that do not apply to rows (like those attached to grid buttons)
    # Note. 
    #  a) I could do it all the same way - ie let the view translate the IDs. However there is a problem with clicking on an linked image in a row because the link is processed before the Selected row event fires. 
    #  b) I could simply not use the web2py URL function or write my own so it doesnt escape these chars. Or use diffferent chars.
    if rec:
        for f in rec:
            Link = Link.replace('{' + f + '}', str(rec[f]))         # fields are identified using {}. 
            Link = Link.replace('%7B' + f + '%7D', str(rec[f]))     # However, when used in the URL function they get escaped into url friendly codes. So check for that as well.
    else:
        # Links are also specified outside of a row call. So we cant set the value in the controller - it needs to be done in the view.
        # So make sure the view gets the URL with the characters not escaped
        Link = Link.replace('%7B','{')
        Link = Link.replace('%7D','}')     

    return Link

def GridDefaults(DataTableName, custom_settings=None, vars = None):

    try:
        I="Starting GridDefaults."
        dt_settings = {'PageHeading':DataTableName, 'PageSubHeading':'', 
                        'SearchFieldSize':{}, 'PrependText':{}, 'Links':{}, 'Widths':{}, 
                         
                    }
        dt_settings['vars'] = vars                  # The vars passed in, usually to filter the table in some way. 
        dt_settings['ElementID'] = f'DT-{DataTableName}'                   # 'ElementID':
        dt_settings['DataTableName'] = None         # This is usually the same as TableName. However it allows the same table to be displayed in different ways.
        dt_settings['TableName'] = None             # Tablename defaults to args[0] in the URL. This value allows it  to be overriden.
        dt_settings['Info'] = None                  # Extra info to show below the heading.
        dt_settings['UseRepresent'] = True          # Uses web2py's rows.render() option to show the the field data using represent option specified in the table. This can have significant effects on performance
        dt_settings['Icon'] = None                  # The URL to an icon for this table. Looks first for an '_Icon' attribute added to the table in the model file.
        dt_settings['common_filter'] = True         # Applies the common filter if one exists when set to True.
        dt_settings['Fields'] = []                  # Field names are the names used in the model. This determines the order of the displayed fields in the grid.
                                                    #  If [AllFields] != '' then any other fields will be positioned as specified.
        dt_settings['FieldTypes'] = {}              # Override the actual type of the field and allows specifying extra types such as 'image'. Useful when a field holds an image and you want to display it as an image
        dt_settings['ColumnNames'] = {':references':'Links'}             # Always want the 'id' column to present as 'ID'
        dt_settings['ChildFields'] = []             # The Fields which must appear only in the expanding part of the row.
        dt_settings['HiddenFields'] = 'created_on', 'created_by', 'modified_on','modified_by','is_active'
        dt_settings['AllFields'] = 'MainRow'        # 'ChildRow', 'MainRow', ''. This determines if we include every field and where to put them.
                                                    #  If it is set to '' then only the fields specified in [Fields] are included. This is to make it easy to include all fields.
        dt_settings['DisabledFields'] = []
        dt_settings['Orderable'] = []               # Default: ALL. List the Fields which can be ordered on.
        dt_settings['Searchable']= []                # Default: ALL. List the Fields which can be searched.
        dt_settings['Alignment'] = {}
        dt_settings['Images'] = {}                  # Images to show in a column. Eg: {'Lang',{'url':'/img.png','width':'10px'}}   Eg2. {'Cards': {'url':URL('static','img/icons/set1/svg/015-card_games_clean.svg'),'width':'16px'}}
        dt_settings['Tabs'] = True
        dt_settings['AddURL'] = ''                  # Specify the URL to use to add a new record. Defaults if left empty
        dt_settings['EditURL'] = ''                  # Specify the URL to use to add a new record. Defaults if left empty
        dt_settings['Buttons'] = ['Delete','Add','Edit']              # all, add, delete, edit, print 
        dt_settings['DOM'] = ''                     # See Datatables.net for info  Example: 'Bprf<t>ip'. This value overrides the Show options below.
        dt_settings['ShowHeader'] = True            
        dt_settings['ShowFooter'] = True            
        dt_settings['ShowPageButtons'] = 'Both'     # Options: Top, Bottom, Both
        dt_settings['ShowRecordCount'] = 'Bottom'   # Options: Top, Bottom, Both
        dt_settings['ShowSearch'] = 'Top'           # Options: Top, Bottom, Both, None
        dt_settings['PageLength'] = 10              # How many records to show per page
        dt_settings['ControlImages'] = {':control': {'url':URL('static','img/icons/set1/svg/expand2.svg'),'width':'10px'},
                                ':edit': {'url':URL('static','img/icons/set1/svg/edit-pencil.svg'),'width':'16px'}
                                }
        dt_settings['ControlFields'] = [':control',':edit']
        dt_settings['ControlLinks'] = {':edit': 'edit_dialog'}
        dt_settings['Widths'] = {':control':'10px',':edit':'10px', 'id':'10px', ':references':'10px'}
        dt_settings['SearchFieldSize']['id'] = 1
        dt_settings['BooleanReplacment'] = {True:'Yes', False:'No',None:'No'}   # We need to add hidden text to checkbox fields so that we can search on that field.
        dt_settings['HideReferenceFields'] = ['modified_by','created_by']       # Defaults to hiding a few common fields. Field names can be specified as table.field or just field. The later will remove the same field from all tables.
        dt_settings['Responsive'] = True

        #----------- Get defaults for specific tables here ------------
        dt_settings = TableDefaults(DataTableName, dt_settings)
        # Merge custom settings
        if custom_settings: 
            new_dict = deepcopy(custom_settings)
            dt_settings.update(new_dict)
        #--------------------------------------------------------------

        dt_settings.setdefault('ShowReferences', 'All')  # Defaults to showing links to all referenced tables 
        dt_settings.setdefault('ShowReferenceIcons', True)  # Defaults to showing icons for tables not their names
        # Merge the defaults with the table specific values keeping the ones that we need to
        dt_settings['ColumnNames'] = {**dt_settings['ColumnNames'], **{'id':'ID'}}  # Merge: Always want the 'id' column to present as 'ID'
        dt_settings['Widths'] = {**{':control':'10px',':edit':'10px', 'id':'10px'}, **dt_settings['Widths']}  # The second dict will overwrite the first.  From python 3.9 can use |=

        if dt_settings['AddURL']: dt_settings['AddURL'] = ParseLink(dt_settings['AddURL'])
        if dt_settings['EditURL']: dt_settings['EditURL'] = ParseLink(dt_settings['EditURL'])
        
        # Default is search/orderable on all fields
        InitialiseSearch = not dt_settings['Searchable']
        InitialiseOrderable = not dt_settings['Orderable']
        DefaultSearchFieldSize = 5
        
        # If the table is not responsive then we dont need the dropdown arrow
        if not dt_settings['Responsive']:
            dt_settings['ControlFields'].remove(':control')

        # We want to set some defaults for every field including the control fields. So make a complete FieldList so we do that.
        FieldList = copy(dt_settings['ControlFields'])
        FieldList.extend(db[dt_settings['TableName']].fields)

        # Go through all the fields setting defaults
        for fld in FieldList:
            if fld[:1] != ":":  # this is a control field
                if InitialiseSearch: 
                    dt_settings['Searchable'].append(fld)
                
                if fld not in dt_settings['SearchFieldSize']: 
                    dt_settings['SearchFieldSize'].update({fld:DefaultSearchFieldSize})
                
                if InitialiseOrderable: 
                    dt_settings['Orderable'].append(fld)

            if not get_deep(dt_settings['Alignment'], fld, None):
                if fld[:1] == ":":  # this is a control field
                    FldType = 'boolean'
                else:
                    FldType = db[dt_settings['TableName']][fld].type
                if FldType in ['id','boolean','integer','double','date','time','datetime','big-int','big-id']:
                    dt_settings['Alignment'][fld] = 'dt-center'

        # We now want to do stuff only with the fields explictly set. So build a new fields list with Control and normal Fields
        FieldList = copy(dt_settings['ControlFields'])
        FieldList.extend(dt_settings['Fields'])  

        dt_settings['Fields'] = FieldList

        # Have to process this before the fields are populated.    
        if dt_settings['AllFields'] == 'ChildRow':
            # All the unspecified fields should go into the child rows
            if dt_settings['ChildFields'] == []:
                # Only do this if we haven't  specified what child fields we want
                for fld in db[dt_settings['TableName']].fields:
                    if (fld not in dt_settings['Fields']):
                        dt_settings['ChildFields'].append(fld)

        # This needs to be done again after the first run through above
        dt_settings['ModelFields'] = []
        for fld in db[dt_settings['TableName']].fields:
            dt_settings['ModelFields'].append(fld)
            if dt_settings['AllFields'] != '':
                # Append any fields not already included in the Fields list. This allows us to specify a field order for the fields we are interested in and the rest can just get added to the end
                if fld not in dt_settings['Fields']:
                    dt_settings['Fields'].append(fld)
                
        dt_settings['Images'].update(dt_settings['ControlImages'])
        dt_settings['Links'].update(dt_settings['ControlLinks'])
        dt_settings['IDcolumnNumber'] = dt_settings['Fields'].index('id')

        if dt_settings['ShowReferences']: 
            if ':references' not in dt_settings['Fields']: 
                dt_settings['Fields'].extend([':references'])  # We need a column to put and links to referenced tables
                if ':references' not in dt_settings['ChildFields']: dt_settings['ChildFields'].append(':references')

        # Disabled fields are handled in the browser. web2py updates records and displays fields based on theor writability. So any disabling of controls needs to happen in the browser otherwise it messes with the data persistence
        if dt_settings['DisabledFields']:
            DisabledFieldsWithTableName = []
            for f in dt_settings['DisabledFields']:
                DisabledFieldsWithTableName.append(f"{dt_settings['TableName']}_{f}")
            dt_settings['DisabledFields'] = DisabledFieldsWithTableName 

        # Set table framework
        if dt_settings['DOM'] == '':                     # 'Bprf<t>ip'
            DOM = {'top':'', 'bottom':''}
            if dt_settings['Buttons'] != '':  DOM['top'] += 'B'
            if dt_settings['ShowRecordCount'] in ['Both','Top']: DOM['top'] += 'i'
            if dt_settings['ShowRecordCount'] in ['Both','Bottom']: DOM['bottom'] += 'i'
            if dt_settings['ShowPageButtons'] in ['Both','Top']: DOM['top'] += 'p'
            if dt_settings['ShowPageButtons'] in ['Both','Bottom']: DOM['bottom'] += 'p'
            if dt_settings['ShowSearch'] in ['Both','Top']: DOM['top'] += 'f'
            if dt_settings['ShowSearch'] in ['Both','Bottom']: DOM['bottom'] += 'f'
            
            if not dt_settings['ShowHeader']: DOM['top'] = ''
            if not dt_settings['ShowFooter']: DOM['bottom'] = ''

            dt_settings['DOM'] = DOM['top'] + '<t>' + DOM['bottom']
        
        if DataTableName == 'DatabaseModel':
            dt_settings['Links'] = {'TableName':URL('datatable','show',args='{TableName}')}

        return dt_settings

    except Exception as e:
        LogError(pyFileName, e, I, FlashError=True)
        return 


def files():  # This function is needed for the files.load action which loads all the files needed for datatables.
    return locals()
