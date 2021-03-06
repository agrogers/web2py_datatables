import datetime
import os
# -*- coding: utf-8 -*-

def my_string_widget(field, value, x):  # Example - not being used
    return INPUT(_name=field.name,
                 _id="%s_%s" % (field.tablename, field.name),
                 _class=field.type,
                 _value=value,
                 requires=field.requires)

def FileSelector_widget(field, value, x):  # Selects a file
    
    if field.tablename == "UploadTemplate" and field.name == "FileReference":
        OriginalFilename = "OriginalFilename"  # Yes, this is not needed. Just here to remind me what to do if i use this widget with other upload fields that use a different original filename field.
    else:
        OriginalFilename = "OriginalFilename"

    html = f"""<input type="file"  class="input-file upload" id="{field.tablename}_{field.name}_select" name="{field.name}" onchange="document.getElementById('{field.tablename}_{OriginalFilename}').value = this.files.length > 0 ? this.files[0].name : 'Select a file'" /> """

    return XML(html)

# Media widget - allows selecting a media item using a popup modal
def media_widget(field, value):
    rec = db.Media[value]
    display_value = value
    html = INPUT(_name=field.name,
                    _id="%s_%s" % (field.tablename, field.name),
                    _class=field.type,
                    _value=display_value,
                    requires=field.requires,
                    _type="hidden"
                    )
    
    icon_src = icon_description = ''
    if rec:
        icon_src = URL('default','image_download', args=rec.Icon)
        icon_description = rec.Description
    html += IMG(_id='MediaIcon', _src=icon_src, _style='width:50px; padding-right:10px')
    html += SPAN(icon_description, _id='MediaDescription')
    html += A('Select Item', _href="#image-selector-dialog", _style="float: right", _class="btn btn-primary", **{'_data-toggle':"modal", '_data-backdrop':'static'})  
        
    return html


db.define_table('Media',
    Field('Description', length=255),
    # Field('OriginalFileName', length=255, label='Filename'),  # Remove this one
    Field('OriginalFilename', length=255, label='Filename'),
    Field('FileReference', 'upload', uploadseparate=True, autodelete=True, length=200, label='File', widget=FileSelector_widget),  # uploadfolder=request.folder +'/static/', requires=IS_NOT_EMPTY() and IS_IMAGE(extensions=('jpeg', 'png','jpg','tif'))), 
    # Field('ThumbnailReference', type='upload', autodelete=True, length=200, label='Thumbnail'),  # compute=lambda row: MakeThumbnailImage(row.FileReference, (100,100))), # ThumbnailReference holds a small version of the image or an icon for the type of media.
    Field('Icon', length=200, label='Icon'),  # Has the URL to a small version of the media file. For images this is a thumbnail created when the image is added. For other types, it is a URL to an icon that represents the type.
    Field('MediaType', type='list:string', requires=IS_IN_SET(['Image', 'Audio', 'Video','Document'], multiple=False, zero=None), label='Type', ),  #  default=lambda r: DetermineMediaRepresentation(r,'Text')),
    Field('IsWallpaper', type='boolean', default=False, label='Wallpaper'),
    Field('IsCardBack', type='boolean', default=False, label='Card Back'),
    Field('IsSuccessSound', type='boolean', default=False, label='Success Sound'),
    Field('IsFailSound', type='boolean', default=False, label='Fail Sound'),
    Field('IsProgressBar', type='boolean', default=False, label='Progress Bar'),
    Field('IsAvatar', type='boolean', default=False, label='Avatar'),
    Field('IsGame', type='boolean', default=False, label='Game'),
    Field('NaturalWidth', type='integer', default=None, label='Width'),
    Field('NaturalHeight', type='integer', default=None, label='Height'),
    Field('Settings'),
    format = '%(Description)s')
db.Media._Icon = '/smartdeck/static/img/icons/set1/svg/media.svg'

