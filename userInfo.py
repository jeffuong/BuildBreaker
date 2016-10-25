from P4 import P4, P4Exception
import sys
import argparse
import datetime

outString = ""
totalPushes = 0
userList = []

p4 = P4()
p4.port = "104.236.191.81:1666"
p4.user = "server"
p4.password = "12345"

def PrintPerforceErrors():
  for e in p4.errors:
    print (e)

#FullName, User
def AppendUsers():
  global userList
  users = p4.run("users")
  userSize = len(users) #getting the size of the members
  for i in range(0, userSize):
    userList.append(users[i]["User"])
    #for key in users[i]:
      #if key == "FullName":
      #if key == "User"
    
    
#path, time, user, client, status, desc, change, changeType
def PrintUserChanges(name):
  global outString
  argc = len(name)
  for user in userList:
    if(name[0] == user):
      if argc == 1:
        changes = p4.run("changes", "-i","-l","-u",name[0])
      elif argc == 2:
        print(name[1])
        changes = p4.run("changes", "-i", "-l","-u", name[0], "@"+name[1] + ",@now")
      elif argc == 3:
        changes = p4.run("changes", "-i", "-l","-u", name[0], "@"+name[1] + ",@"+name[2])
      totalPushes = len(changes)
      outString = name[0]  + " Changes\n"
      for i in range(0, totalPushes):
          dateTime = datetime.datetime.utcfromtimestamp( int( changes[i]["time"] ) )
          outString += "Change #" + changes[i]["change"] + "\nTime: " + str(dateTime) + "\nDescription: " + changes[i]["desc"] + "\n"
      return
  print(name[0],"is not in the list, please select user from the list", str(userList))
  PrintPerforceErrors()
  
def PrintUserPushes(name):
  global outString
  global totalPushes
  
  changes = p4.run("changes", "-l","-i","-u", name)
  totalPushes = len(changes)
  outString = name  + " has " + str(totalPushes) + " pushes"
  PrintPerforceErrors()
  
try:
  p4.connect()
  AppendUsers()
  parser = argparse.ArgumentParser(description='Perforce User Info Script')
  parser.add_argument("-c", "-changes", nargs='+' ,help="User, Date From, Date To, Format:YYYY/MM/DD\n" + str(userList))
  parser.add_argument("-p", "-pushes", nargs=1 ,help="List the number of file changes the user has made")
  #parser.add_argument("User", choices=userList, help="Choose Users")
  args = parser.parse_args()

  if args.c:
    PrintUserChanges(args.c)
  elif args.p:
    PrintUserPushes(args.p[0])
  print(outString)
  
except P4Exception:
  PrintPerforceErrors()