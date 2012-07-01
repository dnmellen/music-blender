music-blender
=============

Python app for avoiding arguments when you travel by car with your partner.

Basically it is an application for merging two playlists equally:

 - You have a GUI where you can add songs in any of the two lists
 - When you are finished choosing the songs you can push the *shuffle* button to randomly change the songs order
 - Now you are ready to press the big *save* button to merge both playlists and copy them to a folder where they will be stored in the correct order
 - Process finished, you can burn the folder containing all the merged mp3s to a CD and play it in your car!

This app is written in **Python** using **PyQt4** and it is still in development. Though it is usable for its main purpose, there may be bugs.

TODO
========

 - Save last path in *add files dialog*.
 - Add functionallity to save song's tables state to a file to avoid loosing all the work if the program is closed.
 - Add keyboard shortcuts.
 - Allow search in *add files dialog*.
 - Show a progress bar when merging and saving the files.
 - Check if a song is duplicated when adding files to the table.
 - Design a beautiful icon for the program.
 - Add button for clearing the tables.
 - Keep songs selected in table when are added.