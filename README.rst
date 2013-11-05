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

Google Plus
------------

In this quick demo we show NLTK capabilities, from cleaning HTML tagged text 
to tokenization, frequency counting and collocations analysis. 
All in addition to Python's URL handling and JSON parsing.

Usage:

- python gplus.py

Cairo Traffic
--------------

In this demo, we want to parte tweets tagged with #CairoTraffic
so that we can tell the following variables in each tweet:

1. From: Where is the tweep going from.
2. To: Where is the tweep going to.
3. The traffic status being reported.

We have to files in the courpus, "corpus/cairotraffic.txt", 
and a short demo version, "corpus/cairotraffic.txt".
We have multiple function to run in the code, demo0, demo1, demo2, etc.
In demo0() we show the basic idea of PoS (Part of Speech) tagging.
Then in demo1() and demo2() we use both unigram and bigram taggers respectively 
to tag new tweets based on what is learnt from the trainig set.
Then in demo3() and demo4() we use Machine Learning techniques for better tagging.
Finally, in demo5() we use Machine Learning to tell traffic status from a tweet.

Usage:

- python cairotraffic.py

Francoarab
-----------

Francoarab, better known as Arabizi, is Arabic text written in Latin letters. 
In this examples we loaded some sentences from the Wikipedia page about Google in English.
We also loaded some sentences from twitter and Bey2ollak written in Francoarab.
Both were saved in the file, `"corpus/franco.txt" <https://github.com/gr33ndata/NLP_GDGCairo2013/blob/master/corpus/franco.txt>`_.
Then we used machine learning technique to learn patterns from each language,
then we can tell if any given text is in English or Francoarab.

To run the code type: python franco.py [some text here]

Usage:

- python franco.py mazzika
- python franco.py music
- python franco.py sab3a million
- python franco.py seven million
- python franco.py 7million
- python franco.py millou7a


Appendix
=========

Contacts and Links:

- Presentation Slides: http://tarekamr.appspot.com/slides/pynlp
- Homepage: http://tarekamr.appspot.com/slides/pynlp
- Twitter: https://twitter.com/gr33ndata
- Open Knowlege Foundation, Egypt: http://eg.okfn.org/