db.define_table('ContentType',
    Field('LongName', required=True, length=255),
    Field('ShortName'),
    format = '%(LongName)s',
    singular="Content Type", plural="Content Types",
#     migrate=False
)
db.ContentType._Icon = URL('static', '/img/icons/set1/svg/content_types.svg')

db.define_table('Organisation',
    Field('LongName', required=True, length=255, label='Name'),
    Field('ShortName', length=255),
    Field('email'),
    Field('PreferredLanguage','list:reference Languages', label='Language'),
    Field('isactive', 'boolean', required=True, default=True, label='Active'),
    Field('Logo','upload', uploadseparate=True, autodelete=True, length=200),
    Field('DefaultAvatar', type='integer', required=False, default=None, requires=IS_EMPTY_OR(IS_IN_DB(db, 'StockItem.id', '%(Description)s')), label='Default Avatar'),
    Field('DefaultWallpaper', type='integer', required=False, default=None, requires=IS_EMPTY_OR(IS_IN_DB(db, 'StockItem.id', '%(Description)s')), label='Default Wallpaper'),
    format = '%(ShortName)s (%(LongName)s)',
    singular="Organisation", plural="Organisations",
    migrate=True)
db.Organisation._Icon = '/smartdeck/static/img/icons/set1/svg/organisations.svg'

db.define_table('OrganisationUser', 
    Field('OrganisationID',db.Organisation, label='Organisation', default=session.OrganisationID),
    Field('UserID',db.auth_user, label='User'),
    Field('AvatarStockItemID',type='integer', label='Avatar'),          # The avatar must be one owned by the user
    Field('WallpaperStockItemID',type='integer', label='Wallpaper'),    # The wallpaper must be one owned by the user 
    Field('auth_group_id',db.auth_group),
    Field('SMSid', label='School ID'),
    Field('DateStart',type='date', label='Started'),
    Field('DateEnd',type='date', label='Finished'),
    Field('IsTeacher','boolean', required=True, default=False, label='Teacher'),
    Field('IsStudent','boolean', required=True, default=True, label='Student'),
    Field('IsActive', 'boolean', required=True, default=True, label='Active'),
    Field('Status', type='string', label='Status'),  # ??? Might be useful
    Field('TotalPoints', type='integer', default=0, label='Pts'),
    Field('TotalGold', type='integer', default=0, label='Gold'),
    Field('TotalSilver', type='integer', default=0, label='Silver'),
    Field('TotalBronze', type='integer', default=0, label='Bronze'),
    Field('Progress',type='integer', required=False, default=None, label='Progress'),  # Percent Progress
    Field('TotalCards',type='integer', required=False, default=0, label='Total Cards'),
    Field('DueCards',type='integer', required=False, default=0, label='Due Cards'),
    Field('ActiveCards',type='integer', required=False, default=0, label='Active Cards'),  # A card that the student has begun to learn (has an interval)
    Field('LearntCards',type='integer', required=False, default=0, label='Learnt Cards'),
    Field('ReviewCount',type='integer', required=False, default=0, label='Reviews'),
    Field('CorrectCount',type='integer', required=False, default=0, label='#Correct'),
    Field('AvgStreak',type='double', required=False, default=0, label='Avg Streak'), 
    Field('AvgCurrentInterval',type='double', required=False, default=0, label='Avg Interval'),
    Field('AvgDifficulty', type='decimal(3,1)', required=False, default=0, label='Avg Difficulty'),  # A scale of 0 to 10 with 10 being the most difficult
    Field('LastReview',type='datetime', required=False, default=None, label='Last Review'),
    Field('Selected', type='boolean', default=False),
    format = lambda r: ("%s [%s]") % (db.auth_user(r.UserID).DisplayName, db.Organisation(r.OrganisationID).ShortName),    
    # migrate=False,
    singular="Organisation User", plural="Organisation Users",
)
db.OrganisationUser._Icon = '/smartdeck/static/img/icons/set1/svg/organisation_user.svg'

