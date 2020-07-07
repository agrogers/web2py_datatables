# from copy import copy
# from copy import deepcopy
# import simplejson as json
from datetime import datetime
# from timer import Timer
# from random import randrange

pyFileName = "common_datatable.py"

# if False:
#     from gluon import *
    # request = current.request
    # response = current.response
    # session = current.session
    # cache = current.cache
    # T = current.T


# Default values for specific tables in this model
def TableDefaults(DataTableName, dt_settings={}):

    dt_settings['DataTableName'] = DataTableName
    dt_settings['TableName'] = DataTableName

    if DataTableName == 'ALL Settings in Alphabetical order':
        dt_settings['AddURL'] = ''                              # The URL of the controller which supplies the form for the 'add' dialog.
        dt_settings['EditURL'] = ''                             # The URL of the controller which supplies the form for the 'edit' dialog.
        dt_settings['Alignment'] = {}                           # Options: {'id':'dt-center','fldname':'dt-right'}.  Specify the alignment of cell text in the column. By default 'id','boolean','integer','double','date','time','datetime','big-int','big-id' are centred.
        dt_settings['AllFields'] = 'ChildRow'                   # Options: 'ChildRow', 'MainRow', ''. This determines if we include every field (not defined elsewhere) and where to place them.
        dt_settings['BooleanReplacment'] = {True:'Yes', False:'No',None:'No'}       # Dictionary for True, False, None.  We add hidden text to checkbox fields so that we can search on that field. The dictionary determines what hidden text is included.
        dt_settings['Buttons'] = ['delete','add','edit']        # all, add, delete, edit, print 
        dt_settings['ChildFields'] = []                         # Options: a list of field names.  Forces those fields into the expandable datatable child row
        dt_settings['ColumnNames'] = {":Build":"Build"}         # Dictionary of fieldnames and column names. Sets the column heading to the value specified.
        dt_settings['common_filter'] = True                     # Ignore the common_filter set in the table definition used to restrict what records are returned
        dt_settings['ControlFields'] = [':control',':edit']     # Special fields that are usually added to the left side of the grid.
        dt_settings['ControlLinks'] = {':edit': 'edit_dialog'}  # Dictionary indicating what control fields link to. 'edit_dialog' identifies the default edit dialog.
        dt_settings['DisabledFields'] = []                      # Which fields should be displayed disabled in the edit and add forms.
        dt_settings['DOM'] = ''                                 # See Datatables.net for info  Example: 'Bprf<t>ip'. This value overrides the Show options below.
        dt_settings['ElementID'] = f'DT-{DataTableName}'        # 'ElementID': This must remain the same if you want the state of the table to be restored.
        dt_settings['Fields'] = [':Organisations']              # A list of table and special fields. It allows for custom ordering of fields. Fieldnames that start with a ':' are treated differently (by default their width is set to 10px, type is set to Boolean, it is not searchable or orderable)
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
        dt_settings['Tabs'] = True                              # Options: True, False.  Shows tabs in the add and edit dialog.
        dt_settings['UseRepresent'] = True                      # Options: True, False.  Uses the Represent settings in the table to render records. Disabling this can improve rendering time significantly
        dt_settings['Widths'] = {'FieldName':'10px'}            # Dictionary of field and width in pixels

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
        dt_settings['Fields'] = [':Decks',':CardMaster',':FullDetails','Preview']
        dt_settings['ChildFields'] = ['FrontFaceStructure','BackFaceStructure','FrontFaceRendered','BackFaceRendered']
        dt_settings['Links'] = {':Decks': URL('datatable','show',args=['CardDecks'],vars={'CardID':'{id}'}),
                                ':CardMaster': URL('datatable','show',args=['CardMaster'],vars={'id':'{CardMasterID}'}),
                                ':FullDetails': URL('card','FullCardDetails',args=['{id}']),
                                'Preview': URL('card','preview',args=['{id}'])
                                }
        dt_settings['Images'] = {':Decks': {'url':URL('static','img/icons/set1/svg/deck6.svg')},
                                ':CardMaster': {'url':URL('static','img/icons/set1/svg/cardmaster.svg')},
                                ':FullDetails': {'url':URL('static','img/icons/set1/svg/full_card_details.svg')},
                                'Preview': {'url':URL('static','img/icons/set1/svg/full_card_details.svg')}
                                }

    elif DataTableName == 'CardCategory':
        dt_settings['PageHeading'] = 'Card Categories'
        dt_settings['TableName'] = 'CardCategory'
        dt_settings['Fields'] = [':Cards']
        dt_settings['Links'] = {':Cards': URL('datatable','show',args=['CardMaster'],vars={'Categories':'{LongName}'})}
        dt_settings['Images'] = {':Cards': {'url':URL('static','img/icons/set1/svg/cards.svg')}}
        dt_settings['UseRepresent'] = False

    elif DataTableName == 'CardDecks':
        dt_settings['PageHeading'] = 'Decks where this card is found'
        dt_settings['TableName'] = 'DeckCard'

    elif DataTableName in ['CardMaster','CardMaster2']:
        dt_settings['PageHeading'] = 'Card Master'
        dt_settings['TableName'] = 'CardMaster'
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
        dt_settings['Info'] = 'The content used to construct a card. The final card may inlcude some or all of these records.'
        dt_settings['AllFields'] = 'MainRow'
        dt_settings['common_filter'] = False
        dt_settings['UseRepresent'] = True
        if DataTableName in ['CardMasterContent2']:
            dt_settings['Fields'] = ['ContentText','ContentType']
            dt_settings['ChildFields'] = ['id', 'RelatedCards']
            dt_settings['HiddenFields'] = ['CardMasterID']
            dt_settings['PageLength'] = 9999
            dt_settings['ShowFooter'] = False
            dt_settings['Searchable'] = ['None']

    elif DataTableName == 'CardStructure':
        dt_settings['Fields'] = [':Cards','LongName', 'ShortName','Lang']
        dt_settings['PageHeading'] = DataTableName 
        dt_settings['ChildFields'] = ['FrontFaceStructure','BackFaceStructure']
        dt_settings['Links'] = {':Cards': URL('datatable','show',args=['Card'], vars={'CardStructureID':'{id}'})}
        dt_settings['Images'] = {':Cards': {'url':URL('static','img/icons/set1/svg/cards2.svg'),'width':'16px'}}

    elif DataTableName == 'ContentType':
        dt_settings['PageHeading'] = 'Content Types' 
        dt_settings['PageLength'] = 999
        dt_settings['ShowPageButtons'] = 'None'

    elif DataTableName == 'Deck':
        dt_settings['PageHeading'] = "Decks"
        dt_settings['Fields'] = [':Build',':DeckChildren',':Cards','LongName','CardCriteria','ChildDeckIDList','ParentDeckIDList','DefaultCardStructureID','is_active','id', 'created_by']
        dt_settings['Orderable'] = ['LongName','ShortName','CardCriteria','id']
        dt_settings['ColumnNames'] = {":Build":"Build", ":Cards":"Cards", ":DeckChildren":"Child",":control":""}
        dt_settings['HiddenFields'] = ['ChildDeckIDList']
        dt_settings['PrependText'] = {':control': ''}
        dt_settings['Searchable'] = ['LongName','ShortName','CardCriteria','ChildDeckIDList','ParentDeckIDList','DefaultCardStructureID']
        dt_settings['Widths'] = {'ParentDecks':'1px'}
        dt_settings['UseTabs'] = [{'Field':'id','Label':'General'},{'Field':'ChildDeckIDList','Label':'Related Decks'},{'Field':'QuestionCardSize','Label':'Sizes'},{'Field':'PresentationOptions','Label':'Other'}]
        dt_settings['Links'] = {':Build': URL('deckcard','DeckBuilder',args=['{id}']),
                                ':Cards': URL('datatable','show',args=['DeckCard'], vars={'DeckID':'{id}'}),
                                ':DeckChildren': URL('datatable','show',args=['DeckChild'], vars={'DeckID':'{id}'})
                                }
        dt_settings['Images'] = {   ':Build': {'url':URL('static','img/icons/set1/svg/deck_builder4.svg'),'Label':'Build Deck'},
                                    ':Cards': {'url':URL('static','img/icons/set1/svg/cards.svg'),'Label':'Deck Cards'},
                                    ':DeckChildren': {'url':URL('static','img/icons/set1/svg/deck_children.svg'),'Label':'Child Decks'}
                                    }

    elif DataTableName == 'DeckCard':
        dt_settings['Fields'] = [':Card']
        dt_settings['PageHeading'] = 'Deck Cards'
        dt_settings['Info'] = 'What decks does this card appear in.'
        dt_settings['UseRepresent'] = True
        dt_settings['Links'] = {':Card': URL('datatable','show',args=['Card'], vars={'id':'{CardID}'})}
        dt_settings['Images'] = {':Card': {'url':URL('static','img/icons/set1/svg/single_card.svg'),'width':'16px'}}

    elif DataTableName == 'DeckChild':
        dt_settings['Fields'] = [':DeckChildren']
        dt_settings['PageHeading'] = 'Deck Children'
        dt_settings['EditURL'] = 'IncludeVars'
        dt_settings['AddURL'] = 'IncludeVars'
        dt_settings['Links'] = {
                                ':DeckChildren': URL('datatable','show',args=['DeckChild'], vars={'DeckID':'{ChildDeckID}'})
                                }
        dt_settings['Images'] = {
                                ':DeckChildren': {'url':URL('static','img/icons/set1/svg/deck_children.svg')}
                                }

    elif DataTableName == 'EventLog':
        dt_settings['PageHeading'] = 'Event Log'
        dt_settings['Fields'] = ['id','created_on','LogType','LogFunction','EventAction','ObjectID','UserID']
        dt_settings['AllFields'] = 'MainRow'
        dt_settings['HiddenFields'] = ['created_by','modified_by','modified_on']
        dt_settings['common_filter'] = False

    elif DataTableName == 'Media':
        dt_settings['TableName'] = 'Media'
        dt_settings['PageHeading'] = 'Media'
        dt_settings['Fields'] = ['Icon','Description','IsWallpaper','IsCardBack','IsSuccessSound','IsFailSound','IsProgressBar','IsAvatar','IsGame','NaturalWidth','NaturalHeight']
        dt_settings['HiddenFields'] = 'Image','ThumbnailImage','created_by','modified_by'
        dt_settings['AllFields'] = 'MainRow'
        dt_settings['FieldTypes'] = {'Icon':'image','FileReference':'image'}
        dt_settings['Alignment'] = {'Icon':'dt-center'}
        dt_settings['UseRepresent'] = False      # Options: True, False

    elif DataTableName in ['Organisation','Organisation2']:
        dt_settings['PageHeading'] = "Organisations"
        dt_settings['TableName'] = 'Organisation'
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
        dt_settings['UseRepresent'] = True
        dt_settings['PageHeading'] = 'Organisation Users'
        dt_settings['Fields'] = [':UserCards',':UserDecks','UserID','IsTeacher','IsStudent','TotalPoints','TotalCards','DueCards','ActiveCards','LearntCards']
        dt_settings['AllFields'] = 'ChildRow'
        dt_settings['ShowReferences'] = 'All'
        dt_settings['Widths'] = {'IsTeacher':'10px','IsStudent':'10px','TotalPoints':'10px','TotalCards':'10px','DueCards':'10px','ActiveCards':'10px','LearntCards':'10px'}
        dt_settings['Tabs'] = [{'Field':'id','Label':'General'},{'Field':'IsTeacher','Label':'Type'},{'Field':'TotalPoints','Label':'Points'},{'Field':'Progress','Label':'Cards'}]
        dt_settings['TabsAdding'] = [{'Field':1,'Label':'Personal'},{'Field':9,'Label':'Address'},{'Field':13,'Label':'Organisation'},{'Field':22,'Label':'Points'},{'Field':26,'Label':'Cards'}]
        dt_settings['TabsEditing'] = dt_settings['TabsAdding']
        dt_settings['AddURL'] = URL('organisationuser','add')
        dt_settings['EditURL'] = URL('organisationuser','edit',args=['{id}'])
        dt_settings['Links'] = {':UserCards': URL('datatable','show',args=['UserCard'],vars={'StudentUserID':'{UserID}'}),
                                ':UserDecks': URL('datatable','show',args=['UserDeck'],vars={'StudentUserID':'{UserID}'}),}
        dt_settings['Images'] = {':UserCards': {'url':URL('static','img/icons/set1/svg/cards2.svg')},
                                ':UserDecks': {'url':URL('static','img/icons/set1/svg/decks.svg')}}
        
        if DataTableName == 'OrganisationUserAdmin':
            dt_settings['common_filter'] = False  # Need to fix this. Should not be able to see other users easily. Need to decorate it somehow with admin group permissions.

    elif DataTableName == 'StockItem':
        dt_settings['PageHeading'] = "Stock Items"
        dt_settings['Fields'] = [':references']
        dt_settings['ColumnNames'] = {":references":"Links"}

    elif DataTableName == 'TeachingGroup':
        dt_settings['PageHeading'] = "Teaching Groups"
        dt_settings['Fields'] = [':Students',':Decks']
        dt_settings['Links'] = {':Students': URL('datatable','show',args=['TeachingGroupStudent'],vars={'TeachingGroupID':'{id}'}),
                                ':Decks': URL('datatable','show',args=['TeachingGroupDeck2'],vars={'TeachingGroupID':'{id}'})
                                }
        dt_settings['Images'] = {':Students': {'url':URL('static','img/icons/set1/svg/teaching_group_students.svg'),'width':'20px','Label':'Students'},
                                ':Decks': {'url':URL('static','img/icons/set1/svg/decks.svg'),'width':'20px','Label':'Decks'},
                                 }

    elif DataTableName in ['TeachingGroupDeck', 'TeachingGroupDeck2']:
        dt_settings['TableName'] = 'TeachingGroupDeck'
        dt_settings['PageHeading'] = "Group Decks"
        dt_settings['Fields'] = [':Build',':Deck','DeckID','TeachingGroupID']
        dt_settings['Links'] = {':Build': URL('deckcard','DeckBuilder',args=['{DeckID}']),
                                ':Deck': URL('datatable','show',args=['Deck'],vars={'id':'{DeckID}'})}
        dt_settings['Images'] = {':Build': {'url':URL('static','img/icons/set1/svg/deck_builder4.svg'),'Label':'Build Deck'},
                                 ':Deck': {'url':URL('static','img/icons/set1/svg/deck5.svg'),'Label':'Deck Details'}}
        if DataTableName == 'TeachingGroupDeck2':
            dt_settings['ChildFields'] = ['TeachingGroupID']

    elif DataTableName == 'TeachingGroupStudent':
        dt_settings['PageHeading'] = "Students in Group"

    elif DataTableName == 'UploadTemplate':
        dt_settings['PageHeading'] = "Upload Template"
        dt_settings['DisabledFields'] = ['OriginalFilename']
        dt_settings['ShowFooter'] = False
        dt_settings['ShowSearch'] = 'None'
        dt_settings['ShowPageButtons'] = 'Top'
        dt_settings['ShowSearch'] = 'Top'
        
    elif DataTableName == 'UserCard':
        dt_settings['TableName'] = 'UserCard'
        dt_settings['PageHeading'] = 'User Cards'
        dt_settings['Fields'] = [':Decks',':CardHistory']
        dt_settings['ChildFields'] = ['id']
        dt_settings['Links'] = {':Decks': URL('datatable','show',args=['CardDecks'],vars={'CardID':'{CardID}'}),
                                ':CardHistory': URL('datatable','show',args=['UserCardHistory'],vars={'UserCardID':'{id}'})}
        dt_settings['Images'] = {':Decks': {'url':URL('static','img/icons/set1/svg/deck4.svg')},
                                 ':CardHistory': {'url':URL('static','img/icons/set1/svg/card_history.svg')}}

    elif DataTableName == 'UserDeck':
        dt_settings['TableName'] = 'UserDeck'
        dt_settings['PageHeading'] = 'User Decks'
        dt_settings['UseRepresent'] = True
        dt_settings['Fields'] = ['DeckID',':Cards']
        dt_settings['HiddenFields'] = ['StudentUserID']
        dt_settings['ChildFields'] = ['id']
        dt_settings['Links'] = {':Cards': URL('datatable','show',args=['DeckCard'],vars={'DeckID':'{DeckID}'})}
        dt_settings['Images'] = {':Cards': {'url':URL('static','img/icons/set1/svg/cards2.svg')}}

    elif DataTableName == 'UserItem':
        dt_settings['TableName'] = 'UserItem'
        dt_settings['PageHeading'] = 'User Items'
        dt_settings['EditURL'] = 'IncludeVars'
        dt_settings['AddURL'] = 'IncludeVars'

    elif DataTableName == 'UserOrganisations':
        dt_settings['TableName'] = 'OrganisationUser'
        dt_settings['UseRepresent'] = True
        dt_settings['PageHeading'] = 'User Organisations'
        dt_settings['Fields'] = ['OrganisationID','IsTeacher','IsStudent','DateStart','DateEnd','TotalPoints']
        dt_settings['AllFields'] = 'ChildRow'
        dt_settings['Widths'] = {'TotalPoints':'10px'}
        dt_settings['EditURL'] = URL('datatable','edit', args=[DataTableName,'{id}']) + '?{VARS}'  # Use the default add method but pass it the variables from the current page in order to set the form default
        dt_settings['AddURL'] = URL('datatable','add', args=[DataTableName]) + '?{VARS}'  # Use the default add method but pass it the variables from the current page in order to set the form default
        dt_settings['common_filter'] = False

    elif DataTableName == 'Example1':
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
