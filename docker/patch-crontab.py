--- crontab.py  2024-09-17 06:56:19.752610239 +0000
+++ 2.py        2024-09-17 06:57:56.279127134 +0000
@@ -215,7 +215,7 @@
         return str(self) == other
 
 
-class CronTab:
+class CronTab(object):
     """
     Crontab object which can access any time based cron using the standard.
 
