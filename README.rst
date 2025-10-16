T O B
=====


**NAME**

|
| ``tobot`` - bot in reverse !
|

**SYNOPSIS**

|
| ``tobot <cmd> [key=val] [key==val]``
| ``tobot -cvaw [init=mod1,mod2]``
| ``tobot -d``
| ``tobot -s``
|


**DESCRIPTION**


``TOB`` has all you need to program a unix cli program, such as disk perisistence for configuration files, event handler to handle the client/server connection, easy programming of your own commands, etc.

``TOB`` contains python3 code to program objects in a functional way. it provides an “clean namespace” Object class that only has dunder methods, so the namespace is not cluttered with method names. This makes storing and reading to/from json possible.

``TOB`` is a python3 IRC bot, it can connect to IRC, fetch and display RSS feeds, take todo notes, keep a shopping list and log text. You can run it under systemd for 24/7 presence in a IRC channel.

``TOB`` is Public Domain.

|

**INSTALL**


installation is done with pipx

|
| ``$ pipx install tobot``
| ``$ pipx ensurepath``
|
| <new terminal>
|
| ``$ tobot srv > tob.service``
| ``$ sudo mv tobot.service /etc/systemd/system/``
| ``$ sudo systemctl enable tobot --now``
|
| joins ``#tobot`` on localhost
|

**USAGE**

use ``tobot`` to control the program, default it does nothing

|
| ``$ tobot``
| ``$``
|

see list of commands

|
| ``$ tobot cmd``
| ``cfg,dpl,exp,imp,mre,nme,pwd,rem,res,rss,syn``
|


**CONFIGURATION**

irc

|
| ``$ tobot cfg server=<server>``
| ``$ tobot cfg channel=<channel>``
| ``$ tobot cfg nick=<nick>``
|

sasl

|
| ``$ tobot pwd <nsvnick> <nspass>``
| ``$ tobot cfg password=<frompwd>``
|

rss

|
| ``$ tobot rss <url>``
| ``$ tobot dpl <url> <item1,item2>``
| ``$ tobot rem <url>``
| ``$ tobot nme <url> <name>``
|

opml

|
| ``$ tobot exp``
| ``$ tobot imp <filename>``
|


**COMMANDS**

|
| ``cfg`` - irc configuration
| ``cmd`` - commands
| ``dpl`` - sets display items
| ``exp`` - export opml (stdout)
| ``imp`` - import opml
| ``mre`` - display cached output
| ``pwd`` - sasl nickserv name/pass
| ``rem`` - removes a rss feed
| ``res`` - restore deleted feeds
| ``rss`` - add a feed
| ``syn`` - sync rss feeds
| ``ver`` - show version
|

**FILES**

|
| ``~/.tobot``
| ``~/.local/bin/tobot``
| ``~/.local/pipx/venvs/tobot/*``
|

**AUTHOR**

|
| Bart Thate <``bthate@dds.nl``>
|

**COPYRIGHT**

|
| ``tobot`` is Public Domain.
|
