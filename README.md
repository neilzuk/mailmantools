# mailman-tools
The purpose of this Python module is to provide a set of tools that allow you to subscribe, un-subscribe and get a list of
 addresses from the mailing list software Mailman v2.

## Required Packages
 `pip3 install lxml`

 `pip3 install requests`

## Example
### Create a MailmanTools instance
```
from mailmantools import MailmanTools

mmt = MailmanTools('https://www.example.com', 'mylist_example.com', 'adminpw')
```
### List of members
Returns an array of e-mail addresses. These are stored in a cache which
can be forcefully refreshed by passing the bool True into the getmembers method.
```
mmt.getmembers() # Will only query Mailman if cache is empty
mmt.getmembers(True) # Will query Mailman
```
### Add member
Returns True if successful. Nothing is returned if the member exists currently.
```
mmt.addmember('name@example.com')
```
### Remove member
Returns True if successful. Nothing is returned if the member does not exist currently.
```
mmt.removemember('name@example.com')
```