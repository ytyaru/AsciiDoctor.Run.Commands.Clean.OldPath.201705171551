#!python3
#encoding: utf-8
import os
import os.path
import subprocess
import datetime
import dataset
class UpdatedDb(object):
    def __init__(self):
        self.__file_name = 'AsciiDoc.Updated.sqlite3'
        self.__file_path = './'  + self.__file_name
        self.__db = None

    """
    DBに存在しないファイルパスのレコードがあればレコードを削除する。path_dir_rootを指定したら親がそのディレクトリでないパスのレコードを削除する。
    @param {string} path_dir_rootはクリーン対象ディレクトリ。
    """
    def Clean(self, path_dir_root=None):
        self.__Initialize()
        self.__db.begin()
        for record in self.__db['Updated'].find():
            if not os.path.exists(record['Path']) or (path_dir_root and not record['Path'].startswith(path_dir_root)):
                print('delete {0}'.format(record['Path']))
                self.__db['Updated'].delete(Path=record['Path'])
        self.__db.commit()
    
    """
    前回から指定ファイルが更新されたか否か。
    @param {string} pathは更新の是非を確認したいファイルのパス。
    """
    def IsUpdated(self, path):
        self.__Initialize()
        record = self.__db['Updated'].find_one(Path=path)
        new_record = {
            'Path': path,
            'Updated': "{0:%Y-%m-%d %H:%M:%S}".format(self.__GetUpdatedByFileMetadata(path))
        }
        # レコードが存在しなければ新しくレコードを追加してAsciiDoctorコマンドを実行する
        if not record:
            self.__db['Updated'].insert(new_record)
            return True
        # レコードが存在しDBの日時が古いなら、DBの日時を更新してAsciiDoctorコマンドを実行する
        else:
            if record['Updated'] < new_record['Updated']:
                self.__db['Updated'].update(new_record, ['Path'])
                return True
        # 上記以外はAsciiDoctorコマンドを実行しない。前回からAsciiDocファイルが更新されていないため
        return False
        
    """
    指定ファイルの最終更新日時を返す。
    @param {string} path_fileは更新日時が欲しいファイルのパス。
    @return {DateTime} ファイルの最終更新日時。
    """
    def __GetUpdatedByFileMetadata(self, path_file):
        return datetime.datetime.fromtimestamp(os.stat(path_file).st_mtime) # https://docs.python.jp/3/library/stat.html#stat.ST_MTIME
        # AttributeError: 'os.stat_result' object has no attribute 'ST_MTIME'
    
    """
    DBに接続する。DBがなければ作成する。
    """
    def __Initialize(self):
        if not os.path.isfile(self.__file_path):
            self.__CreateBlankFile()
            self.__CreateTable()
        else:
            self.__db = dataset.connect('sqlite:///' + self.__file_path)        

    """
    空ファイルを作成する。
    """
    def __CreateBlankFile(self):
        command = 'touch {0}'.format(self.__file_path)
        print(command)
        subprocess.check_output(command, shell=True)

    """
    ファイルの更新日時テーブルを作成する。
    """
    def __CreateTable(self):
        sql = """
create table "Updated"(
    "Id"            integer primary key,
    "Path"          text unique not null,
    "Updated"       text not null
);
"""
        self.__db = dataset.connect('sqlite:///' + self.__file_path)
        self.__db.query(sql)
        
