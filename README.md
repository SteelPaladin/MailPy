# MailPy
A lightweight email client created within Python 3.
@author SteelPaladin - Harrison Baillie

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ v.1.2 ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Designed for personal A2 Coursework and created using Python 3.6.1, available to all to use.
Currently only works with Gmail accounts (@gmail.com OR @googlemail.com). Working on implementing other
email providers (Microsoft, Yahoo, etc.) 
Takes advantage of in-built Python libraries (smtplib/imaplib/email) and uses Tkinter for the GUI interface.
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

UPDATE NOTES:
Version 1.0 released on 11-10-17, the first fully working iteration allowing both listing and viewing of
the user's emails as well as sending emails, now with the standard MIME framework allowing for an email
to be sent as a proper object (subject/recipient/payload).

Version 1.2. released on 13-10-17 fixed issues with shell errors still appearing when network access denied.
This was fixed by placing an exception statement around the block of issue, catching the IMAP4 error and its 
consequential UnboundLocalError's from both rv and data variables. The program now runs smoother, and with 
increased fluidity.
