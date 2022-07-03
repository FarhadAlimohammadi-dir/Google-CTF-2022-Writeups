# Google-CTF-2022-Writeups


This is my solutions for Google CTF 2022 

This is my first offical CTF (Capture The Flag) that will be held by big company like Google so i hope you will enjoy to my writeups.

# LOG4J

at the first as the challenge says, its about the log4j vulnerablity. if you dont know what is that, i recommend to see this video to have a idea how it works:

https://www.youtube.com/watch?v=0-abhd-CLwQ

The challange URL is : https://log4j-web.2022.ctfcompetition.com

the website looks like this:

![](https://user-images.githubusercontent.com/89252882/177054957-412b0ad4-400e-4503-bfa0-c440e9882a4b.png)

there us a box that we can send some comamnds, also we can source of that page in file called `App.java` for backend and the app server called `app.py`
by checking the codes, we found out there that page working with some commands that given by the source:

- help    --> prints hints for using it.
- /help --> same as `help`
- /wc --> it will count all words after first space
- /repeat --> it will print the string after first space
- /time --> it will show the time of system

in attachments file, there is interesting files too, by checking the log4j2.xml file, we will see :

![](https://user-images.githubusercontent.com/89252882/177055655-b9852791-bec6-490c-b511-53a7d1b59f4f.png)

so the we can use log4j vulnerability on the `${sys:cmd}` part

but how we can see, which command and how that variable will be intialized?
for find that, we need to run the server locally and check the log output of it.

for example sent /repeat hello world to our chatbot box, and here is the output:

![](https://user-images.githubusercontent.com/89252882/177055812-da839fd1-5179-4ea9-bbcc-c0bb843823dd.png)

according to the picture, we can see the first string before space will be in `${sys:cmd}`.
so we just need to send our payload in first string before space, like video i send above, first thing we should do, is checking vulnerability by a local variable such as : 

- ${java:version}
- ${java:runtume}
- ${java:os}
- etc

so i wil test with`${java:version}`we need to send `${java:version}` to our local server and check the output and see is that working or not. here is output:

![](https://user-images.githubusercontent.com/89252882/177056364-57e90858-b888-41c9-829a-51b109f514b6.png)

so we can see the payload working great, now we should send our main paylod to get the flag. second thing for getting access to server like RCE, we need use jndi vulnerability, so we must check the version of log4j because it might using version that vulnerability has been patched.

by checking the pom.xml file in attachments we will see Log4j version is 2.17.2.

![](https://user-images.githubusercontent.com/89252882/177056507-1222d74f-aaa7-4aa0-a09e-03b6793d2bf6.png)

so we will check if there is vulnerability on that or not. the version used on this challange doesnt have jndi vulnerability so we need to find another way with that variable.

by guessing the parameter used in request, we will face with an interesting Exception.
i sent this payload: `${java:flag}` xD and this happend.

![](https://user-images.githubusercontent.com/89252882/177056988-5e6a7c05-6df8-4b19-b849-fb8f5eca7c91.png)

then i decode to pass the real Flag variable according to App.java file

![](https://user-images.githubusercontent.com/89252882/177057023-91890358-daf6-4e09-b2de-0c19328cfe77.png)

that line means flag set in envairement variables with `FLAG` name .

so our payload will be this: `${java:${env:FLAG}}` and the result will be:

![](https://user-images.githubusercontent.com/89252882/177057122-2f7f3f0f-2d9c-4427-bc51-676ac657ee16.png)

and here is the flag: `CTF{d95528534d14dc6eb6aeb81c994ce8bd}`


------------
