# FBGrpExtraction
Group Member extraction from Facebook

Please follow steps mentioned below.

### Update fb.conf
  Update your username and password in fb.conf.


### Get Facebook Group ID
1. go to desired facebook group page.

2. get the ID from the URL
https://www.facebook.com/groups/XXXXXXXXXXXXXXXXXXXXXXXXXXX/

copy XXXXXX value as ID from the URL.

### Run extraction script

python fbgrp.py <fb_group_id>

Replace fb_group_id with ID Copied before.

```
python fbgrp.py mygroup
```