db.define_table('CardCategory',
    Field('LongName', required=True, label='Name'),
    Field('ShortName'),
    format = '%(LongName)s',
    singular="Card Category", plural="Card Categories")
db.CardCategory._Icon = '/smartdeck/static/img/icons/set1/svg/categories.svg'
        
# ----- Card Master table-----
# A CardMaster is the parent record for each item of content that relates to that card.
db.define_table('CardMaster',
    Field('Name'),
    Field('Categories', 'list:string'),
    Field('Description'),
    # format = '%(Name)s'  + '(%(Description)s)' if Description,
    format = lambda r: f"{r.Name}" + (f" ({r.Description})" if r.Description else ''),
#     migrate=False,
    singular="Card Master", plural="Card Masters")
db.CardMaster._Icon = '/smartdeck/static/img/icons/set1/svg/cardmaster.svg'

# ----- Card Master Content table-----
# The content that makes up a CardMaster. A CardMaster can have any number of content items. 
# A Card is constructed by using these items to make two faces. A face could have one or more items on it.
db.define_table('CardMasterContent',
    Field('CardMasterID',db.CardMaster, label='Card Master ID', required=True),
    Field('Lang', label='Language', default='-'),
    Field('LangWrittenIn', label='Written In', default='-'),
    Field('ContentType',label='Type', default='-'),
    Field('ContentMediaID',db.Media, label='Media ID'),
    Field('ContentText',label='Text', 
            widget= lambda field, value: SQLFORM.widgets.text.widget(field, value, _class='textbox_100')),
    Field('RelatedCards',label='Related Cards'),
    singular="Card Master Content", plural="Card Master Contents",
    format = '%(ContentText)s [%(Lang)s|%(LangWrittenIn)s]'
    )

db.CardMasterContent._Icon = '/smartdeck/static/img/icons/set1/svg/cardmaster_content.svg'

# ----- Card Structure table-----
db.define_table('CardStructure',
    Field('LongName', label='Name', required=True),
    Field('ShortName', label='Short Name', required=False),
    Field('FrontFaceStructure', label='Front Structure', required=True, 
            widget= lambda field, value: SQLFORM.widgets.text.widget(field, value, _class='textbox_100')),
    Field('BackFaceStructure', label='Back Structure', required=True, 
            widget= lambda field, value: SQLFORM.widgets.text.widget(field, value, _class='textbox_100')),
    Field('Tags', label='Tags'),
    Field('Lang', label='Language', default='-'),
    Field('MultiChoiceImages',type='string', required=False, default='', label='Multi Choice Images'),
    format = '%(LongName)s',
    singular="Card Structure", plural="Card Structures",
)
db.CardStructure.Lang.requires = IS_IN_DB(db, 'Languages.Code', '%(Code)s (%(LongName)s)', zero=T(''))
db.CardStructure.MultiChoiceImages.requires = IS_IN_SET(('', 'Hide on Front Face', 'Hide on Back Face', 'Hide on Both Faces'))
db.CardStructure._Icon = '/smartdeck/static/img/icons/set1/svg/card_structure.svg'

