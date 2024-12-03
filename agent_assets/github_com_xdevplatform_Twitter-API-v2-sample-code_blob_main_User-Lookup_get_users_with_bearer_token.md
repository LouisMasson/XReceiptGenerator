URL: https://github.com/xdevplatform/Twitter-API-v2-sample-code/blob/main/User-Lookup/get_users_with_bearer_token.py
---


You signed in with another tab or window. Reload to refresh your session.You signed out in another tab or window. Reload to refresh your session.You switched accounts on another tab or window. Reload to refresh your session.Dismiss alert

{{ message }}

[xdevplatform](/xdevplatform)/ **[Twitter-API-v2-sample-code](/xdevplatform/Twitter-API-v2-sample-code)** Public

- [Notifications](/login?return_to=%2Fxdevplatform%2FTwitter-API-v2-sample-code) You must be signed in to change notification settings
- [Fork\\
1k](/login?return_to=%2Fxdevplatform%2FTwitter-API-v2-sample-code)
- [Star\\
2.8k](/login?return_to=%2Fxdevplatform%2FTwitter-API-v2-sample-code)


## Files

main

/

# get\_users\_with\_bearer\_token.py

Blame

Blame

## Latest commit

[![aureliaspecker](https://avatars.githubusercontent.com/u/32238702?v=4&size=40)](/aureliaspecker)[aureliaspecker](/xdevplatform/Twitter-API-v2-sample-code/commits?author=aureliaspecker)

[Change Python Requests to use auth= parameter instead of headers= to …](/xdevplatform/Twitter-API-v2-sample-code/commit/2fa0bfdb3a62dd4e544b6f4f334b2a557a395f49)

Jul 6, 2021

[2fa0bfd](/xdevplatform/Twitter-API-v2-sample-code/commit/2fa0bfdb3a62dd4e544b6f4f334b2a557a395f49) · Jul 6, 2021

## History

[History](/xdevplatform/Twitter-API-v2-sample-code/commits/main/User-Lookup/get_users_with_bearer_token.py)

52 lines (40 loc) · 1.48 KB

/

# get\_users\_with\_bearer\_token.py

Top

## File metadata and controls

- Code

- Blame


52 lines (40 loc) · 1.48 KB

[Raw](https://github.com/xdevplatform/Twitter-API-v2-sample-code/raw/refs/heads/main/User-Lookup/get_users_with_bearer_token.py)

1

2

3

4

5

6

7

8

9

10

11

12

13

14

15

16

17

18

19

20

21

22

23

24

25

26

27

28

29

30

31

32

33

34

35

36

37

38

39

40

41

42

43

44

45

46

47

48

49

50

51

52

importrequests

importos

importjson

\# To set your enviornment variables in your terminal run the following line:

\# export 'BEARER\_TOKEN'='<your\_bearer\_token>'

bearer\_token=os.environ.get("BEARER\_TOKEN")

defcreate\_url():

\# Specify the usernames that you want to lookup below

\# You can enter up to 100 comma-separated values.

usernames="usernames=TwitterDev,TwitterAPI"

user\_fields="user.fields=description,created\_at"

\# User fields are adjustable, options include:

\# created\_at, description, entities, id, location, name,

\# pinned\_tweet\_id, profile\_image\_url, protected,

\# public\_metrics, url, username, verified, and withheld

url="https://api.twitter.com/2/users/by?{}&{}".format(usernames, user\_fields)

returnurl

defbearer\_oauth(r):

"""

Method required by bearer token authentication.

"""

r.headers\["Authorization"\] =f"Bearer {bearer\_token}"

r.headers\["User-Agent"\] ="v2UserLookupPython"

returnr

defconnect\_to\_endpoint(url):

response=requests.request("GET", url, auth=bearer\_oauth,)

print(response.status\_code)

ifresponse.status\_code!=200:

raiseException(

"Request returned an error: {} {}".format(

response.status\_code, response.text

)

)

returnresponse.json()

defmain():

url=create\_url()

json\_response=connect\_to\_endpoint(url)

print(json.dumps(json\_response, indent=4, sort\_keys=True))

if\_\_name\_\_=="\_\_main\_\_":

main()

You can’t perform that action at this time.