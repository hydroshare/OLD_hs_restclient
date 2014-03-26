
import os
from cStringIO import StringIO
import mimetypes
import base64

import slumber
import simplejson as json


class HydroShareException(Exception):
    pass

class _entity(object):
    """
    Root entity used for creating all other object types (via subclassing)
    """
    def __init__(self, obj=None):
        """ Construct an entity
        
            Arguments:
            obj -- A dict type whose keys will back this class's attributes
        """
        if obj:
            self.__dict__['_obj'] = obj
        else:
            self.__dict__['_obj'] = {}
        
    def __getattr__(self, name):
        if name.startswith("_"):
            raise AttributeError(name)
        
        return self._obj[name]
    
    def __setattr__(self, name, value):
        if name.startswith("_"):
            self.__dict__[name] = value
        
        self._obj[name] = value
        
    def _getObj(self):
        return self._obj
    
    def _setObj(self, obj):
        self._obj = obj


class GenericResource(_entity):
    """
    A HydroShare Generic Resource
    """
    RESOURCE_FILE_KEY = 'resource_file'
    FILE_KEY = 'file' 
    FILE_NAME_KEY = 'name'
    FILE_TYPE_KEY = 'content-type'
    MIME_DEFAULT = 'application/octet-stream'
    
    TITLE_KEY = 'title'
    CREATOR_KEY = 'creator'
    USER_KEY = 'user'
    OWNERS_KEY = 'owners'
    
    
    def __init__(self, obj=None):
        """
            Constructor for GenericResources.
            
            Generally should not be called directly
        """
        super(GenericResource, self).__init__(obj)
        try:
            resource_file = self._obj[GenericResource.RESOURCE_FILE_KEY]
            if not GenericResource.FILE_KEY in resource_file:
                raise HydroShareException("resource_file object of resource %d has no key %s" % \
                                          (self._obj['id'], GenericResource.FILE_KEY) )
            if not GenericResource.FILE_NAME_KEY in resource_file:
                raise HydroShareException("resource_file object of resource %d has no key %s" % \
                                          (self._obj['id'], GenericResource.FILE_NAME_KEY) )
            if not GenericResource.FILE_TYPE_KEY in resource_file:
                raise HydroShareException("resource_file object of resource %d has no key %s" % \
                                          (self._obj['id'], GenericResource.FILE_TYPE_KEY) )
        except KeyError:
            pass
        
    # File-related methods
    def readFile(self, filename):
        """
        Write contents of file to file named by filename.  
        
        Caller must set file name separately using the appropriate call.
        """
        infile = open(filename, 'rb')
        encoded = StringIO()
        base64.encode(infile, encoded)
        infile.close()
        try:
            resource_file = self._obj[GenericResource.RESOURCE_FILE_KEY]
        except KeyError:
            resource_file = {}
            self._obj[GenericResource.RESOURCE_FILE_KEY] = resource_file
        resource_file[GenericResource.FILE_KEY] = encoded.getvalue().replace('\n', '')
        encoded.close()
      
    def writeFile(self, filename):
        """
        Write contents of file to file named by filename
        """
        outfile = open(filename, 'wb')
        encoded = StringIO(self.resource_file[GenericResource.FILE_KEY])
        base64.decode(encoded, outfile)
        outfile.close()
    
    def getFilename(self):
        """ 
        Return the name of the file
        """
        return self.resource_file[GenericResource.FILE_NAME_KEY]
    
    def setFilename(self, filename):
        """ 
        Set the name of the file
        """
        self.resource_file[GenericResource.FILE_NAME_KEY] = filename
        (mimeType, enc) = mimetypes.guess_type(filename)
        if not mimeType:
            mimeType = GenericResource.MIME_DEFAULT
        self.resource_file[GenericResource.FILE_TYPE_KEY] = mimeType
    
    def getFiletype(self):
        """
        Return MIME type of the file
        """
        return self.resource_file[GenericResource.FILE_TYPE_KEY]


class HydroShare(object):

    def __init__(self, base_url, user_name=None, password=None):
        self.base_url = base_url
        self.user_name = user_name
        self.password = password
        
        self.api = slumber.API(self.base_url, format='json', 
                               auth=(self.user_name, self.password) )
        # TODO: error checking
        self.user = self.api.user.get(username=user_name)['objects'][0]

    def createResource(self, title, resource_type=GenericResource,
                       filename=None):
        """
        Create a new resource.
        
        Returns the ID of the newly created resource
        """
        if resource_type is GenericResource:
            newResource = GenericResource()
            newResource.user = self.user['resource_uri']
            newResource.creator = self.user['resource_uri']
            newResource.title = title
            if filename:
                newResource.readFile(filename)
                newResource.setFilename( os.path.basename(filename) )
            initObj = newResource._getObj()
            # TODO: error checking
            result = self.api.resource.post(initObj)
            # Copy created resource to existing object
            if GenericResource.RESOURCE_FILE_KEY in initObj:
                # HydroShare doesn't send the file field back in the response, so copy it
                result[GenericResource.RESOURCE_FILE_KEY] = initObj[GenericResource.RESOURCE_FILE_KEY]
            newResource._setObj(result)
            
            return newResource
        else:
            raise NotImplementedError("Type %s is not supported" % (str(resource_type), ) )
        
    
    def getResource(self, id):
        # TODO: error checking
        result = self.api.resource.get(id=id)['objects'][0]
        # TODO: type checking
        return GenericResource(result)
        
    
    def updateResource(self, resource):
        initObj = resource._getObj()
        
        import pdb; pdb.set_trace()
        
        result = self.api.resource.put(initObj)
        
        resource._setObj(result)
        return resource
    
    def deleteResource(self):
        pass