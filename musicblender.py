#!/usr/bin/python -tt
# encoding: utf-8
from eyeD3.tag import TagException

__author__ = "Diego Navarro"
__email__ = "dnmellen@gmail.com"
__version__ = 0.6


import sys
import os
from PyQt4 import QtCore, QtGui
from PyQt4.QtGui import *
from gui import Ui_MainWindow
import eyeD3 
import random
import itertools
import shutil


def merge_lists(a, b):
    '''
    Awesome function to merge equally two lists
    
    @param a: list
    @param b: list
    '''
    
    partial = list(itertools.izip_longest(a, b))
    partial_none = [e for e in partial if not all(e)]
    partial_good = [e for e in partial if all(e)]
    result = list(itertools.izip_longest(partial_good, partial_none))
    
    clean_res = reduce(list.__add__, 
                       [list(i) for i in 
                            [(e[0] or ()) + (e[1] or ()) for e in result]])
    return [e for e in clean_res if e]


class MyForm(QtGui.QMainWindow):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self,parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Signals/Slots
        QtCore.QObject.connect(self.ui.pushButton_Add1, QtCore.SIGNAL("clicked()"), self.add_songs1)
        QtCore.QObject.connect(self.ui.pushButton_Shuffle1, QtCore.SIGNAL("clicked()"), self.shuffle1)
        QtCore.QObject.connect(self.ui.pushButton_Delete1, QtCore.SIGNAL("clicked()"), self.delete1)
        QtCore.QObject.connect(self.ui.pushButton_Add2, QtCore.SIGNAL("clicked()"), self.add_songs2)
        QtCore.QObject.connect(self.ui.pushButton_Shuffle2, QtCore.SIGNAL("clicked()"), self.shuffle2)
        QtCore.QObject.connect(self.ui.pushButton_Delete2, QtCore.SIGNAL("clicked()"), self.delete2)
        QtCore.QObject.connect(self.ui.pushButton_Save, QtCore.SIGNAL("clicked()"), self.save)
        QtCore.QObject.connect(self.ui.actionAbout, QtCore.SIGNAL("activated()"), self.show_about)
    

    def add_songs1(self):
        self._add_songs("My songs", self.ui.groupMySongs, self.ui.tableWidgetMySongs)

    def add_songs2(self):
        self._add_songs("His/Her songs", self.ui.groupHerSongs, self.ui.tableWidgetHerSongs)

    def _add_songs(self, groupTitle, groupBox, table):
        '''
        Add songs to the table
        '''

        files = QtGui.QFileDialog.getOpenFileNames(self, 'Add songs', 
                                                   os.path.expanduser("~"), 
                                                   "Audio Files (*.mp3)")
        total_size = 0.0
        for filename in files:
            tag = eyeD3.Tag()
            try:
                # Patch for TagException: Multiple UFID frames not allowed 
                # with the same owner ID
                tag.link(unicode(filename))
            except TagException:
                pass
            size = os.path.getsize(unicode(filename)) / (1024.0 * 1024.0)
            total_size += size 
            self._create_table_item({'title': tag.getTitle(),
                                     'artist': tag.getArtist(),
                                     'size': "%.2f MB" % size,
                                     'path': unicode(filename)}, table)
            
        self._update_groupBox_label(table, groupTitle, groupBox)


    def _create_table_item(self, data, table):
        '''
        Create a table item
        
        @param data: dict
        '''
        
        new_rc = table.rowCount()
        table.setRowCount(new_rc + 1)
        table.setItem(new_rc, 0, QTableWidgetItem(data['title']))
        table.setItem(new_rc, 1, QTableWidgetItem(data['artist']))
        table.setItem(new_rc, 2, QTableWidgetItem(data['size']))
        table.setItem(new_rc, 3, QTableWidgetItem(data['path']))


    def shuffle1(self):
        self._shuffle(self.ui.tableWidgetMySongs)
        
    def shuffle2(self):
        self._shuffle(self.ui.tableWidgetHerSongs)

    def _shuffle(self, table):
        '''
        Shuffle rows
        '''
        
        data = [(table.item(i, 0).text(),
                 table.item(i, 1).text(),
                 table.item(i, 2).text(),
                 table.item(i, 3).text()) 
                    for i in xrange(table.rowCount())]
        random.shuffle(data)
        table.setRowCount(0)
        table.setRowCount(len(data))
        for i, row in enumerate(data):
            table.setItem(i, 0, QTableWidgetItem(row[0]))
            table.setItem(i, 1, QTableWidgetItem(row[1]))
            table.setItem(i, 2, QTableWidgetItem(row[2]))
            table.setItem(i, 3, QTableWidgetItem(row[3]))
    
    def _update_groupBox_label(self, table, groupTitle, groupBox):
        '''
        Update the groupBox label to show name, number of items and size
        '''
    
        groupBox.setTitle("%s (%d items, %.2f MB)" % (groupTitle, table.rowCount(), 
                                                      self._count_songs_size(table)))
    
    
    def _count_songs_size(self, table):
        '''
        Counts the size of the songs of a table
        '''
        
        files_size = sum([os.path.getsize(unicode(table.item(i, 3).text())) 
                          for i in xrange(table.rowCount())])
        
        return files_size / (1024.0 * 1024.0)
    
    
    def delete1(self):
        self._delete(self.ui.tableWidgetMySongs, "My songs", self.ui.groupMySongs)
        
    def delete2(self):
        self._delete(self.ui.tableWidgetHerSongs, "His/Her songs", self.ui.groupHerSongs)
    
    def _delete(self, table, groupTitle, groupBox):
        '''
        Shuffle rows
        '''
        
        table.removeRow(table.currentRow())
        self._update_groupBox_label(table, groupTitle, groupBox)
    
    def _get_songs(self, table):
        '''
        Returns list of file paths
        '''
        
        return [table.item(i, 3).text() for i in xrange(table.rowCount())]
        
    
    def save(self):
        '''
        Merge lists and save to disk
        '''
        
        
        mysongs = self._get_songs(self.ui.tableWidgetMySongs)
        hersongs = self._get_songs(self.ui.tableWidgetHerSongs)
        
        if not (mysongs and hersongs):
            QMessageBox.information(self, "Merge lists", "You need to fill up both song lists")
            return None
        
        # First select where to dump the files
        folder = QtGui.QFileDialog.getExistingDirectory(self, 'Select folder to save the files')
        if folder:
            folder_path = os.path.abspath(unicode(folder))
            merged_songs = merge_lists(mysongs, hersongs)
            
            QMessageBox.information(self, "Merge lists", 
                                    "%d files are going to be copied to %s" % (len(merged_songs), 
                                                                               folder_path.encode('utf-8')))
            for i, song_path in enumerate(merged_songs):
                dest_name = (u'%.4d-%s' % (i, os.path.basename(unicode(song_path))))
                shutil.copy(unicode(song_path).encode('utf-8'), os.path.join(folder_path, dest_name).encode('utf-8'))
    
            QMessageBox.information(self, "Merge lists", "Files copied OK!")
            
        
    def show_about(self):
        '''
        Show about dialog
        '''
        
        QMessageBox.about(self, "Music Blender", 
                          "Author: Diego Navarro Mellén\nLicense: GPLv3".decode('utf-8'))


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    myapp = MyForm()
    myapp.show()
    sys.exit(app.exec_())   
