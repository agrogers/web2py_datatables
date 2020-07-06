from datetime import datetime
import inspect
import sys
import simplejson as json
import logging

#------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Gets a value from a nested value and returns None if any key doesn't exist
def get_deep(dictionary, keys, default=None):

    def Parse(val):
        if isinstance(val,str):
            if val.lower() == 'true':
                return True
            elif val.lower() == 'false':
                return False
            else:
                return val
        else:
            return val

    # return functools.reduce(lambda d, key: d.get(key, default) if isinstance(d, dict) else default, keys.split("."), dictionary)
    if not dictionary or not keys: return default
    d = dictionary
    # Check if the keys is a simple boolean or number. If it is, we cant split it (and dont need to. Just turn it into a list for processing.)
    if isinstance(keys, (int, float)):
        k = [keys]
    else:
        k = keys.split(".")
    if k[0] in d:
        if len(k) == 1: 
            return Parse(d.get(k[0]))
        d = d.get(k[0])
        if k[1] in d:
            if len(k) == 2: return Parse(d.get(k[1]))
            d = d.get(k[1])
            if k[2] in d:
                if len(k) == 3: return Parse(d.get(k[2]))
                return "Can only get key/values that are 3 deep. It's a bit embarassing "
    
    return default

#------------------------------------------------------------------------------------------------------------------------------------------------------------------
def AddLogEntry(LogType="Error", LogFunction = "", LogMessage = "", EventAction='',ObjectID=None, UserID=None, Settings=None, InsertOrUpdate='Update'):
    # LogType: Error, [TableName] etc
    
    if (ObjectID or UserID) and InsertOrUpdate=='Update':
        if LogType == 'UserCard':
            # Assumes ObjectID = UserCardID
            if not Settings: Settings = 'ObjectId=UserCardID'

        db.EventLog.update_or_insert(LogType=LogType, EventAction=EventAction, ObjectID=ObjectID, UserID=UserID, Processed=False, Settings=Settings)
    else:
        # It's probably an error or operational or debugging message
        db.EventLog.insert(LogType=LogType, LogFunction = LogFunction, LogMessage = LogMessage, EventAction=EventAction, Settings=Settings, ObjectID=ObjectID, UserID=UserID, )

    return

#------------------------------------------------------------------------------------------------------------------------------------------------------------------
def LogError(Controller, e=None, ExtraInfo = "", LogType = 'Error', ReturnJson=False, FlashError = False):

    NOW = datetime.now()
    curframe = inspect.currentframe()
    ErrFunction = inspect.getouterframes(curframe, 2)
    Msg = sys.exc_info()[0]
    LogFunction = "[%s] %s > %s > %s" %(Controller, ErrFunction[1].function, ErrFunction[2].function, ErrFunction[3].function) 

    if e:
        if hasattr(e, 'message'):
            Msg = "%s [Sys: %s]" % (e.message, Msg)
            #print(e.message)
        else:
            #print(e)
            Msg = "%s [Sys: %s]" % (e, Msg)

    if not Msg: Msg=''
    
    print('------------------------------- ERROR -----------------------------------')
    print("%s: FUNC: %s. ERR: %s. %s" % (str(NOW)[11:19], LogFunction, Msg, ExtraInfo))
    AddLogEntry(LogType=LogType, LogFunction = LogFunction, LogMessage = '%s %s' % (Msg, ExtraInfo))
    
    print('-------------------------------------------------------------------------')
    
    result = ("%s: FUNC: %s. ERR: %s. %s" % (str(NOW)[11:19], LogFunction, Msg, ExtraInfo))

    message = result
    if 'ERR: UNIQUE constraint failed' in message:
        startat = message.find("ERR: UNIQUE")
        char1 = ":"
        char2 = "["
        table_info = message[message.find(char1,startat) + 1 : message.find(char2,startat)]
        message = f'There is already a record in the database just like this one. We cannot add another. ({table_info})'

    if FlashError: response.flash = XML(response.flash + "Error: " + message)

    if ReturnJson:
        result = json.dumps(dict(Success = False, Message = message))
    
    logger = logging.getLogger("web2py.app.myapp")
    logger.setLevel(logging.DEBUG)
    logger.error(message)

    return result

#------------------------------------------------------------------------------------------------------------------------------------------------------------------
def DetermineMediaRepresentation(opRow, ReturnMediaType = 'Text', FieldName = 'FileReference'):

    try:
        FileReference = opRow[FieldName]

        if FileReference:
            # fn_parts = MediaRec.Media.FileReference.split(".")
            fn_parts = FileReference.split(".")

            Images = ['gif','jpg','png','bmp','jpeg','tif','svg']
            Videos = ['mov','mp4','mpeg','mpg','avi']
            Documents = ['doc','docx','xls','xlsx','ppt','pptx','txt']
            Audio = ['wav','mp3','mid']

            ext =  fn_parts[4].lower()
            
            if ext in Images:
                if ReturnMediaType == 'Text':
                    return 'Image'
                else:
                    if ext == 'gif':
                        return 'Media.FileReference.0000000000000006.60000000000000.svg'
                    elif ext == 'jpg':
                        return 'Media.FileReference.0000000000000011.11000000000000.svg'
                    elif ext == 'png':
                        return 'Media.FileReference.0000000000000010.10000000000000.svg'
                    else:
                        return 'Media.FileReference.0000000000000010.10000000000000.svg'

            elif fn_parts[4].lower() in Videos:
                if ReturnMediaType == 'Text':
                    return 'Video'
                else:
                    return 'Media.FileReference.0000000000000002.20000000000000.svg'
                
            elif fn_parts[4].lower() in Documents:
                if ReturnMediaType == 'Text':
                    return 'Document'
                else:
                    if ext[:3] == 'xls':
                        return 'Media.FileReference.0000000000000005.50000000000000.svg'
                    else:
                        return 'Media.FileReference.0000000000000003.30000000000000.svg'
                
            elif fn_parts[4].lower() in Audio:
                if ReturnMediaType == 'Text':
                    return 'Audio'
                else:
                    return 'Media.FileReference.0000000000000004.40000000000000.svg'

            else:
                if ReturnMediaType == 'Text':
                    return 'Unknown'
                else:
                    return 'Media.FileReference.0000000000000001.10000000000000.png'
        else:
            # This media item has no file. So we are probably dealing with URL of some sort. We can use the other row fields to determine an appropriate icon
            # But for the moment i am just going to make it a URL
            if ReturnMediaType == 'Text':
                return 'URL'
            else:
                return 'Media.FileReference.0000000000000007.70000000000000.svg'

    except Exception as e:
        PrintDebug(9,e)
        return 'None'