# ----- Card table -----
# A Ccard is the final visual representation (eg CardStructure) of selected content from the CardMaster. A single card can belong to multiple Decks. However each deck
# expects that the Cards all have the same CardStructure. So the one card cannot belong to decks with different CardStructures. However it is possible for the to be in
# a child deck where the parent has one structure and the child another. 
# CardStructureID: this is set when the card is first created and added to a deck.
db.define_table('Card',
    Field('CardMasterID',db.CardMaster, label='Card Master', required=True),
    Field('CardStructureID',db.CardStructure, label='Structure'),
    Field('RenderSizes', label='Render Sizes', required=False),
    Field('FrontFaceStructure', label='Front Structure', required=False, 
            widget= lambda field, value: SQLFORM.widgets.text.widget(field, value, _class='textbox_100')),
    Field('BackFaceStructure', label='Back Structure', required=False, 
            widget= lambda field, value: SQLFORM.widgets.text.widget(field, value, _class='textbox_100')),
    Field('FrontFaceRendered', label='Front Render', required=False, 
            widget= lambda field, value: SQLFORM.widgets.text.widget(field, value, _class='textbox_100')),
    Field('BackFaceRendered', label='Back Render', required=False, 
            widget= lambda field, value: SQLFORM.widgets.text.widget(field, value, _class='textbox_100')),
    Field('LongName', compute= lambda r: ("%s [%s]") % (db.CardMaster(r.CardMasterID).Name, '-' if not r.CardStructureID else db.CardStructure(r.CardStructureID).ShortName)),
    Field('Details',default=None),
    # format = lambda r: ("%s") % (r.LongName),  # db.CardStructure(r.CardStructureID).ShortName'),
    format = lambda r: ("%s [%s]") % (db.CardMaster(r.CardMasterID).Name, '-' if not r.CardStructureID else db.CardStructure(r.CardStructureID).ShortName),
    singular="Card", plural="Cards",
)  
db.Card._Icon = URL('static', '/img/icons/set1/svg/cards3.svg')

db.define_table('PresentationOption',
    Field('LongName', label='Name', required=True),
    Field('ShortName', label='Short Name', required=False),
    Field('IsGame',type='boolean',default=False)
)
#lambda row: (db.brands(row.brand_id_01).name)

# ------ Deck Table -------
# DefaultCardStructureID:   This is used to set the CardStructureID of a new card created for this deck. It is also used when changing the structure for all cards in the deck.
#                           All cards in the deck that have the old strcuture will be changed to use the new structure
# CardCriteria: Stores the complex criteria (includes and excludes) which determines which cards are included in the deck. 
db.define_table('Deck',
    Field('LongName', label='Name', required=True),
    Field('ShortName', label='Short Name', required=False),
    Field('DefaultCardStructureID',db.CardStructure, label='Default Structure'),
    Field('IsPublic','boolean', required=True, default=True, label='Public'),
    Field('OwnerByOrganisationID',db.Organisation, required=True, default=session.OrganisationID, label='Owner Organisation'),
    Field('DeckImageID', db.Media, label='Image'),
    Field('CardCriteria', label='Criteria', required=False,
            widget= lambda field, value: SQLFORM.widgets.text.widget(field, value, _class='textbox_100')),
    Field('ChildDeckIDList', type='list:reference Deck', required=False, default=None, label='Child Decks'),  # This is a list of all Child Decks either directly assigned or assigned to other child decks.
    Field('ParentDeckIDList', type='list:reference Deck', required=False, default=None, label='Parent Decks'),  # This is a list of all Parent Decks either directly assigned or assigned to other parent decks.
    Field('QuestionCardSize', label='Question Card Size'),  # What is the ideal card size for questions
    Field('QuestionCardOrientation', default='Portrait', label='Question Card Orientation'),
    Field('AnswerCardSize', label='Answer Card Size'),  # What is the ideal card size for answers
    Field('AnswerCardOrientation', default='Portrait', label='Answer Card Orientation'),
    Field('PresentationOptions', type='list:reference PresentationOption', default=None, label='Presentation Options'),
    Field('CardCount', type='integer', default=0, label='Card Count'),
    format = '%(LongName)s',
    singular="Deck", plural="Decks",
)  
db.Deck._Icon = '/smartdeck/static/img/icons/set1/svg/deck6.svg'

db.define_table(
    'DeckChild',
    Field('ChildDeckID',db.Deck, label='Child Deck', required=True),
    Field('DeckID',db.Deck, label='Deck', required=True),
    Field('Include','boolean', label='Include', default=True),          # Should this deck be included
    Field('StartOffset','integer', label='Start Date', default=0),      # The number of days this deck should become active after the TeachingGroup start date.
    Field('StartDate','date', label='Start Date'),                      # The date when a deck should become visible. It overides the StartOffset
    format = lambda r: ("%s has child %s" % (db.Deck(r.DeckID).ShortName, db.Deck(r.ChildDeckID).ShortName)),
    singular="Child Deck", plural="Child Decks",
)  
db.DeckChild._Icon = '/smartdeck/static/img/icons/set1/svg/deck_children2.svg'
db.executesql('CREATE UNIQUE INDEX IF NOT EXISTS idx_DeckID_ChildDeckID ON DeckChild (DeckID,ChildDeckID);')

