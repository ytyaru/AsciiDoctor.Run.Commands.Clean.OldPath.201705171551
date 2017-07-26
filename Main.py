#!python3
#encoding: utf-8
import os
import os.path
import subprocess
import UpdatedDb
class Main(object):
    def __init__(self, path_dir_root, path_dir_css, filename_css='asciidoctor.css'):
        self.__path_dir_root = path_dir_root
        self.__path_dir_css = path_dir_css
        self.__filename_css = filename_css
        self.__db = UpdatedDb.UpdatedDb()
    
    def Run(self, path_dir_root=None, path_dir_css=None, filename_css=None):
        if path_dir_root:
            self.__path_dir_root = path_dir_root
        if path_dir_css:
            self.__path_dir_css = path_dir_css
        if filename_css:
            self.__filename_css = filename_css
        print(self.__path_dir_root)
        print(self.__path_dir_css)
        print(self.__filename_css)
        for dirpath, dirnames, filenames in os.walk(self.__path_dir_root):
            for filename in filenames:
                if self.__IsAsciiDocExtension(filename):
                    path_adoc = os.path.join(dirpath, filename)
                    if self.__db.IsUpdated(path_adoc):
                        self.__RunAsciiDoctor(path_adoc)
    
    def __IsAsciiDocExtension(self, path):
        if not path:
            return False
        for e in ['ad', 'asc', 'adoc', 'asciidoc']:
            if path.endswith(e):
                return True
        return False
    
    def __RunAsciiDoctor(self, path_file_adoc):
        command = 'rbenv exec asciidoctor -a linkcss -a stylesheet={stylesheet} -a stylesdir={stylesdir} {adoc}'.format(stylesheet=self.__filename_css, stylesdir=self.__path_dir_css, adoc=path_file_adoc)
        print(command)
        subprocess.check_output(command, shell=True)


if __name__ == '__main__':
    path_root_adoc = os.path.abspath(os.path.dirname(__file__))
    path_dir_css = os.path.join(path_root_adoc, 'css/')
    filename_css = 'asciidoctor.css'
    
    db = UpdatedDb.UpdatedDb()
    db.Clean(path_root_adoc)
    
    m = Main(path_root_adoc, path_dir_css, filename_css)
    m.Run()

