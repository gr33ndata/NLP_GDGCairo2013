NLP at GDG Cairo2013
=====================

This github repository contains the code used in my presentation in GDG Cairo about Natural Language Processing in Python. You can find the session slides `here <http://tarekamr.appspot.com/slides/pynlp>`_

Prerequisites
==============

Before running the code here, you need to make sure you have the following libraries installed, after making sure that you already have the `Python programming language <http://www.python.org/>`_ installed on your computer::

Natural Language Toolkit, `NLTK <http://nltk.org/>`_ 

Machine learning in Python, `Scikit-Learn <http://scikit-learn.org>`_

Examples 
=========

Francoarab
-----------

Francoarab, better known as Arabizi, is Arabic text written in Latin letters. 
In this examples we loaded some sentences from the Wikipedia page about Google in English.
We also loaded some sentences from twitter and Bey2ollak written in Francoarab.
In this example we used machine learning technique to learn patterns from each language,
then we can tell if any given text is in English or Francoarab.

To run the code type: python franco.py [some text here]

Examples:
- python franco.py mazzika
- python franco.py music
- python franco.py sab3a million
- python franco.py seven million
- python franco.py 7million
- python franco.py millou7a






