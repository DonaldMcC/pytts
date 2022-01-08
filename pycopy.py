#!/usr/bin/env python3
# this will copy files from a specified source to destination we may look at parameters and
# so forth later - but currently only 1 main use for this
# pip install shareplum
# https://stackoverflow.com/questions/68914339/python-upload-files-to-sharepoint-using-shareplum

import os
import shutil
from shareplum import Office365
from shareplum import Site
from shareplum.site import Version
from mainfile import list_files


# SETUP DATA - amend for your use
source_folder = r'c:\users\donal\Documents\testcopy\source'  # where you put files to be copied
dest_folder = r'c:\users\donal\Documents\testcopy\dest'  # where you create moved files
archive_folder = r'c:\users\donal\Documents\testcopy\archive'  # where you move the archived files
sharepoint_dest = False

#sharepoint info
server_url = "https://example.sharepoint.com/"
site_url = server_url + "sites/my_site_name"
Username = 'myusername'
Password = 'mypassword'
Sharepoint_folder = 'Shared Documents'
fileName = 'myfilename'


def file_upload_to_sharepoint(file):
    source = os.path.join(source_folder, file)
    authcookie = Office365(server_url, username = Username, password=Password).GetCookies()
    site = Site(site_url, version=Version.v365, authcookie=authcookie)
    folder = site.Folder(Sharepoint_folder)
    with open(source, mode='rb') as srcfile:
        fileContent = srcfile.read()
    folder.upload_file(fileContent, file)


f = list_files(source_folder)
for file in f:
    sourcefile = os.path.join(source_folder, file)
    archivefile = os.path.join(archive_folder, file)
    if sharepoint_dest:
        file_upload_to_sharepoint(file)
    else:
        destfile = os.path.join(dest_folder, file)
        copy_success = shutil.copy(sourcefile, destfile)
    if copy_success:
        shutil.move(sourcefile, archivefile)
