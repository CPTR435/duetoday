# duetoday
#### (Student App)

## To Get the Code Locally
Download and Install git for windows:
https://git-scm.com/download/win
Select "Use in Windows Command Prompt" (the second option) when prompted

1. Open a command prompt window
2. Run ```cd C:\Users\%username%\Desktop``` to change to your desktop directory
3. Run ```git clone https://github.com/cptr435/duetoday``` to get a copy of all the files


## Working with the Files
cd into the duetoday directory before running these commands

### Getting new changes
```git pull```

### Pushing new changes
1. ```git add -u``` to add all updated files
2. ```git status``` to make sure there aren't any untracked files
  1. ```git add FILENAME``` for any NEW files
  2. Check ```git status``` and repeat
3. ```git commit -m``` will prompt you to write a short comment about your recent changes
4. ```git push``` will finally push all your changes to github


## To Run the Server
```
cd server
python server.py
```

The default url when running locally will be:
*http://localhost:8887/*
(Running on port 8887 by default)

Log files are stored in *server/etc/logs/*
