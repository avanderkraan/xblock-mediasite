# xblock-mediasite
This XBlock gives the ability to access a Sonic Foundry Mediasite. The TU Delft has a mediasite called Collegerama, where a lot of recorded lectures, presentations and live events are stored.<br/>
With this XBlock a teacher or course maker can select a part of a recording to use in an edX online course.

## Requirements
This XBlock needs credentials in order to access the mediasite API server.<br/>
The credential software can be found on [https://github.com/avanderkraan/xblock-mediasite-credentials](../../../xblock-mediasite-credentials/blob/master/README.md)

### Installation
The installation of XBlocks is described on [https://github.com/edx/edx-platform/wiki/Installing-a-new-XBlock](https://github.com/edx/edx-platform/wiki/Installing-a-new-XBlock)

### Screenshots
There are some screenshots available to give you an impression about what this XBlock does.<br/>
The XBlock has two views. One for the course-maker, called studio view, and one for the student.<br/>

#### Studio view
1. Give a title and description<br/>
![Title and description](../../blob/master/screenshots/Studio_view_1.png?raw=true)
<br/>
2. Search a course on the mediasite server<br/>
![Course selection](../../blob/master/screenshots/Studio_view_2.png?raw=true)
<br/>
3. Select the course and select the video fragment, using the begin time and end time<br/>
![Fragment selection](../../blob/master/screenshots/Studio_view_3.png?raw=true)

#### Student view
This is what a student sees following a course with de mediasite XBlock<br/>
![Fragment selection](../../blob/master/screenshots/Student_view.png?raw=true)

# NOTE
This software is under developing and almost in test phase ...
