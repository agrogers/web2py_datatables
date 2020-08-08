from copy import copy
from copy import deepcopy
from datetime import datetime  # Need this line because i have problems when using the datetime function in other modules. I dont understand why.

pyFileName = "datatable.py"
URL_icon_set = URL("static","img/icons/set1") + "/"

if False:
    from gluon import *
    from common_functions_public import get_deep

# ------------------------------------------------------------------------------------------------------------------
def datatable_data(args, vars = None, custom_settings = None):  # Initialises the settings and gets the data for the requested table

    I="Starting."
    dt_settings = {'Success':True}

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
                                            <button id="{dt_settings['ElementID']}-submit" class="btn-primary btn" type="submit" value="submit" class="btn btn-primary" >Submit</button>
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
        table = db.define_table('DatabaseModel', Field('TableName'))  # This is not working now
        for t in db.tables:
            table.update_or_insert(TableName=t)

        return table
    
    try:
        session.ReturnURL = request.url

        if args:
            if isinstance(args,str):
                DataTableName = args
            else:    
                DataTableName = args[0]

        if DataTableName == 'DatabaseModel':
            TmpDatabaseModel()

        dt_settings = GridDefaults(DataTableName, custom_settings, vars)
        
        # Check if user has permissions to view this table
        if dt_settings['AuthGroups']:
            PermissionGranted = False
            for grp in dt_settings['AuthGroups']:
                if auth.has_membership(group_id=grp):
                    PermissionGranted = True
                    break
            if not PermissionGranted:
                dt_settings['Success'] = False
                dt_settings['Error'] = f'You do not have permission to view the {dt_settings["TableName"]} table.'
                return dt_settings

        if not dt_settings['Success']:  # There was some problem with the building of the datatable
            return dt_settings

        TableName = dt_settings['TableName']
        table = db[TableName]

        # Build a dictionary of all Fields in the Table or Query. This could be used for Query based datatables. There is still a lot of stuff that needs addressing - all the references, icons etc are Table based and wont work for queries.
        DT_Fields = {}
        if dt_settings['Query']:  # A query is being used, not a sinple table so need to build the list differently
            NewFields = []
            for f in dt_settings['Fields']:
                fn = f.split(".")
                if len(fn) == 2: 
                    DT_Fields[f] = db[fn[0]][fn[1]]
                    NewFields.append(f)
            OrderFields = None
            dt_settings['Fields'] = NewFields
        else:
            for f in table.fields:
                DT_Fields[f] = table[f]
            OrderFields = DT_Fields['id']

        I="Initialise the ColumnNames from the DAL labels."
        for fld in DT_Fields:
            if DT_Fields[fld].label:
                try:
                    l = DT_Fields[fld].label   # This is weird. The built in fields have a type of 'lazyT'. Appending them to the dictionary adds the whole object which breaks thinng. I cant find how to determine their type.
                    l = l.m
                except:
                    l = DT_Fields[fld].label
                I="If we havent already set the column name then set it here."
                if fld not in dt_settings['ColumnNames']:
                    dt_settings['ColumnNames'][fld] = l
        
        # There are some tasks that can be prepared before the record loop and just use string substituion to build the final cell text
        I="Build the link template for referenced tables."
        if ':references' in dt_settings['Fields'] and not dt_settings['Query']:  
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
                        link_vars[LinkFieldName] = 777  # Just need a placeholder for substituion purposes later on but it needs to be a value that the URL function wont complain about                   
                        Link = A(XML(link_html),_href=URL('datatable','show',args=[LinkTableName], vars=link_vars))
                        Link = f'<span class="reference_link">{Link}</span>'  # div needed for onhover popup
                        cell_reference_template = str(Link) if cell_reference_template == '' else cell_reference_template + SeparatorChar + str(Link)

        I="Build the filter query based on request.vars"
        SubTitle = {}; query_parts = []; LimitBy = (0,9999999)
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
                    for op in ['<=','>=','<','>','CONTAINS']:
                        kv = key.split(op)
                        if len(kv) > 1: 
                            k = kv[0].strip()
                            v = kv[1].strip()
                            break
                if k:
                    if k in DT_Fields:
                        if op == '=': query_parts.append((DT_Fields[k] == v)) 
                        elif op == '>=':query_parts.append((DT_Fields[k] >= v)) 
                        elif op == '<=':query_parts.append((DT_Fields[k] <= v)) 
                        elif op == '<':query_parts.append((DT_Fields[k] < v)) 
                        elif op == '>':query_parts.append((DT_Fields[k] > v)) 
                        elif op == 'CONTAINS':query_parts.append((DT_Fields[k].contains(v)))
                        SubTitle[k] = {}
                        SubTitle[k]['Operator'] = op
                        SubTitle[k]['Value'] = v
                    else:
                        if k == 'LAST':
                            OrderFields = ~DT_Fields['id']
                            LimitBy=(0,int(v))

            # query = (table.id>=0)
            query = (DT_Fields['id']>=0)
            for q in query_parts:
                query = q if query is None else query & q
        else:
            query = table

        I="Get table records"  # --------------------------------------------------------------------------------
        SetCache = False
        if not dt_settings['common_filter']: table._common_filter  = None  
        if dt_settings['Query']:
            #  Need to include the filter clause    recs = db(query & dt_settings['Query']).select(db.CardMasterContent.id, db.CardMasterContent.CardMasterID, db.Media.Icon, cacheable=SetCache, orderby=OrderFields, orderby_on_limitby = False, limitby=LimitBy)
            recs = db(dt_settings['Query']).select()
            dt_settings['Query'] = 'Replaced since we dont need it anymore and it causes JSON errors'
        else:
            # recs = db(query).select(cache=(cache.ram, 3600), cacheable=SetCache, orderby=OrderFields, orderby_on_limitby = False, limitby=LimitBy)
            # recs = db(query).select(orderby=OrderFields, orderby_on_limitby = False, limitby=LimitBy)
            recs = db(query).select(orderby=OrderFields, limitby=LimitBy)

        data = []
        row_num = 0

        I="Process the records "
        if dt_settings['UseRepresent']: Records = recs.render()
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
                    url = get_deep(dt_settings['Images'][f],'url',None)
                    if url: 
                        cell_img = str(IMG(_class=css_class, _style=style, _src=dt_settings['Images'][f]['url']))
                        key = f"{f}.Label"
                        cell += f'<span class="reference_link">{cell_img}<span>{get_deep(dt_settings["Images"],key,"")}</span></span>'  # div needed for onhover popup
                    else:
                        txt = get_deep(dt_settings['Images'][f],'Text',None)
                        if txt:
                            cell = ParseLink(txt, recs.records[row_num][TableName])
                
                I="Add links for each referenced table."
                if f == ':references':  
                    cell = cell_reference_template.replace("777",str(r.id))
                
                I="Include the row data"
                if r.get(f,'!MiSsInG!') != '!MiSsInG!':  # VirtualFields are not in the list of table fields. So we can't check using 'in table.fields'. Need to look at the row itself. Check for '!MiSsInG!' because hopefully that is never an actual field value!
                    I = f"Process field '{f}' in the row."
                    if f in DT_Fields:  # Need to get the FieldType like this because VirtualFields dont exist in the DT_Fields list
                        FieldType = DT_Fields[f].type
                    else:
                        FieldType = ''
                    if r[f] is None:
                        cell += ''
                    elif isinstance(r[f], list):  # If the field is a list then convert it into CSV format
                        I = "Field is a list."
                        cell += ",".join(map(str,r[f]))  # Convert list to CSV
                    elif FieldType == 'boolean':
                        I = "Field is a boolean."
                        values = {}
                        values['checked'] = 'checked' if r[f] else ''
                        values['label'] = get_deep(dt_settings['BooleanReplacment'],r[f],'No')  # 'Yes' if r[f] else 'No'
                        cell += '<div class="dt-boolean">{label}</div><input type="checkbox" value="" {checked} onclick="return false;" onkeydown="return false;">'.format(**values)
                    elif FieldType[:6] in ['double','decimal']:  # Checking the type wont work for virtual fields.
                        I = "Field is a decimal."
                        if r[f]:
                            cell += '{0:.2f}'.format(r[f])
                        else:
                            cell += ''
                    elif FieldType == 'upload':
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

                I="Build links"
                if f in dt_settings['Links']:
                    I = f"Building link {f}."
                    link = ParseLink(dt_settings['Links'][f], recs.records[row_num][TableName])
                    if link == "edit_dialog":
                        cell = f"""<a class="edit-icon" RowID="{r['id']}" href="javascript:void(0);"> {XML(cell)} </a>""" 
                    else:
                        if cell == '': cell = f
                        cell = A(XML(cell), _href='%s'% (link)) 

                I="Get the correct heading name"
                ColName = GetColumnName(f, dt_settings['ColumnNames'])

                row[ColName] = cell
            data.append(row)
            row_num += 1
        I="Build the Title and subtitle"
        if SubTitle:
            t = ""
            if recs:
                # Try and convert ids into their human readable represents value
                for row in recs[0:1].render():
                    for k in SubTitle:
                        SubTitle[k]['Value'] = row[k]

            for k in SubTitle:
                if t != "": t += " and "
                # t = t + "%s %s" % (k, SubTitle[k])
                t += f"{k} {SubTitle[k]['Operator']} {SubTitle[k]['Value']}"
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
            elif fld[:1] == ':':
                # Special fields which start with a ':' often need to be as small as possible. So set that here.
                col['width'] = '10px'

            I="Set Searchable"
            col['searchable'] = (fld in dt_settings['Searchable'] or dt_settings['Searchable'] == [] or dt_settings['Searchable'][0]=='ALL')

            col['responsivePriority']= i
            col['targets'] = i

            if col:
                columnDefs.append(col)

        I="Get html table template"
        html = BuildDataTableHTML(table, dt_settings)

        dt_settings['order'] = ordering
        dt_settings['tablename'] = TableName
        dt_settings['html'] = html
        dt_settings['data'] = data
        dt_settings['columns'] = columns
        dt_settings['columnDefs'] = columnDefs

        if DataTableName != 'EventLog' and True is False:
            AddLogEntry(LogType='Datatable Build', LogFunction = "datatable_data", LogMessage = '', EventAction = DataTableName, Settings='Cnt:' + f"{row_num}")
        dt_settings['Success'] = True

        return dt_settings

    except Exception as e:
        dt_settings['Success'] = False
        dt_settings['Error'] = LogError(pyFileName, e, I, FlashError=True)
        return dt_settings

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
        dt_settings['Alignment'] = {}
        dt_settings['AllFields'] = 'MainRow'        # 'ChildRow', 'MainRow', ''. This determines if we include every field and where to put them.
                                                    #  If it is set to '' then only the fields specified in [Fields] are included. This is to make it easy to include all fields.
        dt_settings['AddURL'] = ''                  # Specify the URL to use to add a new record. Defaults if left empty
        dt_settings['AuthGroups'] = []
        dt_settings['BooleanReplacment'] = {True:'Yes', False:'No',None:'No'}   # We need to add hidden text to checkbox fields so that we can search on that field.
        dt_settings['Buttons'] = ['Delete','Add','Edit']              # all, add, delete, edit, print 
        dt_settings['ChildFields'] = []             # The Fields which must appear only in the expanding part of the row.
        dt_settings['ColumnNames'] = {':references':'Links'}             # Always want the 'id' column to present as 'ID'
        dt_settings['common_filter'] = True         # Applies the common filter if one exists when set to True.
        dt_settings['ControlImages'] = {':control': {'url':URL('static','img/icons/set1/svg/expand2.svg'),'width':'10px','Label':''},
                                ':edit': {'url':URL('static','img/icons/set1/svg/edit-pencil.svg'),'width':'16px','Label':''}
                                }
        dt_settings['ControlFields'] = [':control',':edit']
        dt_settings['ControlLinks'] = {':edit': 'edit_dialog'}
        dt_settings['CustomButtons'] = None
        dt_settings['DataTableName'] = None         # This is usually the same as TableName. However it allows the same table to be displayed in different ways.
        dt_settings['DisabledFields'] = []
        dt_settings['DOM'] = ''                     # See Datatables.net for info  Example: 'Bprf<t>ip'. This value overrides the Show options below.
        dt_settings['EditURL'] = ''                  # Specify the URL to use to add a new record. Defaults if left empty
        dt_settings['ElementID'] = f'DT-{DataTableName}'                   # 'ElementID':
        dt_settings['Fields'] = []                  # Field names are the names used in the model. This determines the order of the displayed fields in the grid.
                                                    #  If [AllFields] != '' then any other fields will be positioned as specified.
        dt_settings['FieldsPerTab'] = 8             # Number of fields to show on each Tab in the popup dialog
        dt_settings['FieldTypes'] = {}              # Override the actual type of the field and allows specifying extra types such as 'image'. Useful when a field holds an image and you want to display it as an image
        dt_settings['HiddenFields'] = ['created_on', 'created_by', 'modified_on','modified_by','is_active']
        dt_settings['HideReferenceFields'] = ['modified_by','created_by']       # Defaults to hiding a few common fields. Field names can be specified as table.field or just field. The later will remove the same field from all tables.
        dt_settings['Images'] = {}                  # Images to show in a column. Eg: {'Lang',{'url':'/img.png','width':'10px'}}   Eg2. {'Cards': {'url':URL('static','img/icons/set1/svg/015-card_games_clean.svg'),'width':'16px'}}
        dt_settings['Info'] = None                  # Extra info to show below the heading.
        dt_settings['Icon'] = None                  # The URL to an icon for this table. Looks first for an '_Icon' attribute added to the table in the model file.
        dt_settings['Orderable'] = []               # Default: ALL. List the Fields which can be ordered on.
        dt_settings['PageLength'] = 10              # How many records to show per page
        dt_settings['Query'] = None                 # Custom query to use instead of a table
        dt_settings['Responsive'] = True
        dt_settings['Searchable']= []                # Default: ALL. List the Fields which can be searched.
        dt_settings['SearchFieldSize']['id'] = 1
        dt_settings['ShowHeader'] = True            
        dt_settings['ShowFooter'] = True            
        dt_settings['ShowPageButtons'] = 'Both'     # Options: Top, Bottom, Both
        dt_settings['ShowRecordCount'] = 'Bottom'   # Options: Top, Bottom, Both
        dt_settings['ShowSearch'] = 'Top'           # Options: Top, Bottom, Both, None
        dt_settings['TableName'] = None             # Tablename defaults to args[0] in the URL. This value allows it  to be overriden.
        dt_settings['Tabs'] = True
        dt_settings['UseRepresent'] = True          # Uses web2py's rows.render() option to show the the field data using represent option specified in the table. This can have significant effects on performance
        dt_settings['vars'] = vars                  # The vars passed in, usually to filter the table in some way. 
        dt_settings['Widths'] = {':control':'10px',':edit':'10px', 'id':'10px', ':references':'10px'}

        #----------- Get defaults for specific tables here ------------
        dt_settings = TableDefaults(DataTableName, dt_settings)
        # Merge custom settings
        if custom_settings: 
            new_dict = deepcopy(custom_settings)
            dt_settings.update(new_dict)
        #--------------------------------------------------------------

        if dt_settings['TableName'] not in db.tables:  # Need to make sure the table exists before continuing
            dt_settings['Success'] = False
            dt_settings['Error'] = f'The {dt_settings["TableName"]} table does not exist in this database.'
            return dt_settings

        dt_settings.setdefault('ShowReferences', 'All')  # Defaults to showing links to all referenced tables 
        dt_settings.setdefault('ShowReferenceIcons', True)  # Defaults to showing icons for tables not their names
        
        # Merge the defaults with the table specific values keeping the ones that we need to
        dt_settings['ColumnNames'] = {**dt_settings['ColumnNames'], **{'id':'ID'}}  # Merge: Always want the 'id' column to present as 'ID'
        dt_settings['Widths'] = {**{':control':'10px',':edit':'10px', 'id':'10px', 'Icon':'10px'}, **dt_settings['Widths']}  # The second dict will overwrite the first.  From python 3.9 can use |=

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

            # Get the type of the field
            if fld[:1] == ":":  # this is a control field so treat like a boolean to get center aligned
                FldType = 'boolean'
            else:
                FldType = db[dt_settings['TableName']][fld].type

            if FldType in ['id','boolean','integer','double','date','time','datetime','big-int','big-id']:
                # Default alignment is center
                if not get_deep(dt_settings['Alignment'], fld, None):
                    dt_settings['Alignment'][fld] = 'dt-center'
                # Default width is 10px - ie the width of the header usually
                if not get_deep(dt_settings['Widths'], fld, None):
                    dt_settings['Widths'][fld] = '10px'

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

        # This needs to be done again after the first run through above. We need to process the fields explicitly mentioned first then append all additional fields if required.
        dt_settings['ModelFields'] = []
        for fld in db[dt_settings['TableName']].fields:
            dt_settings['ModelFields'].append(fld)
            if dt_settings['AllFields'] != '':
                # Append any fields not already included in the Fields list. This allows us to specify a field order for the fields we are interested in and the rest can just get added to the end
                if fld not in dt_settings['Fields']:
                    dt_settings['Fields'].append(fld)

        # Make sure child fields are included in the field list
        for f in dt_settings['ChildFields']:
            if f not in dt_settings['Fields']: dt_settings['Fields'].append(f)

        # Make sure hidden fields are included in the field list
        for f in dt_settings['HiddenFields']:
            if f not in dt_settings['Fields']: dt_settings['Fields'].append(f)

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
            if dt_settings['ShowPageButtons'] in ['Both','Top'] and dt_settings['PageLength']>0: DOM['top'] += 'p'
            if dt_settings['ShowPageButtons'] in ['Both','Bottom'] and dt_settings['PageLength']>0: DOM['bottom'] += 'p'
            if dt_settings['ShowSearch'] in ['Both','Top']: DOM['top'] += 'f'
            if dt_settings['ShowSearch'] in ['Both','Bottom']: DOM['bottom'] += 'f'
            
            if not dt_settings['ShowHeader']: DOM['top'] = ''
            if not dt_settings['ShowFooter']: DOM['bottom'] = ''

            dt_settings['DOM'] = DOM['top'] + '<t>' + DOM['bottom']
        
        # Set default values for CustomButtons
        if dt_settings['CustomButtons']:
            for c in dt_settings['CustomButtons']:
                dt_settings['CustomButtons'][c].setdefault('url', None)
                dt_settings['CustomButtons'][c].setdefault('Extend', 'selectedSingle')
                dt_settings['CustomButtons'][c].setdefault('Prompt', None)
                dt_settings['CustomButtons'][c].setdefault('SuccessAction', None)
                dt_settings['CustomButtons'][c].setdefault('FailureAction', None)

        if DataTableName == 'DatabaseModel':
            dt_settings['Links'] = {'TableName':URL('datatable','show',args='{TableName}')}

        dt_settings['Success'] = True
        return dt_settings

    except Exception as e:
        LogError(pyFileName, e, I, FlashError=True)
        return dt_settings

