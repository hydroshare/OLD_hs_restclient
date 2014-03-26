import unittest
import os
import sys
import shutil
import tempfile
import filecmp
from zipfile import ZipFile

from hs_restclient import HydroShare

class GenericResourceTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.hs = HydroShare('http://127.0.0.1:8001/api/v1/', user_name='hs', password='water')
        
        # Create dummy resource file
        cls.tmpDir = tempfile.mkdtemp()
        os.chdir(cls.tmpDir)
        
        filename = 'foo.txt'
        cls.tmpFilename = os.path.join(cls.tmpDir, filename)
        cls.tmpFilenameOrig = "%s.orig" % (cls.tmpFilename,)
        tmpFile = open(cls.tmpFilename, 'w')
        tmpFile.write('this is a test\n')
        tmpFile.close()
        
        cls.zipFilename = 'foo.zip'
        cls.zipFilepath = os.path.join(cls.tmpDir, cls.zipFilename)
        with ZipFile(cls.zipFilename, 'w') as zipFile:
            zipFile.write(filename)
        os.rename(cls.tmpFilename, cls.tmpFilenameOrig)
        
        
    def test_create_and_get_resource(self):
        title = 'my new resource'
        newResource = self.hs.createResource('my new resource', filename=self.zipFilename)
        newResourceId = newResource.id
        self.assertEqual(title, newResource.title)
        self.assertIsNotNone(newResource.resource_file)

        # Get the newly created resource
        resource = self.hs.getResource(newResourceId)
        self.assertEqual(title, resource.title)
        self.assertIsNotNone(resource.resource_file)
        
        # Unzip the file from the resource and verify contents are the same
        outZipname = 'out.zip'
        outputZipfilepath = os.path.join(self.tmpDir, 'out')
        resource.writeFile(outputZipfilepath)
        
        outZip = ZipFile(outputZipfilepath, 'r')
        outZip.extractall(path=self.tmpDir)
        
        self.assertTrue( filecmp.cmp(self.tmpFilename, self.tmpFilenameOrig) )
        
        
    def test_create_and_update_resource(self):
        title = 'my new resource'
        newResource = self.hs.createResource('my new resource', filename=self.zipFilename)
        newResourceId = newResource.id
        self.assertEqual(title, newResource.title)
        self.assertIsNotNone(newResource.resource_file)
         
        newResource.title = 'my updated title'
        updatedResource = self.hs.updateResource(newResource)
        self.assertEqual(newResource.title, updatedResource.title)
        self.assertIsNotNone(newResource.resource_file)
    
    
    def test_create_and_delete_resource(self):
        title = 'my new resource'
        newResource = self.hs.createResource('my new resource', filename=self.zipFilename)
        newResourceId = newResource.id
        self.assertEqual(title, newResource.title)
         
        result = self.hs.deleteResource(newResource)
        self.assertTrue(result)
        
    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.tmpDir)
        
if __name__ == '__main__':
    unittest.main()