# Redmine Defect #28565 PDF export has too many whitespaces

2018-04-17 10:41 Tyler Nguyen

Status:

Priority:

Assignee:

Category:

Target version:

Resolution:

# Description

Closed

Normal

Go MAEDA

PDF export

3.3.9

Fixed

Start date:

Due date:

% Done:

Estimated time:

Affected version:

0%

0.00 hour

3.1.7

When exported in pdf format, there are too many whitespace under each note (attached).

As far as I can see, white space is automatically generated equal to the line number of the note.

I tested on Redmine 3.4.4.stable.17198 and Redmine 3.1.7.stable.17140, this issue persists.

Hope this issue is fixed soon.

Thank you !

# Associated revisions

# Revision 17574 2018-10-06 02:11 Go MAEDA

PDF export has too many whitespaces (#28565).

Contributed by Jun NAITOH.

Revision 17575 2018-10-06 02:17 Go MAEDA

Merged r17574 from trunk to 3.4-stable (#28565).

Revision 17576 2018-10-06 02:18 Go MAEDA

Merged r17574 from trunk to 3.3-stable (#28565).

# History

# #1 2018-04-17 12:49 Guillermo ML

I can confirm this behaviour on 3.3.1.stable, 3.4.3.stable and 3.4.4.stable

The number of blank lines after each note seems to be identical to the number of lines of text in the note.

# #2 2018-04-30 02:40 Go MAEDA

- Status changed from New to Confirmed
- Target version set to Candidate for next minor release


Reproducible in the current trunk (r17315).

# #3 2018-08-01 04:28 Tyler Nguyen

