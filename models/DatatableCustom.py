# from copy import copy
# from copy import deepcopy
# import simplejson as json
from datetime import datetime
# from timer import Timer
# from random import randrange

pyFileName = "common_datatable.py"

""" --- URL Query Options Help ---
    Format: .../datatable/show/[tablename]?[query]
    Operators: LAST,CONTAINS,>,<,=,>=,<=
    Examples:
        .../datatable/show/Media?LAST=50
        .../datatable/show/Media?Description%20CONTAINS%20Card%20Back
        .../datatable/show/Media?IsCardBack=True
        .../datatable/show/Media?id=17 """

# Default values for specific tables in this model
def TableDefaults(DataTableName, dt_settings={}):

    dt_settings['DataTableName'] = DataTableName
    dt_settings['TableName'] = DataTableName
    # dt_settings['AuthGroups'] = ['admin']

    if DataTableName == 'ALL Settings in Alphabetical order':
        dt_settings['AddURL'] = ''                              # The URL of the controller which supplies the form for the 'add' dialog.
        dt_settings['AuthGroups'] = []                          # A list of auth groups  eg ['admin','teacher']
        dt_settings['Alignment'] = {}                           # Options: {'id':'dt-center','fldname':'dt-right'}.  Specify the alignment of cell text in the column. By default 'id','boolean','integer','double','date','time','datetime','big-int','big-id' are centred.
        dt_settings['AllFields'] = 'ChildRow'                   # Options: 'ChildRow', 'MainRow', ''. This determines if we include every field (not defined elsewhere) and where to place them.
        dt_settings['BooleanReplacment'] = {True:'Yes', False:'No',None:'No'}       # Dictionary for True, False, None.  We add hidden text to checkbox fields so that we can search on that field. The dictionary determines what hidden text is included.
        dt_settings['Buttons'] = ['delete','add','edit']        # all, add, delete, edit, print 
        dt_settings['ChildFields'] = []                         # Options: a list of field names.  Forces those fields into the expandable datatable child row
        dt_settings['ColumnNames'] = {":Build":"Build"}         # Dictionary of fieldnames and column names. Sets the column heading to the value specified.
        dt_settings['common_filter'] = True                     # Ignore the common_filter set in the table definition used to restrict what records are returned
        dt_settings['ControlFields'] = [':control',':edit']     # Special fields that are usually added to the left side of the grid.
        dt_settings['ControlLinks'] = {':edit': 'edit_dialog'}  # Dictionary indicating what control fields link to. 'edit_dialog' identifies the default edit dialog.
        dt_settings['CustomButtons'] = None                     # Dictionary of dictionaries. {'Button1 Label,{'url:None, 'Extend':'selectedSingle','Prompt':None,'SuccessAction':'RefreshRecord|RefreshPage|""', 'FailureAction':'Not implemented'}}
        dt_settings['DisabledFields'] = []                      # Which fields should be displayed disabled in the edit and add forms.
        dt_settings['DOM'] = ''                                 # See Datatables.net for info  Example: 'Bprf<t>ip'. This value overrides the Show options below.
        dt_settings['EditURL'] = ''                             # The URL of the controller which supplies the form for the 'edit' dialog.
        dt_settings['ElementID'] = f'DT-{DataTableName}'        # 'ElementID': This must remain the same if you want the state of the table to be restored.
        dt_settings['Fields'] = [':Organisations']              # A list of table and special fields. It allows for custom ordering of fields. Fieldnames that start with a ':' are treated differently (by default their width is set to 10px, type is set to Boolean, it is not searchable or orderable)
        dt_settings['FieldsPerTab'] = 8                         # Number of fields to show on each Tab in the popup dialog        
        dt_settings['FieldTypes'] = {}                          # A dictionary that allows your to override the actual type of the field. This allows specifying extra types such as 'image'. It's useful when a field holds an image and you want to display it as an image.
        dt_settings['HiddenFields'] = []                        # A list of field names. When empty, the created_by, created_on etc fields are hidden
        dt_settings['HideReferenceFields'] = ['modified_by','created_by']           # List of fieldnames. Defaults to hiding a few common fields. Field names can be specified as table.field or just field. The later will remove the same field from all tables.
        dt_settings['IDcolumnNumber'] = ''                      # You do not set this value. It holds the field index for the 'id' column.
        dt_settings['Images'] = {'MyFieldName1': {'url':'ImgURL','width':'16px','Label':'Hover Label'}}   # A dictionary of dictionaries used to show an image instead of the cell text. Normally used in conjunction with the Links setting
        dt_settings['Info'] = None                              # Extra info to show below the heading.
        dt_settings['Links'] = {'MyFieldName1':'MyURL1','MyFieldName2':'MyURL2'}    # A dictionary of field:url. The fieldname must appear in one of the Field settings in order to know where to place the link
        dt_settings['Orderable'] = []                           # a list of fieldnames. Specifies which columns can be ordered.
        dt_settings['PageHeading'] = "My Custom Heading"        # Custom page heading
        dt_settings['PageLength'] = 10                          # How many records to show per page.
        dt_settings['Responsive'] = True                        # Options: True, False.  Makes a table responsive.
        dt_settings['Searchable'] = []                          # A list of fieldnames. Identifies which fields have the search field displayed.
        dt_settings['ShowReferences'] = True                    # Options: 'Media.modified_by' 
        dt_settings['ShowReferenceIcons'] = True                # Options: True, False.  Use the table icons (if available) instead of table names.
        dt_settings['ShowHeader'] = True                        # Options: True, False. Shows nothing above the first row of the table. Overrides the Show options for 'top' below
        dt_settings['ShowFooter'] = True                        # Options: True, False. Shows nothing below the last row of the table. Overrides the Show options for 'bottom' below
        dt_settings['ShowPageButtons'] = 'Both'                 # Options: Top, Bottom, Both, None
        dt_settings['ShowRecordCount'] = 'Bottom'               # Options: Top, Bottom, Both, None
        dt_settings['ShowSearch'] = 'Top'                       # Options: Top, Bottom, Both, None
        dt_settings['TableName'] = DataTableName                # Defaults to the DataTableName function parameter
        dt_settings['Tabs'] = True                              # Options: True, False, List of dictionaries.  Shows tabs in the add and edit dialog. Example: {'Field':'id','Label':'General'},...
        dt_settings['UseRepresent'] = True                      # Options: True, False.  Uses the Represent settings in the table to render records. Disabling this can improve rendering time significantly
        dt_settings['Widths'] = {'FieldName':'10px'}            # Dictionary of field and width in pixels

    elif DataTableName == 'TestQ':
        # There is still work to do on this. Need handle lots more - id, Editing, control, links etc
        dt_settings['PageHeading'] = "Teaching Groups Query"
        dt_settings['TableName'] = 'TeachingGroupStudent'
        dt_settings['Query'] = (db.TeachingGroup.id==db.TeachingGroupStudent.TeachingGroupID)
        dt_settings['Fields'] = ['TeachingGroup.LongName','TeachingGroupStudent.StudentUserID']
        # dt_settings['ColumnNames'] = {":Build":"Build"}         # Dictionary of fieldnames and column names. Sets the column heading to the value specified.

    elif DataTableName in ['auth_event']:
        dt_settings['TableName'] = 'auth_event'
        dt_settings['Info'] = "Logs changes in the other tables and successful access via CRUD to objects controlled by the RBAC."
        dt_settings['PageHeading'] = 'Auth Events'
        
    elif DataTableName in ['auth_group']:
        dt_settings['TableName'] = 'auth_group'
        dt_settings['Info'] = "Stores groups or roles for users in a many-to-many structure. By default, each user is in its own group, but a user can be in multiple groups, and each group can contain multiple users. A group is identified by a role and a description."
        dt_settings['PageHeading'] = 'User Groups'
        
    elif DataTableName in ['auth_membership']:
        dt_settings['TableName'] = 'auth_membership'
        dt_settings['Info'] = "Links users and groups in a many-to-many structure."
        dt_settings['PageHeading'] = 'User Membership'
        
    elif DataTableName in ['auth_permission']:
        dt_settings['TableName'] = 'auth_permission'
        dt_settings['Info'] = "And 'auth' table that dictates permissions."
        dt_settings['PageHeading'] = 'User Permissions'
        
    elif DataTableName == 'auth_user':
        dt_settings['PageHeading'] = "Users"
        dt_settings['Fields'] = [':Organisations']
        dt_settings['Links'] = {':Organisations': URL('datatable','show',args=['UserOrganisations'], vars={'UserID':'{id}'})}
        dt_settings['Images'] = {':Organisations': {'url':URL('static','img/icons/set1/svg/organisations.svg'),'width':'16px'}}
        # dt_settings['ShowReferences'] = 'Media.modified_by' 
        # dt_settings['ShowReferences'] = None

    elif DataTableName == 'Card':
        dt_settings['PageHeading'] = 'Cards'
        dt_settings['TableName'] = 'Card'
        dt_settings['AuthGroups'] = ['admin','teacher']
        dt_settings['UseRepresent'] = True
        dt_settings['Fields'] = [':Decks',':CardMaster',':FullDetails',':Preview','LongName']
        dt_settings['ChildFields'] = ['FrontFaceStructure','BackFaceStructure','FrontFaceRendered','BackFaceRendered']
        dt_settings['Links'] = {':Decks': URL('datatable','show',args=['CardDecks'],vars={'CardID':'{id}'}),
                                ':CardMaster': URL('datatable','show',args=['CardMaster'],vars={'id':'{CardMasterID}'}),
                                ':FullDetails': URL('card','FullCardDetails',args=['{id}']),
                                ':Preview': URL('card','preview',args=['{id}'])}
        dt_settings['Images'] = {':Decks': {'url':URL('static','img/icons/set1/svg/deck6.svg'),'Label':'Decks with this card'},
                                ':CardMaster': {'url':URL('static','img/icons/set1/svg/cardmaster.svg'),'Label':'Card Master for this card'},
                                ':FullDetails': {'url':URL('static','img/icons/set1/svg/full_card_details.svg'),'Label':'Full card details'},
                                ':Preview': {'url':db.Card._PreviewIcon,'Label':'Preview'}}
        dt_settings['CustomButtons'] = {'Render Card':{'url':"%s%s" % (URL('card','render'),"?CardID={id}"),'Extend':'selectedSingle','SuccessAction':'RefreshRecord'},
                                        'Render All Cards':{'url':"%s" % (URL('card','render',vars={'AllCards':'True'})),'Extend':'','SuccessAction':'RefreshPage','Prompt':'Are you sure you want to render all cards?'}}

    elif DataTableName == 'CardCategory':
        dt_settings['PageHeading'] = 'Card Categories'
        dt_settings['TableName'] = 'CardCategory'
        dt_settings['AuthGroups'] = ['admin','teacher']
        dt_settings['Fields'] = [':Cards']
        dt_settings['Links'] = {':Cards': URL('datatable','show',args=['CardMaster'],vars={'Categories':'{LongName}'})}
        dt_settings['Images'] = {':Cards': {'url':URL('static','img/icons/set1/svg/cards.svg')}}
        dt_settings['UseRepresent'] = False
        dt_settings['CustomButtons'] = {'Update Counts for ALL records':{'url':"%s" % (URL('cardcategory','UpdateAllCounts')),
                                                              'Extend':'','Prompt':'Are you sure you want to update ALL records?','SuccessAction':'RefreshPage'}}

    elif DataTableName == 'CardDecks':
        dt_settings['PageHeading'] = 'Decks where this card is found'
        dt_settings['TableName'] = 'DeckCard'
        dt_settings['AuthGroups'] = ['admin','teacher']
        dt_settings['ChildFields'] = ['CardID']

    elif DataTableName in ['CardMaster','CardMaster2']:
        dt_settings['PageHeading'] = 'Card Master'
        dt_settings['TableName'] = 'CardMaster'
        dt_settings['AuthGroups'] = ['admin','teacher']
        dt_settings['Info'] = 'The container for a card. It provides a link to all relevant information (text, images, audio etc) in all languages.'
        dt_settings['Fields'] = [':references']
        dt_settings['AllFields'] = 'MainRow'
        dt_settings['common_filter'] = False
        dt_settings['UseRepresent'] = False
        if DataTableName in ['CardMaster2']:
            dt_settings['ChildFields'] = ['id']
            dt_settings['Fields'] = [':references','Name','Categories','Description']

    elif DataTableName in ['CardMasterContent','CardMasterContent2']:
        dt_settings['PageHeading'] = 'Card Master Content'
        dt_settings['TableName'] = 'CardMasterContent'
        dt_settings['AuthGroups'] = ['admin','teacher']
        dt_settings['Info'] = 'The content used to construct a card. The final card may inlcude some or all of these records.'
        dt_settings['Fields'] = ['Icon','ContentText','ContentType']
        dt_settings['FieldTypes'] = {'Icon':'image'}
        dt_settings['AllFields'] = 'MainRow'
        dt_settings['common_filter'] = False
        dt_settings['UseRepresent'] = True
        if DataTableName in ['CardMasterContent2']:
            # dt_settings['Query'] = (db.CardMasterContent.ContentMediaID==db.Media.id)
            dt_settings['ChildFields'] = ['id', 'RelatedCards']
            dt_settings['HiddenFields'].extend(['CardMasterID'])
            dt_settings['PageLength'] = 9999
            dt_settings['ShowFooter'] = False
            dt_settings['Searchable'] = ['None']
            dt_settings['Widths'] = {'Icon':'10px'}
            # dt_settings['UseRepresent'] = False

    elif DataTableName == 'CardStructure':
        dt_settings['Fields'] = [':Cards','LongName', 'ShortName','Lang']
        dt_settings['PageHeading'] = DataTableName 
        dt_settings['AuthGroups'] = ['admin','teacher']
        dt_settings['ChildFields'] = ['FrontFaceStructure','BackFaceStructure']
        dt_settings['Links'] = {':Cards': URL('datatable','show',args=['Card'], vars={'CardStructureID':'{id}'})}
        dt_settings['Images'] = {':Cards': {'url':URL('static','img/icons/set1/svg/cards2.svg'),'width':'16px'}}

    elif DataTableName == 'ContentType':
        dt_settings['PageHeading'] = 'Content Types' 
        dt_settings['PageLength'] = 999
        dt_settings['ShowPageButtons'] = 'None'

    elif DataTableName == 'Deck':
        dt_settings['PageHeading'] = "Decks"
        dt_settings['TableName'] = "Deck"
        dt_settings['AuthGroups'] = ['admin','teacher']
        dt_settings['Fields'] = [':Build',':DeckChildren',':Cards',':UserDecks',':GroupDecks','LongName','DefaultCardStructureID','CardCriteria','ChildDeckIDList','ParentDeckIDList','is_active','id', 'created_by']
        dt_settings['Orderable'] = ['LongName','ShortName','CardCriteria','id']
        dt_settings['PrependText'] = {':control': ''}
        dt_settings['Searchable'] = ['LongName','ShortName','CardCriteria','ChildDeckIDList','ParentDeckIDList','DefaultCardStructureID']
        dt_settings['Widths'] = {'ParentDecks':'1px'}
        dt_settings['UseTabs'] = [{'Field':'id','Label':'General'},{'Field':'ChildDeckIDList','Label':'Related Decks'},{'Field':'QuestionCardSize','Label':'Sizes'},{'Field':'PresentationOptions','Label':'Other'}]
        dt_settings['Links'] = {':Build': URL('deckcard','DeckBuilder',args=['{id}']),
                                ':Cards': URL('datatable','show',args=['DeckCard2'], vars={'DeckID':'{id}'}),
                                ':DeckChildren': URL('datatable','show',args=['DeckChild'], vars={'DeckID':'{id}'}),
                                ':UserDecks': URL('datatable','show',args=['UserDeck'], vars={'DeckID':'{id}'}),
                                ':GroupDecks': URL('datatable','show',args=['TeachingGroupDeck3'], vars={'DeckID':'{id}'})}
        dt_settings['Images'] = {   ':Build': {'url':URL('static','img/icons/set1/svg/deck_builder4.svg'),'Label':'Build Deck'},
                                    ':Cards': {'url':URL('static','img/icons/set1/svg/cards.svg'),'Label':'Deck Cards'},
                                    ':DeckChildren': {'url':db.DeckChild._Icon,'Label':'Child Decks'},
                                    ':UserDecks': {'url':db.UserDeck._Icon,'Label':'Users with this deck'},
                                    ':GroupDecks': {'url':db.TeachingGroupDeck._Icon,'Label':'Groups with this deck'}}
        dt_settings['CustomButtons'] = {'Duplicate Deck':{'url':"%s" % (URL('datatable','duplicate',vars={'TableName':dt_settings['TableName']})),
                                                              'Extend':'selectedSingle','Prompt':'Are you sure you want to duplicate this record?','SuccessAction':'InsertRecord'},
                                        'Render all cards in the deck':{'url':"%s%s" % (URL('card','render'),"?DeckID={id}"),'Extend':'selectedSingle','SuccessAction':'','Prompt':'Are you sure you want to render all cards?'}}
                                                              
    elif DataTableName in ['DeckCard','DeckCard2']:
        dt_settings['TableName'] = 'DeckCard'
        dt_settings['Fields'] = [':Card']
        dt_settings['AuthGroups'] = ['admin','teacher']
        dt_settings['PageHeading'] = 'Deck Cards'
        dt_settings['Info'] = 'What decks does this card appear in.'
        dt_settings['Links'] = {':Card': URL('datatable','show',args=['Card'], vars={'id':'{CardID}'})}
        dt_settings['Images'] = {':Card': {'url':db.Card._Icon,'width':'16px','Label':'Card Details'}}
        dt_settings['CustomButtons'] = {'Render card':{'url':"%s%s" % (URL('card','render'),"?DeckCardID={id}"),'Extend':'selectedSingle','SuccessAction':'RefreshRecord','Prompt':'Are you sure you want to render this card?'}}
        if DataTableName == 'DeckCard2':
            dt_settings['ChildFields'] = ['DeckID']

    elif DataTableName == 'DeckChild':
        dt_settings['Fields'] = [':DeckChildren',':DeckCards']
        dt_settings['PageHeading'] = 'Deck Children'
        dt_settings['AuthGroups'] = ['admin','teacher']
        dt_settings['EditURL'] = 'IncludeVars'
        dt_settings['AddURL'] = 'IncludeVars'
        dt_settings['Links'] = {':DeckChildren': URL('datatable','show',args=['DeckChild'], vars={'DeckID':'{ChildDeckID}'}),
                                ':DeckCards': URL('datatable','show',args=['DeckCard2'], vars={'DeckID':'{ChildDeckID}'})}
        dt_settings['Images'] = {':DeckChildren': {'url':db.DeckChild._Icon,'Label':'Child Decks'},
                                 ':DeckCards': {'url':db.Card._Icon,'Label':'Deck Cards'}}

    elif DataTableName == 'EventLog':
        dt_settings['PageHeading'] = 'Event Log'
        dt_settings['Fields'] = ['id','Processed','created_on','LogType','LogFunction','EventAction','ObjectID','UserID']
        dt_settings['AllFields'] = 'MainRow'
        dt_settings['HiddenFields'] = ['created_by','modified_by','modified_on']
        dt_settings['common_filter'] = False
        dt_settings['UseRepresent'] = False
        dt_settings['CustomButtons'] = {'Delete ALL records':{'url':(URL('datatable','DeleteAll',vars={'TableName':'EventLog'})),
                                                              'Extend':'','Prompt':'Are you sure you want to delete ALL EventLog records?','SuccessAction':'RefreshPage'},
                                        'Process Record':{'url':"%s" % (URL('eventlog','Process',vars={'Datatable':'True'})),
                                                              'Extend':'selectedSingle','Prompt':'Are you sure you want to process this record?','SuccessAction':'RefreshRecord'},
                                        'Process All Records':{'url':"%s" % (URL('eventlog','Process',vars={'AllRecords':'True'})),
                                                              'Extend':'','Prompt':'Are you sure you want to process ALL records?','SuccessAction':'RefreshPage'}}
        dt_settings['Tabs'] = False

    elif DataTableName in ['ItemSet']:
        dt_settings['PageHeading'] = 'Item Sets'
        dt_settings['TableName'] = 'ItemSet'
        dt_settings['AuthGroups'] = ['admin','teacher']
        dt_settings['Info'] = "Media items and shop items can be grouped in 'sets'."
        dt_settings['Fields'] = ['Icon']
        dt_settings['FieldTypes'] = {'Icon':'image'}
        # dt_settings['AllFields'] = 'MainRow'
        dt_settings['common_filter'] = False
        dt_settings['UseRepresent'] = True

    elif DataTableName == 'Media':
        dt_settings['TableName'] = 'Media'
        dt_settings['PageHeading'] = 'Media'
        dt_settings['AuthGroups'] = ['admin','teacher']
        dt_settings['Fields'] = ['Icon','Description','IsWallpaper','IsCardBack','IsSuccess','IsFail','IsProgressBar','IsAvatar','IsGame','NaturalWidth','NaturalHeight']
        dt_settings['HiddenFields'] = 'Image','ThumbnailImage','created_by','modified_by'
        dt_settings['AllFields'] = 'MainRow'
        dt_settings['FieldTypes'] = {'Icon':'image','FileReference':'image'}
        dt_settings['Alignment'] = {'Icon':'dt-center'}
        dt_settings['UseRepresent'] = False      # Options: True, False
        dt_settings['Tabs'] = [{'Field':'id','Label':'General'},{'Field':'IsWallpaper','Label':'Used By'},{'Field':'NaturalWidth','Label':'Size'}]
        dt_settings['CustomButtons'] = {'Validate Record':{'url':"%s" % (URL('media','Validate',vars={'Datatable':'True','ForceUpdate':'True'})),
                                                              'Extend':'selectedSingle','Prompt':'Are you sure you want to validate this record?','SuccessAction':'RefreshRecord'},
                                        'Validate All Records':{'url':"%s" % (URL('media','Validate',vars={'AllRecords':'True'})),
                                                              'Extend':'','Prompt':'Are you sure you want to validate ALL records?','SuccessAction':'RefreshPage'}}

    elif DataTableName in ['Organisation','Organisation2']:
        dt_settings['PageHeading'] = "Organisations"
        dt_settings['TableName'] = 'Organisation'
        dt_settings['AuthGroups'] = ['admin','teacher']
        dt_settings['Alignment'] = {'id':'dt-center','ShortName':'dt-center','Active':'dt-center','Logo':'dt-center'}
        dt_settings['Fields'] = [':Users','id','Logo']
        dt_settings['Links'] = {':Users': URL('datatable','show',args=['OrganisationUserAdmin'],vars={'OrganisationID':'{id}'})}
        dt_settings['Images'] = {':Users': {'url':URL('static','img/icons/set1/svg/users.svg'),'Label':'Users'}}
        dt_settings['FieldTypes'] = {'Logo':'image'}
        dt_settings['Widths'] = {'Logo':'10px'}                 # Dictionary of field and width in pixels   
        if DataTableName == 'Organisation2':
            dt_settings['common_filter'] = False

    elif DataTableName == 'OrganisationUser' or DataTableName == 'OrganisationUserAdmin':
        dt_settings['TableName'] = 'OrganisationUser'
        dt_settings['AuthGroups'] = ['admin','teacher']
        dt_settings['UseRepresent'] = True
        dt_settings['PageHeading'] = 'Organisation Users'
        dt_settings['Fields'] = [':UserCards',':UserDecks',':UserGroups','UserID','IsTeacher','IsStudent','TotalPoints','TotalCards','DueCards','ActiveCards','LearntCards']
        dt_settings['AllFields'] = 'ChildRow'
        dt_settings['HiddenFields'] = ['!UserID']
        dt_settings['ShowReferences'] = 'All'
        dt_settings['Widths'] = {'IsTeacher':'10px','IsStudent':'10px','TotalPoints':'10px','TotalCards':'10px','DueCards':'10px','ActiveCards':'10px','LearntCards':'10px'}
        dt_settings['Tabs'] = [{'Field':'id','Label':'General'},{'Field':'IsTeacher','Label':'Type'},{'Field':'TotalPoints','Label':'Points'},{'Field':'Progress','Label':'Cards'}]
        dt_settings['TabsAdding'] = [{'Field':1,'Label':'Personal'},{'Field':9,'Label':'Address'},{'Field':13,'Label':'Organisation'},{'Field':22,'Label':'Points'},{'Field':26,'Label':'Cards'}]
        dt_settings['TabsEditing'] = dt_settings['TabsAdding']
        dt_settings['AddURL'] = URL('organisationuser','add')
        dt_settings['EditURL'] = URL('organisationuser','edit',args=['{id}'])
        dt_settings['Links'] = {':UserCards': URL('datatable','show',args=['UserCard'],vars={'StudentUserID':'{UserID}'}),
                                ':UserDecks': URL('datatable','show',args=['UserDeck2'],vars={'StudentUserID':'{UserID}'}),
                                ':UserGroups': URL('datatable','show',args=['TeachingGroupStudent2'],vars={'StudentUserID':'{UserID}'})}
        dt_settings['Images'] = {':UserCards': {'url':db.UserCard._Icon,'Label':'User Cards'},
                                ':UserDecks': {'url':db.UserDeck._Icon,'Label':'User Decks'},
                                ':UserGroups': {'url':db.TeachingGroupStudent._Icon,'Label':"User's Groups"},
                                '!UserID': {'Text':'{UserID}'}}
        dt_settings['CustomButtons'] = {'Update Statistics':{'url':"%s" % (URL('organisationuser','UpdateStatistics',vars={'StudentUserID':'{!UserID}'})),
                                                              'Extend':'selectedSingle','Prompt':None,'SuccessAction':'RefreshRecord'}}
        
        if DataTableName == 'OrganisationUserAdmin':
            dt_settings['common_filter'] = False  # Need to fix this. Should not be able to see other users easily. Need to decorate it somehow with admin group permissions.

    elif DataTableName == 'scheduler_run':
        dt_settings['PageHeading'] = "Scheduler Run"
        dt_settings['TableName'] = "scheduler_run"
        dt_settings['CustomButtons'] = {'Delete ALL records':{'url':(URL('maintenance','DeleteAll',vars={'TableName':'scheduler_run'})),
                                                              'Extend':'','Prompt':'Are you sure you want to delete ALL records?','SuccessAction':'RefreshPage'}}

    elif DataTableName == 'scheduler_task':
        dt_settings['PageHeading'] = "Scheduler Task"
        dt_settings['TableName'] = "scheduler_task"
        dt_settings['CustomButtons'] = {'Delete ALL records':{'url':(URL('maintenance','DeleteAll',vars={'TableName':dt_settings['TableName']})),
                                                              'Extend':'','Prompt':'Are you sure you want to delete ALL Task records?','SuccessAction':'RefreshPage'}}

    elif DataTableName == 'ShopItem':
        dt_settings['PageHeading'] = "Shop Items"
        dt_settings['AuthGroups'] = ['admin','teacher']
        # dt_settings['Fields'] = [':references','Icon']
        # dt_settings['ChildFields'] = [':Media']
        # dt_settings['ColumnNames'] = {":references":"Links",":Media":"Media"}
        # dt_settings['FieldTypes'] = {'Icon':'image'}
        # dt_settings['Links'] = {':Media': URL('datatable','show',args=['Media'], vars={'id':'{MediaID}'})}
        # dt_settings['Images'] = {':Media': {'url':db.Media._Icon,'Label':'Media Record'}}
        ItemCntToAdd = 10
        dt_settings['CustomButtons'] = {
                                        'Add all stock to shop':{'url':"%s" % (URL('shopitem','add_stock',vars=dict(MediaType='',TotalToAdd=9))),'Extend':'','SuccessAction':'RefreshPage','Prompt':'Are you sure you want to add all stock items?'},
                                        }

    elif DataTableName == 'StockItem':
        dt_settings['PageHeading'] = "Stock Items"
        dt_settings['AuthGroups'] = ['admin','teacher']
        dt_settings['Fields'] = [':references','Icon']
        dt_settings['ChildFields'] = [':Media']
        dt_settings['ColumnNames'] = {":references":"Links",":Media":"Media"}
        dt_settings['FieldTypes'] = {'Icon':'image'}
        dt_settings['Links'] = {':Media': URL('datatable','show',args=['Media'], vars={'id':'{MediaID}'})}
        dt_settings['Images'] = {':Media': {'url':db.Media._Icon,'Label':'Media Record'}}

        ItemCntToAdd = 10
        dt_settings['CustomButtons'] = {
                                        'Add all media to stock':{'url':"%s" % (URL('stockitem','add_all_media',vars=dict(MediaType='',TotalToAdd=ItemCntToAdd))),'Extend':'','SuccessAction':'RefreshPage','Prompt':'Are you sure you want to add all media?'},
                                        'Add extra media Avatars':{'url':"%s" % (URL('stockitem','add_all_media',vars=dict(MediaType='Avatar',TotalToAdd=ItemCntToAdd))),'Extend':'','SuccessAction':'RefreshPage','Prompt':f'Are you sure you want to add {ItemCntToAdd} Avatars?'},
                                        'Add extra media Wallpapers':{'url':"%s" % (URL('stockitem','add_all_media',vars=dict(MediaType='Wallpaper',TotalToAdd=ItemCntToAdd))),'Extend':'','SuccessAction':'RefreshPage','Prompt':f'Are you sure you want to add {ItemCntToAdd} Wallpapers?'},
                                        'Add extra media Card Backs':{'url':"%s" % (URL('stockitem','add_all_media',vars=dict(MediaType='CardBack',TotalToAdd=ItemCntToAdd))),'Extend':'','SuccessAction':'RefreshPage','Prompt':f'Are you sure you want to add {ItemCntToAdd} Card Backs?'},
                                        }

    elif DataTableName == 'TeachingGroup':
        dt_settings['PageHeading'] = "Teaching Groups"
        dt_settings['AuthGroups'] = ['admin','teacher']
        dt_settings['Fields'] = [':Students',':Decks']
        dt_settings['Links'] = {':Students': URL('datatable','show',args=['TeachingGroupStudent3'],vars={'TeachingGroupID':'{id}'}),
                                ':Decks': URL('datatable','show',args=['TeachingGroupDeck2'],vars={'TeachingGroupID':'{id}'})
                                }
        dt_settings['Images'] = {':Students': {'url':URL('static','img/icons/set1/svg/teaching_group_students.svg'),'width':'20px','Label':'Students'},
                                ':Decks': {'url':URL('static','img/icons/set1/svg/decks.svg'),'width':'20px','Label':'Decks'},
                                 }

    elif 'TeachingGroupDeck' in DataTableName:
        dt_settings['TableName'] = 'TeachingGroupDeck'
        dt_settings['AuthGroups'] = ['admin','teacher']
        dt_settings['PageHeading'] = "Group Decks"
        dt_settings['Fields'] = [':Build',':Deck',':DeckChildren',':DeckCards','DeckID','TeachingGroupID']
        dt_settings['Links'] = {':Build': URL('deckcard','DeckBuilder',args=['{DeckID}']),
                                ':Deck': URL('datatable','show',args=['Deck'],vars={'id':'{DeckID}'}),
                                ':DeckChildren': URL('datatable','show',args=['DeckChild'],vars={'DeckID':'{DeckID}'}),
                                ':DeckCards': URL('datatable','show',args=['DeckCard2'], vars={'DeckID':'{DeckID}'})}
        dt_settings['Images'] = {':Build': {'url':URL('static','img/icons/set1/svg/deck_builder4.svg'),'Label':'Build Deck'},
                                 ':Deck': {'url':db.Deck._Icon,'Label':'Deck Details'},
                                 ':DeckChildren': {'url':db.DeckChild._Icon,'Label':'Child Decks'},
                                 ':DeckCards': {'url':db.Card._Icon,'Label':'Deck Cards'}}
        if DataTableName == 'TeachingGroupDeck2':
            dt_settings['ChildFields'] = ['TeachingGroupID']
        elif DataTableName == 'TeachingGroupDeck3':
            dt_settings['Info'] = 'Groups that are learning this deck'
            dt_settings['ChildFields'] = ['DeckID']

    elif 'TeachingGroupStudent' in DataTableName:
        dt_settings['PageHeading'] = "Students in Group"
        dt_settings['AuthGroups'] = ['admin','teacher']
        dt_settings['TableName'] = 'TeachingGroupStudent'
        dt_settings['Fields'] = [':UserCards',':UserDecks',':UserGroups']
        dt_settings['Links'] = {':UserCards': URL('datatable','show',args=['UserCard'],vars={'StudentUserID':'{StudentUserID}'}),
                                ':UserDecks': URL('datatable','show',args=['UserDeck2'],vars={'StudentUserID':'{StudentUserID}'}),
                                ':UserGroups': URL('datatable','show',args=['TeachingGroupStudent2'],vars={'StudentUserID':'{StudentUserID}'})}
        dt_settings['Images'] = {':UserCards': {'url':db.UserCard._Icon,'Label':'User Cards'},
                                ':UserDecks': {'url':db.UserDeck._Icon,'Label':'User Decks'},
                                ':UserGroups': {'url':db.TeachingGroupStudent._Icon,'Label':"User's Groups"}}

        if DataTableName == 'TeachingGroupStudent2':
            dt_settings['PageHeading'] = "Student is in these Groups"
            dt_settings['Fields'] += ['id','IsEnrolled']
            dt_settings['ChildFields'] = ['StudentUserID']
        if DataTableName == 'TeachingGroupStudent3':
            dt_settings['PageHeading'] = "Students in this Group"
            dt_settings['Fields'] += ['id','IsEnrolled']
            dt_settings['ChildFields'] = ['TeachingGroupID']

    elif DataTableName == 'UploadTemplate':
        dt_settings['PageHeading'] = "Upload Template"
        dt_settings['DisabledFields'] = ['OriginalFilename']
        dt_settings['ShowFooter'] = False
        dt_settings['ShowSearch'] = 'None'
        dt_settings['ShowPageButtons'] = 'Top'
        dt_settings['ShowSearch'] = 'Top'
        
    elif DataTableName in ['UserCard','UserCard2']:
        dt_settings['TableName'] = 'UserCard'
        dt_settings['PageHeading'] = 'User Cards'
        dt_settings['AuthGroups'] = ['admin','teacher']
        dt_settings['Fields'] = [':Decks',':CardHistory',':Card',':MultiChoice','CardID','Status']
        dt_settings['Links'] = {':Decks': URL('datatable','show',args=['CardDecks'],vars={'CardID':'{CardID}'}),
                                ':CardHistory': URL('datatable','show',args=['UserCardHistory'],vars={'UserCardID':'{id}'}),
                                ':Card': URL('datatable','show',args=['Card'],vars={'id':'{CardID}'}),
                                ':MultiChoice': URL('learn','StudyCardsMultiChoice',vars={'UserCardID':'{id}'})}
        dt_settings['Images'] = {':Decks': {'url':URL('static','img/icons/set1/svg/deck4.svg'),'Label':'Decks the card is in'},
                                 ':CardHistory': {'url':URL('static','img/icons/set1/svg/card_history.svg'),'Label':'Card History'},
                                 ':Card': {'url':db.Card._Icon,'Label':'Card Details'},
                                 ':MultiChoice': {'url':db.UserCard._StudyMultiChoiceIcon,'Label':'Study Multichoice'}}
        dt_settings['CustomButtons'] = {'Study Card (Multichoice)':{'url':URL('learn','StudyCardsMultiChoice',vars={"UserCardID":"{id}"}),'Extend':'selectedSingle','SuccessAction':'ImmediateRedirect'}}
        if DataTableName == 'UserCard2':
            dt_settings['ChildFields'] = ['StudentUserID']

    elif DataTableName in ['UserDeck','UserDeck2']:
        dt_settings['TableName'] = 'UserDeck'
        dt_settings['AuthGroups'] = ['admin','teacher']
        dt_settings['Info'] = 'All the decks that have been assigned to the user. This may include decks that were assigned through a group that the student is no longer a member of.'
        dt_settings['PageHeading'] = 'User Decks'
        dt_settings['UseRepresent'] = True
        dt_settings['Fields'] = [':Cards',':Deck','DeckID']
        dt_settings['HiddenFields'] = ['!DeckID','!StudentUserID']
        dt_settings['CustomButtons'] = {'Update User Deck Statistics':{'url':"%s?UserID={!StudentUserID}&DeckID={!DeckID}" % (URL('userdeck','UpdateUserDeckStatistics'))}}
        dt_settings['Links'] = {':Cards': URL('datatable','show',args=['DeckCard2'],vars={'DeckID':'{DeckID}'}),
                                ':Deck': URL('datatable','show',args=['Deck'],vars={'id':'{DeckID}'})}
        dt_settings['Images'] = {':Cards': {'url':db.DeckCard._Icon,'Label':'Cards associated directly with this deck'},
                                ':Deck': {'url':db.Deck._Icon,'Label':'Deck Details'},
                                '!DeckID': {'Text':'{DeckID}'}, '!StudentUserID':{'Text':'{StudentUserID}'}}

    elif DataTableName in ['UserItem','UserItem2']:
        dt_settings['TableName'] = 'UserItem'
        dt_settings['AuthGroups'] = None
        dt_settings['PageHeading'] = 'User Items'
        dt_settings['EditURL'] = 'IncludeVars'
        dt_settings['AddURL'] = 'IncludeVars'
        if DataTableName in ['UserItem2']:
            dt_settings['HiddenFields'].append('OrganisationUserID')

    elif DataTableName == 'UserOrganisations':
        dt_settings['TableName'] = 'OrganisationUser'
        dt_settings['AuthGroups'] = ['admin','teacher']
        dt_settings['UseRepresent'] = True
        dt_settings['PageHeading'] = 'User Organisations'
        dt_settings['Fields'] = ['OrganisationID','IsTeacher','IsStudent','DateStart','DateEnd','TotalPoints']
        dt_settings['AllFields'] = 'ChildRow'
        dt_settings['Widths'] = {'TotalPoints':'10px'}
        dt_settings['EditURL'] = URL('datatable','edit', args=[DataTableName,'{id}']) + '?{VARS}'  # Use the default add method but pass it the variables from the current page in order to set the form default
        dt_settings['AddURL'] = URL('datatable','add', args=[DataTableName]) + '?{VARS}'  # Use the default add method but pass it the variables from the current page in order to set the form default
        dt_settings['common_filter'] = False

    elif 'Example' in DataTableName:
        if DataTableName == 'Example1':
            dt_settings['TableName'] = 'OrganisationUser'
            dt_settings['PageHeading'] = DataTableName
            dt_settings['Info'] = f"All defaults applied including the Common Filter"  
        elif DataTableName == 'Example2':
            dt_settings['PageHeading'] = DataTableName
            dt_settings['TableName'] = 'OrganisationUser'
            dt_settings['common_filter'] = False
            dt_settings['Fields'] = 'TotalPoints','Gold','Silver','Bronze' 
            dt_settings['Info'] = f"Rearrange fields. Fields={dt_settings['Fields']} | No Common Filter"  
        elif DataTableName == 'Example3':
            dt_settings['PageHeading'] = DataTableName 
            dt_settings['TableName'] = 'OrganisationUser'
            dt_settings['Fields'] = 'UserID','TotalPoints'
            dt_settings['AllFields'] = 'ChildRow'
            dt_settings['Info'] = "Show other fields in child row. AllFields='ChildRow' "  
        elif DataTableName == 'Example4':
            dt_settings['PageHeading'] = DataTableName
            dt_settings['TableName'] = 'OrganisationUser'
            dt_settings['Fields'] = 'UserID','TotalPoints','id'
            dt_settings['AllFields'] = ''
            dt_settings['Widths'] = {'TotalPoints':'10px','id':'200px'}
            dt_settings['ControlFields'] = [':edit']
            dt_settings['ShowReferences'] = False
            dt_settings['Info'] = f"AllFields='' | Fields={dt_settings['Fields']} | Widths={dt_settings['Widths']} | ControlFields={dt_settings['ControlFields']} | ShowReferences=False"
        elif DataTableName == 'Example5':
            dt_settings['PageHeading'] = DataTableName 
            dt_settings['TableName'] = 'OrganisationUser'
            dt_settings['Fields'] = 'UserID','TotalPoints','id'
            dt_settings['Orderable'] = 'UserID','TotalPoints','TotalGold'
            dt_settings['Info'] = f"Enable ordering on specific fields. | Orderable={dt_settings['Orderable']}"
        elif DataTableName == 'Example6':
            dt_settings['PageHeading'] = DataTableName 
            dt_settings['TableName'] = 'OrganisationUser'
            dt_settings['Fields'] = 'UserID','TotalPoints','id'
            dt_settings['Orderable'] = 'UserID','TotalPoints','TotalGold'
            dt_settings['Searchable'] = 'OrganisationID','TotalSilver','Teacher'
            dt_settings['Info'] = f"Enable searching on specific fields. | Searchable={dt_settings['Searchable']}"
        elif DataTableName == 'Example7':
            dt_settings['TableName'] = 'OrganisationUser'
            dt_settings['Fields'] = 'UserID','TotalPoints','id'
            dt_settings['Orderable'] = 'UserID','TotalPoints','TotalGold'
            dt_settings['Searchable'] = 'OrganisationID','Teacher','TotalSilver','Teacher'
            dt_settings['Widths'] = {'id':'300px'}
            dt_settings['Responsive'] = False
            dt_settings['PageHeading'] = DataTableName 
            dt_settings['Info'] = f"Responsive=False | Widths (doesn't work) = {dt_settings['Widths']}"
        elif DataTableName == 'Example8':
            dt_settings['PageHeading'] = DataTableName
            dt_settings['TableName'] = 'OrganisationUser'
            dt_settings['Fields'] = 'UserID','TotalPoints','id'
            dt_settings['Orderable'] = 'UserID','TotalPoints','TotalGold'
            dt_settings['Searchable'] = 'OrganisationID','Teacher','TotalSilver','Teacher'
            dt_settings['Icon'] = URL('static','img/icons/set1/svg/idea.svg')
            dt_settings['Info'] = f"Set an icon | Icon=url...  Normally it comes from the table definition '_Icon' property"
        elif DataTableName == 'Example9':
            dt_settings['PageHeading'] = DataTableName 
            dt_settings['TableName'] = 'OrganisationUser'
            dt_settings['Fields'] = 'UserID','TotalPoints','id'
            dt_settings['Orderable'] = 'UserID','TotalPoints','TotalGold'
            dt_settings['Searchable'] = 'OrganisationID','IsTeacher','TotalSilver','Teacher'
            dt_settings['Icon'] = URL('static','img/icons/set1/svg/idea.svg')
            dt_settings['ChildFields'] = ['OrganisationID']
            dt_settings['Info'] = f"Force fields into the child section | ChildFields= 'OrganisationID'"
        elif DataTableName == 'Example10':
            dt_settings['PageHeading'] = DataTableName 
            dt_settings['TableName'] = 'OrganisationUser'
            dt_settings['Fields'] = ':UserCards','User Decks'
            dt_settings['Links'] = {':UserCards': URL('datatable','show',args=['UserCard'],vars={'StudentUserID':'{UserID}'}),
                                    'User Decks': URL('datatable','show',args=['UserDeck'],vars={'StudentUserID':'{UserID}'}),}
            dt_settings['Images'] = {':UserCards': {'url':URL('static','img/icons/set1/svg/cards2.svg')}}
            dt_settings['Info'] = f"Add links (images and text)"
        elif DataTableName == 'Example11':
            dt_settings['PageHeading'] = DataTableName 
            dt_settings['TableName'] = 'OrganisationUser'
            # dt_settings['Tabs'] = [{'Field':'id','Label':'General'},{'Field':'IsTeacher','Label':'Type'},{'Field':'TotalPoints','Label':'Points'},{'Field':'Progress','Label':'Cards'}]
            dt_settings['TabsAdding'] = [{'Field':1,'Label':'Add Personal'},{'Field':9,'Label':'Add Address'},{'Field':13,'Label':'Organisation'},{'Field':22,'Label':'Points'},{'Field':26,'Label':'Cards'}]
            dt_settings['TabsEditing'] = [{'Field':1,'Label':'Edit Personal'},{'Field':9,'Label':'Edit Address'},{'Field':13,'Label':'Organisation'},{'Field':22,'Label':'Points'},{'Field':26,'Label':'Cards'}]
            dt_settings['Info'] = f"Labeling add and edit dialog tabs"

    return dt_settings