db.define_table('DeckCard',
    Field('DeckID',db.Deck, label='Deck', required=True),
    Field('CardID',db.Card, label='Card', required=True),
    Field('Include','boolean', label='Include', default=True, represent = lambda name, row: "Yes" if name is True else "No"),
    Field('LongName', compute=lambda r: ("%s") % (db.Card(r.CardID).LongName)),
    # Field('LongggName', compute=lambda r: ("--") ),
    format = lambda r: ("%s" % (r.LongName)),
    singular="DeckCard", 
    plural="Deck Cards",
)  
db.DeckCard._Icon = URL('static','img/icons/set1/svg/deck_cards.svg')

db.executesql('CREATE UNIQUE INDEX IF NOT EXISTS idx_DeckID_CardID ON DeckCard (DeckID,CardID);')

db.define_table('TeachingGroup',
    Field('LongName', type='string', label='Group Name', required=True),
    Field('ShortName', type='string', label='Short Name', required=True),
    Field('OrganisationID',db.Organisation, label='Organisation', required=True, default=session.OrganisationID),
    Field('TeacherUserID', db.auth_user, label='Teacher'),
    Field('StartDate', type='date', label='Start'),
    Field('EndDate', type='date', label='End'),
    Field('Period'),
    Field('IsActive', type='boolean', label='Active', required=True, default=True),
    format = lambda r: ("%s" % (r.LongName)),
    singular="Teaching Group", plural="Teaching Groups",
    # migrate=False,
)
db.TeachingGroup._Icon = '/smartdeck/static/img/icons/set1/svg/teaching_groups.svg'

db.define_table('TeachingGroupStudent',
    Field('TeachingGroupID',db.TeachingGroup, label='Group'),
    Field('StudentUserID',db.auth_user, label='Student'),
    # Field('TeachingGroupID',type='integer', label='Group'),
    # Field('StudentUserID',type='integer', label='Student'),
    Field('IsEnrolled', 'boolean', label='Enrolled', required=True, default=True),
    format = lambda r: '%s (%s)' %(r.StudentUserID, r.TeachingGroupID),
    singular="Student", plural="Students"
)
db.TeachingGroupStudent._Icon = URL('static','img/icons/set1/svg/teaching_group_students.svg')

#db.executesql('DROP TABLE IF EXISTS TeachingGroupDeck;')

db.define_table('TeachingGroupDeck',
    Field('TeachingGroupID',db.TeachingGroup, required=True, label='Group'),
    Field('DeckID',db.Deck, required=True, label='Deck'),
    Field('IsActive', 'boolean', label='Active', required=True, default=True),
    format = lambda r: '%s (%s)' %(r.DeckID, r.TeachingGroupID),
    singular="Teaching Group Deck", plural="Teaching Group Decks",
)
db.TeachingGroupDeck._Icon = URL('static','img/icons/set1/svg/teaching_group_decks.svg')
db.executesql('CREATE UNIQUE INDEX IF NOT EXISTS idx_TeachingGroupID_DeckID ON TeachingGroupDeck (TeachingGroupID, DeckID);')

