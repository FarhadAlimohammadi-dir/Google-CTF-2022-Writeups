# Google-CTF-2022-Writeups


These  are my solutions for Google CTF 2022

This is my first official CTF (Capture The Flag) that will be held by a big company like Google so I hope you will enjoy my writeups.

# LOG4J

the first as the challenge says is about the log4j vulnerability. if you don't know what is that, I recommend seeing this video to have an idea of how it works:

https://www.youtube.com/watch?v=0-abhd-CLwQ

The challange URL is: https://log4j-web.2022.ctfcompetition.com

the website looks like this:

![](https://user-images.githubusercontent.com/89252882/177054957-412b0ad4-400e-4503-bfa0-c440e9882a4b.png)

there is a box that we can send some commands, also we can source in a file called `App.java` for the backend and the app server called `app.py` by checking the codes, we found out there that page working with some commands that are given by the source:

- help    --> prints hints for using it.
- /help --> same as `help`
- /wc --> it will count all words after the first space
- /repeat --> it will print the string after the first space
- /time --> it will show the time of the system

in the attachment's file, there are interesting files too, by checking the log4j2.xml file, we will see :

![](https://user-images.githubusercontent.com/89252882/177055655-b9852791-bec6-490c-b511-53a7d1b59f4f.png)

so we can use log4j vulnerability on the `${sys:cmd}` part
but how we can see, which command and how that variable will be initialized? To find that, we need to run the server locally and check its log output of it.
for example, I sent /repeat hello world to our chatbot box, and here is the output:

![](https://user-images.githubusercontent.com/89252882/177055812-da839fd1-5179-4ea9-bbcc-c0bb843823dd.png)

according to the picture, we can see the first string before space will be in `${sys:cmd}`. so we just need to send our payload in the first string before space, like the video I send above, the first thing we should do, checks vulnerability by a local variable such as :

- ${java:version}
- ${java:runtume}
- ${java:os}
- etc

so I will test with `${java:version}` we need to send `${java:version}` to our local server and check the output and see is working or not. here is the output:

![](https://user-images.githubusercontent.com/89252882/177056364-57e90858-b888-41c9-829a-51b109f514b6.png)

so we can see the payload working great, now we should send our main payload to get the flag. the second thing for getting access to a server like RCE, we need to use JNDI vulnerability, so we must check the version of log4j because it might use the version that vulnerability has been patched.

by checking the pom.xml file in the attachments we will see the Log4j version is 2.17.2.

![](https://user-images.githubusercontent.com/89252882/177056507-1222d74f-aaa7-4aa0-a09e-03b6793d2bf6.png)

so we will check if there is a vulnerability on that or not. the version used on this challenge doesn't have JNDI vulnerability so we need to find another way with that variable.

by guessing the parameter used in the request, we will face an interesting Exception. 
i sent this payload: `${java:flag}` xD and this happened.

![](https://user-images.githubusercontent.com/89252882/177056988-5e6a7c05-6df8-4b19-b849-fb8f5eca7c91.png)

so I decode to pass the real Flag variable according to App.java file

![](https://user-images.githubusercontent.com/89252882/177057023-91890358-daf6-4e09-b2de-0c19328cfe77.png)

that line means flag set in environment variables with `FLAG` name.

so our payload will be this: `${java:${env:FLAG}}` and the result will be:

![](https://user-images.githubusercontent.com/89252882/177057122-2f7f3f0f-2d9c-4427-bc51-676ac657ee16.png)


and the reason is stacktrace goes to stdout. here is the flag: `CTF{d95528534d14dc6eb6aeb81c994ce8bd}`


------------
