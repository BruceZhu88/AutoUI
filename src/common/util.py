
# Author: Bruce.Zhu(Jialin)

import os
import shutil
import json
import threading
import webbrowser
import zipfile
from xml.etree import ElementTree as ElementTree
from .Logger import MyLog


logger = MyLog("main").get_log()


def split_dict(dic: dict):
    for k, v in dic.items():
        return k, v


def store(file_path, data):
    path = os.path.abspath(file_path)
    with open(path, 'w') as json_file:
        # json.dump(json.dumps(data), json_file)
        json_file.write(json.dumps(data))


def load(file_path):
    path = os.path.abspath(file_path)
    with open(path) as json_file:
        data = json.load(json_file)
    return data


def go_web_page(url):
    try:
        threading.Timer(0, lambda: webbrowser.open(url)).start()
    except Exception as e:
        logger.debug(e)


def read_file(filename):
    try:
        with open(filename) as f:
            for line in f.readlines():
                return line
    except Exception as e:
        logger.debug("File {0} does not exist: {1}".format(filename, e))
        return ""


def delete_file(src):
    if os.path.exists(src):
        try:
            os.remove(src)
        except Exception as e:
            logger.debug("Delete file {0} failed: {1}".format(src, e))
            # print('delete file %s failed'%src)
    else:
        logger.debug("Delete file {0} does not exist!!".format(src))


def empty_folder(dir_path, except_file=None):
    if not os.path.exists(dir_path):
        return False
    for file_name in os.listdir(dir_path):
        file_path = os.path.join(dir_path, file_name)
        if file_name == except_file:
            continue
        try:
            shutil.rmtree(file_path)
        except OSError:
            os.remove(file_path)


def zip_dir(dir_name, zip_file_name):
    file_list = []
    # Check input ...
    full_dir_name = os.path.abspath(dir_name)
    full_zip_filename = os.path.abspath(zip_file_name)
    print("Start to zip {0} to {1}...".format(
        full_dir_name, full_zip_filename))
    if not os.path.exists(full_dir_name):
        print("Dir/File %s is not exist, Press any key to quit..." % full_dir_name)
        # input_str = input()
        return
    if os.path.isdir(full_zip_filename):
        tmp_basename = os.path.basename(dir_name)
        full_zip_filename = os.path.normpath(
            os.path.join(full_zip_filename, tmp_basename))
    if os.path.exists(full_zip_filename):
        print(
            "%s has already exist, are you sure to modify it ? [Y/N]" % full_zip_filename)
        while 1:
            # input_str = input()
            input_str = "Y"
            if input_str.lower() == "n":
                return
            else:
                if input_str.lower() == "y":
                    print("Continue to zip files...")
                    break

    # Get file(s) to zip ...
    if os.path.isfile(dir_name):
        file_list.append(dir_name)
        dir_name = os.path.dirname(dir_name)
    else:
        # get all file in directory
        for root, dir_list, files in os.walk(dir_name):
            for filename in files:
                file_list.append(os.path.join(root, filename))

    # Start to zip file ...
    with zipfile.ZipFile(full_zip_filename, "w") as dest_zip:
        for each_file in file_list:
            dest_file = each_file[len(dir_name):]
            print("Zip file {0}...".format(dest_file))
            dest_zip.write(each_file, dest_file)
    print("Zip folder succeed!")


adb_command = {}


def set_xml():
    if len(adb_command) == 0:
        adb_path = './config/adb.xml'
        tree = ElementTree.parse(adb_path)
        for adb in tree.findall("adb"):
            command = {}
            for data in adb.getchildren():
                adb_id = data.get("id")
                command[adb_id] = data.text
            adb_command[adb.get('name')] = command


def get_xml_dict(command_name):
    set_xml()
    adb_dict = adb_command.get(command_name)
    return adb_dict


def get_adb(command_name, adb_id):
    command = get_xml_dict(command_name)
    adb = command.get(adb_id)
    return adb