db.define_table('UserCard',
    Field('StudentUserID',db.auth_user, required=True, label='Student'),
    Field('CardID', db.Card, required=True, label='Card'),
    Field('Status', type='string'),  # Pending (waiting to be shown as a new card), New (part of the new cards being shown), Active (current being scheduled), Exclude 
    Field('ReviewCount',type='integer', required=False, default=0),
    Field('CorrectCount',type='integer', required=False, default=0),
    Field('Streak',type='integer', required=False, default=0),  # A wrong answer will reset this to 0
    Field('CurrentInterval',type='double', required=False, default=0),
    Field('LastReview',type='datetime', required=False, default=None),
    Field('Due',type='datetime', required=False, default=None),
    Field('Difficulty', type='decimal(3,1)', required=False, default=0),  # A scale of 0 to 10 with 10 being the most difficult
    Field('LastResult', type='string', required=False, default=''),
    Field('LastPoints', type='integer', default=0)
)
db.UserCard._Icon = URL('static','img/icons/set1/svg/cards3.svg')
db.executesql('CREATE UNIQUE INDEX IF NOT EXISTS idx_UserCard_StudentUserID_CardID ON UserCard (StudentUserID, CardID);')

# UserDeck is determined indirectly from the Groups he is assigned to. We need this table to maintain statistical data for students so that we dont
# have to generate it every time a teacher does a report or a page needs to display progress stats
db.define_table('UserDeck',
    Field('StudentUserID',db.auth_user, required=True, label='Student'),
    Field('DeckID', db.Deck, required=True, label='Deck'),
    Field('TotalCards',type='integer', required=False, default=None, label='Total Cards'),
    Field('DueCards',type='integer', required=False, default=None, label='Due Cards'),
    Field('ActiveCards',type='integer', required=False, default=None, label='Active Cards'),  # A card that the student has begun to learn (has an interval)
    Field('LearntCards',type='integer', required=False, default=None, label='Learnt Cards'),
    Field('Status', type='string'),  # ??? Might be useful
    Field('ReviewCount',type='integer', required=False, default=None, label='Review Count'),
    Field('CorrectCount',type='integer', required=False, default=None, label='CorrectCount'),
    Field('AvgStreak',type='double', required=False, default=0, label='Avg Streak'),  # A wrong answer will reset this to 0
    Field('AvgCurrentInterval',type='double', required=False, default=0, label='Avg Interval'),
    Field('AvgDifficulty', type='decimal(3,1)', required=False, default=0, label='Avg Difficulty'),  # A scale of 0 to 10 with 10 being the most difficult
    Field('LastReview',type='datetime', required=False, default=None, label='Last Reviewed'),
    Field('Progress',type='integer', required=False, default=None)  # Percent Progress
)
db.UserDeck._Icon = URL('static','img/icons/set1/svg/decks.svg')
db.executesql('CREATE UNIQUE INDEX IF NOT EXISTS idx_UserDeck_StudentUserID_DeckID ON UserDeck (StudentUserID, DeckID);')

# This is not intended to be a complete history. We might hold card history for 30-60 days (2 months). After that time we might collapse the daily history into
# monthly history (merging all records for the month into a single record on the first of the month). And then after 1 year we might collapse those records
# into annual records on the first of the year. It is needed to maintain a leaderboard for best progress today, this week, this month etc.
db.define_table('UserCardHistory',
    Field('UserCardID',db.UserCard, required=True, label='User Card'),
    Field('ReviewDate',type='date', required=True, default=datetime.datetime.now()),
    Field('ReviewCount',type='integer', required=False, default=0),
    Field('CorrectCount',type='integer', required=False, default=0),
    Field('TotalTime',type='time', required=False, default=None),
    Field('Points', type='integer', required=False, default=0)
)
db.UserCardHistory._Icon = URL('static','img/icons/set1/svg/categories3.svg')
db.executesql('CREATE UNIQUE INDEX IF NOT EXISTS idx_UserCardHistory_UserCardID_ReviewDate ON UserCardHistory (UserCardID, ReviewDate);')

