--- crontab.orig.py	2021-10-21 12:51:27.016454632 +0000
+++ crontab.py	2021-10-21 12:51:29.392466805 +0000
@@ -198,7 +198,7 @@ def _unicode(text):
     return text
 
 
-class CronTab:
+class CronTab(object):
     """
     Crontab object which can access any time based cron using the standard.
 