# This table holds the answered supplied by the students for a particular card. Both wrong and right answers are recorded. This allows us to see
# which answers students most often think are the correct answers. We can then use these answers as the multiple choice answers and so make the
# question more or less easy. 
db.define_table('CardAnswer',
    Field('CardID', db.Card, required=True, label='Card'),              # The card being tested
    Field('AnswerCardID', db.Card, required=True, label='AnswerCard'),  # The card that the student thought was the answer
    Field('AnswerCount',type='integer', required=True, default=0)       # The number of times this Answer Card has been chosen
)
db.CardAnswer._Icon = URL('static','img/icons/set1/svg/categories3.svg')

db.executesql('CREATE UNIQUE INDEX IF NOT EXISTS idx_CardAnswery_CardID_AnswerCardID ON CardAnswer (CardID, AnswerCardID);')

# Shop stuff
db.define_table('ItemType',  # What types of items does the shop sell. Some orgainsations might not want to sell all media items. So they can set which ones here.
    Field('Description'),
    Field('IsShopItem', type='boolean', label='Shop'),
    Field('IsMediaItem', type='boolean', label='Media'),
    format = '%(Description)s'
)
db.ItemType._Icon = URL('static','img/icons/set1/svg/categories3.svg')
db.executesql('CREATE UNIQUE INDEX IF NOT EXISTS idx_ItemType_Description ON ItemType (Description);')

db.define_table('StockItem',  # What items does the shop sell. Some orgainsations might not want to sell all media items. So they can set which ones here.
    Field('Description'),
    Field('ItemType', db.ItemType, required=True, label='Type'),                # Card Back, Game, Theme, Sounds when right or wrong
    Field('OrganisationID', db.Organisation, required=True, label='Organisation', default=session.OrganisationID),
    Field('MediaID', db.Media, required=True, label='Media', widget=media_widget),       # All(?) items come from the Media table.
    Field('Status', type='string', required=True, label='Status', default='Available', requires = IS_IN_SET(('Available', 'Unavailable', 'On Hold'))),  # ???
    # Field('ItemType', type='string', required=True),                # Determined from the MediaID
    Field('PricePoints', type='integer',required=True, default=0, label='Price'),  # Also used as the minimum for an auction
    Field('RestockDelay',type='integer', required=True, default=0, label='Restock Delay'),  # If owned by the shop, how quickly should this item be restocked. Allows a delay on popular items
    Field('PriceAdjustmentFactor',type='integer', required=True, default=0, label='Price Adjustment%'),  # 0% means no adjustment,  10% means in crease it by 10% when purchased, -10 means decrease price
    Field('Availability'),  # Restrict when items are available (every second week, only to some students etc.)
    Field('Qty',type='integer', required=True, default=-1),  # -1 is unlimited
    format = lambda r: f"{r.Description} ({db.ItemType[r.ItemType].Description})", 
    singular="Stock Item", plural="Stock Items",
)
db.StockItem._Icon = URL('static','img/icons/set1/svg/stock_item.svg')

# db.executesql('DROP INDEX IF EXISTS idx_StockItem_OrganisationID_MediaID;')
db.executesql('CREATE UNIQUE INDEX IF NOT EXISTS idx_StockItem_OrganisationID_MediaID_ItemType ON StockItem (OrganisationID, MediaID, ItemType);')

db.define_table('ShopItem',  # What items are or will be available for sale
    Field('StockItemID', db.StockItem, required=True, label='Stock Item'),             # This ties an item to an Organisation
    Field('OwnerUserID', db.auth_user, required=True, label='Owner', default=session.UserID),
    Field('BuyerUserID', db.auth_user, required=False, label='Buyer'),
    Field('Status', type='string', required=True, label='Status', default='auction'),  # auction, buynow, sold, canceled
    Field('PricePoints', type='integer',required=True, default=0, label='Price'),  # Also used as the minimum for an auction
    Field('OfferPoints', type='integer',required=True, default=0, label='Offer'),  # How much is the buyer offering
    Field('AvailableDateTime', type='datetime', required=False, label='Available When'),
    Field('CompleteByDateTime', type='datetime', required=False, label='Complete By'),
    Field('Qty',type='integer', required=True, default=1),
    format = lambda r: '%s (%s)' %(r.StockItemID, r.OwnerUserID),
    singular="Shop Item", plural="Shop Items",
)
db.ShopItem._Icon = URL('static','img/icons/set1/svg/shop_item.svg')

db.define_table('UserItem',  # What items does the user own or like
    Field('OrganisationUserID', db.OrganisationUser, required=True, label='User'),
    Field('StockItemID', db.StockItem, required=True, label='Stock Item'),  # Only one record per stock item.
    Field('Status', type='string', required=True, label='Status', default='liked'),  # available, unavailable, liked (allows students to like an item they find int the store)
    Field('Favourite',type='boolean', default=True),               # Allows the user to choose what items they want to show
    Field('History', type='string', required=False),                # What has happened to this item - buy, sold, won, auctioned etc etc
    Field('PricePoints', type='integer',required=True, default=0, label='Price'),  # How much did the item cost.
    Field('Qty', type='integer',required=True, default=0, label='Quantity'),  # A user can buy more than one of the same item
    singular="User Item", plural="User Items",
)
db.UserItem._Icon = URL('static','img/icons/set1/svg/user_item.svg')
# db.executesql('DROP INDEX IF EXISTS idx_UserItem_UserID_OrganisationID_StockItemID;')
# db.executesql('CREATE UNIQUE INDEX IF NOT EXISTS idx_UserItem_UserID_OrganisationID_StockItemID ON UserItem (UserID, OrganisationID, StockItemID);')
db.executesql('CREATE UNIQUE INDEX IF NOT EXISTS idx_UserItem_OrganisationUserID_StockItemID ON UserItem (OrganisationUserID, StockItemID);')

db.define_table('EventLog',
    Field('LogType', label='Type'),  # A tablename, 
    Field('EventAction'),
    Field('ObjectID', type='integer', default=None),
    Field('UserID', type='integer', default=None),
    Field('Settings', default=None),
    Field('Processed', type='boolean', default=False),
    Field('LogFunction', label='Function'),
    Field('LogMessage', type='text', label='Message'),
)
db.EventLog._Icon = URL('static', '/img/icons/set1/svg/event_log.svg')
db.executesql('CREATE INDEX IF NOT EXISTS idx_EventLog_EventAction ON EventLog (EventAction);')
db.executesql('CREATE INDEX IF NOT EXISTS idx_EventLog_UserID_Processed ON EventLog (UserID, Processed);')
db.executesql('CREATE INDEX IF NOT EXISTS idx_EventLog_EventAction_UserID_Processed ON EventLog (EventAction, UserID, Processed);')

db.define_table('UploadTemplate',
    Field('Description', label='Description'),
    Field('OriginalFilename'),
    Field('FileReference', type='upload', required=False, uploadfolder=os.path.join(request.folder, 'static/temp'), autodelete=True, widget=FileSelector_widget),
    # Field('Filename', type='upload', required=False, uploadfolder=os.path.join(request.folder, 'static/temp'), autodelete=True),
    # Field('Filename', type='upload', required=False),
    Field('Settings', type='text', default=None),
    Field('Fields', type='text', default=None),
    Field('Processed', type='boolean', default=False),
)
db.UploadTemplate._Icon = URL('static', '/img/icons/set1/svg/event_log.svg')
# db.UploadTemplate.Filename.widget = lambda field, value, x: my_string_widget(field, value, x)

db.define_table('Registry',
    Field('CustomSQL')
    )
    
#TESTING STUFF
db.define_table('post', Field('your_message', 'text'))
db.post.your_message.requires = IS_NOT_EMPTY()

db.define_table('user_pictures',
                Field('userr', db.auth_user, unique=True, represent=lambda id: '%s %s '%(db.auth_user(id).first_name, db.auth_user(id).last_name)),
                Field('picture', 'upload', requires=IS_IMAGE()))
#db.user_pictures.user.requires=IS_IN_DB(db,'auth_user.id', '%(first_name)s %(last_name)s', zero=T('choose one'))
