gogrepo gamma
--------------
Python-based tool for downloading your GOG.com game collections and extras to your local computer for full offline enjoyment.

It is a clean standalone python script that can be run from anywhere. It requires a typical Python 2.7 or Python 3 installation and html5lib, requests and pyOpenSSL.

By default, game folders are saved in the same location that the script is run in. You can also specify another
directory. Run gogrepo.py -h to see help or read more below. Each game has its own directories with all game/bonus files saved within.

License: GPLv3+

Features
--------
* Ability to choose which games to download based on combinations of OS (windows, linux, mac) and language (en, fr, de, etc...)
* Saves a !info.txt in each game folder with information about each game/extra item.
* Creates a !serial.txt if the game has a special serial/cdkey (I know, not 100% DRM-free, is it?). Sometimes coupon codes are hidden here!
* Verify your downloaded collection with full MD5, zip integrity, and expected file size checking.
* Auto retrying of failed fetch/downloads. Sometime GOG servers report temporary errors.
* Download resume support for interrupted downloads where possible.
* Ability to import your already existing local collection.
* Easy to throw into a daily cronjob to get all the latest updates and newly added content!
* Clear logging prints showing update/download progress and HTTP errors. Log files are created by default but can be disabled.

Quick Start -- Typical Use Case
----------------

* Login to GOG and save your login cookie for later commands. Your login/pass can be specified or be prompted. You generally only need to do this once to create a valid gog-cookies.dat

  ``gogrepoc.py login``

* Fetch all new and updated game and bonus information from GOG for items that you own and save into a local manifest file. Run this whenever you want to discover newly added games or game updates.

  ``gogrepoc.py update``

* Download the games and bonus files for the OS and languages you want for all items known from the saved manifest file.

  ``gogrepoc.py download``

* Verify and report integrity of all downloaded files. Does MD5, zip integrity, and expected filesize verification. This makes sure your game files can actually be read back and are healthy.

  ``gogrepoc.py verify``

Running in a (Docker) container
----------------

* The python script and all its dependencies is also available as a container image. Only a container engine like [Docker](https://docs.docker.com/engine/) or [Podman](https://docs.podman.io/en/latest/index.html) need to be installed.

  ``docker run ghcr.io/proudier/gogrepoc:docker update``

* The working directory in the container is `/srv`, so unless you specify a volume, the files will be downloaded there but will be lost when the container is deleted.

  ``docker run --rm -v /tank/gogrepo:/srv ghcr.io/proudier/gogrepoc:docker update``

Advanced Usage -- Common Tasks
----------------

* Add new games from your library to the manifest.

  ``gogrepoc.py update -os windows -lang en de -skipknown``

* Update games with the updated tag in your libary.

  ``gogrepoc.py update -os windows -lang en de -updateonly``

* Update one or more specified games in your manifest.

  ``gogrepoc.py update -ids trine_2_complete_story``

* Download one or more specified games game in your manifest.

  ``gogrepoc.py download -ids trine_2_complete_story``

Commands
--------

``gogrepoc.py login`` Authenticate with GOG and save the cookie locally in gog-cookies.dat file. This is needed to do
update or download command. Run this once first before doing update and download.

    login [username] [password]
    username    GOG username/email
    password    GOG password


If the login fails because of a reCatch, log to gog.com in a browser and extract the values of the following cookies:
- sessions_gog_com
- gog-al

Then use this template to generate the gog-cookies.dat file (replace the `REPLACE_ME`):

```
Set-Cookie3: sessions_gog_com="REPLACE_ME"; path="/"; domain=".gog.com"; path_spec; domain_dot; expires="2023-03-26 13:18:33Z"; httponly=true; secure=true; version=0
Set-Cookie3: gog-al="REPLACE_ME"; path="/"; domain=".gog.com"; path_spec; domain_dot; expires="2023-03-26 13:18:33Z"; httponly=true; secure=true; version=0
```

--

``gogrepoc.py update`` Fetch game data and information from GOG.com for the specified operating systems and languages. This collects file game titles, download links, serial numbers, MD5/filesize data and saves the data locally in a manifest file. Manifest is saved in a gog-manifest.dat file

    update [-os [OS [OS ...]]] [-lang [LANG [LANG ...]]] [-skipknown | -updateonly | -id <title>]
    -os [OS [OS ...]]    	operating system(s) (ex. windows linux mac)
	-skipos				 	skip operating system(s)
							Can't be used with -os
    -lang [LANG [LANG ...]] game language(s) (ex. en fr de)
	-skiplang				skip game language(s)
							Can't be used with -lang
	-standard				update new and updated games only (default unless -ids used)
							Can't be used with -skipknown, -updateonly, -full
    -skipknown            	only update new games in your library
    -updateonly           	only update games with the updated tag in your library
	-full				  	update all games on your account (default if -ids used)
	-ids <title>		  	id(s)/titles(s) of (a) specific game(s) to update
    -id <title>           	specify the game to update by 'title' from the manifest. Deprecated by -ids
							<title> can be found in the !info.txt of the game directory
	-skipids <title>	  	id(s)/titles(s) of (a) specific game(s) not to update
	-resumemode			  	how to handle resuming if necessary: noresume, resume, or onlyresume. Default: resume
	-strictverify 		  	clear previously verified unless md5 match
	-skiphidden			  	skip games marked as hidden
	-installers			  	GOG Installer type to use: galaxy, standalone or both. Default: standalone
	-wait <WAIT>			wait this long in hours before starting

--

``gogrepoc.py download`` Use the saved manifest file from an update command, and download all known game items and bonus files.

    download [-dryrun] [-skipextras] [-skipextras] [-skipgames] [-wait WAIT] [-id <title>] [savedir]
    savedir      	   directory to save downloads to
    -dryrun      	   display, but skip downloading of any files
    -skipextras  	   skip downloading of any GOG extra files
    -skipgames   	   skip downloading of any GOG game files. Deprecated by -skipgalaxy, -skipstandalone and -skipshared
	-skipgalaxy  	   skip downloading Galaxy installers
    -skipstandalone    skip downloading standlone installers
    -skipshared 	   skip downloading installers shared between Galaxy and standalone
	-skipfiles <file>  file name (or glob patterns) to NOT download
    -wait <WAIT>   	   wait this long in hours before starting
	-ids <title>	   id(s) or title(s) of the game in the manifest to download
    -id <title>  	   specify the game to download by 'title' from the manifest. Deprecated by -ids
					   <title> can be found in the !info.txt of the game directory
    -skipids <title>   id(s) or title(s) of the game(s) in the manifest to NOT download, default=[])
    -os [OS [OS ...]]  download game files only for operating system(s) (ex. windows linux mac)
	-skipos			   skip downloading game files for operating system(s)
					   Can't be used with -os
    -lang [LANG [LANG ...]] download game files only for language(s) (ex. en fr de)
	-skiplang		   skip downloading game files for language(s)
					   Can't be used with -lang
--

``gogrepoc.py verify`` Check all your game files against the save manifest data, and verify MD5, zip integrity, and
expected file size. Any missing or corrupt files will be reported.

    verify [-skipmd5] [-skipsize] [-skipzip] [-delete] [gamedir]
    gamedir     directory containing games to verify
	-forceverify (also verify files that are unchanged (by gogrepo) since they were last successfully verified)
    -skipmd5    	   do not perform MD5 check
    -skipsize   	   do not perform size check
    -skipzip    	   do not perform zip integrity check
	-skipextras  	   skip verification of any GOG extra files
    -skipgames   	   skip verification of any GOG game files. Deprecated by -skipgalaxy, -skipstandalone and -skipshared
	-skipgalaxy 	   skip verification of any GOG Galaxy installer files
    -skipstandalone    skip verification of any GOG standalone installer files
    -skipshared 	   skip verification of any installers included in both the GOG Galalaxy and Standalone sets
	-skipfiles <file>  file name (or glob patterns) to NOT verify
    -ids <title>	   id(s) or title(s) of the game in the manifest to verify
    -id <title>  	   specify the game to verify by 'title' from the manifest. Deprecated by -ids
					   <title> can be found in the !info.txt of the game directory
    -skipids <title>   id(s) or title(s) of the game(s) in the manifest to NOT verify, default=[])
    -os [OS [OS ...]]  verify game files only for operating system(s) (ex. windows linux mac)
	-skipos			   skip verification of game files for operating system(s)
					   Can't be used with -os
    -lang [LANG [LANG ...]] verify game files only for language(s) (ex. en fr de)
	-skiplang		   skip downloading game files for language(s)
					   Can't be used with -lang
	-delete    		   delete any files which fail integrity test
	-clean 			   clean any files which fail integrity test

--

``gogrepoc.py import`` Search an already existing GOG collection for game item/files, and import them to your
new GOG folder with clean game directory names and file names as GOG has them named on their servers.

    import [src_dir] [dest_dir]
    src_dir     	   source directory to import games from
    dest_dir    	   directory to copy and name imported files to
	-skipgalaxy  	   skip importing Galaxy installers
    -skipstandalone    skip importing standlone installers
    -skipshared 	   skip importing installers shared between Galaxy and standalone
	-ids <title>	   id(s) or title(s) of the game in the manifest to import
    -skipids <title>   id(s) or title(s) of the game(s) in the manifest to NOT import, default=[])
    -os [OS [OS ...]]  import game files only for operating system(s) (ex. windows linux mac)
	-skipos			   skip importing game files for operating system(s)
					   Can't be used with -os
    -lang [LANG [LANG ...]] import game files only for language(s) (ex. en fr de)
	-skiplang		   skip importing game files for language(s)
					   Can't be used with -lang
--

``gogrepoc.py backup`` Make copies of all known files in manifest file from a source directory to a backup destination directory. Useful for cleaning out older files from your GOG collection.

    backup [src_dir] [dest_dir]
    src_dir     	   source directory containing gog items
    dest_dir    	   destination directory to backup files to
	-skipextras  	   skip backup of any GOG extra files
    -skipgames   	   skip backup of any GOG game files. Deprecated by -skipgalaxy, -skipstandalone and -skipshared
	-skipgalaxy  	   skip backup of Galaxy installers
    -skipstandalone    skip backup of standlone installers
    -skipshared 	   skip backup of installers shared between Galaxy and standalone
	-ids <title>	   id(s) or title(s) of the game in the manifest to backup
    -skipids <title>   id(s) or title(s) of the game(s) in the manifest to NOT backup, default=[])
    -os [OS [OS ...]]  backup game files only for operating system(s) (ex. windows linux mac)
	-skipos			   skip backup of game files for operating system(s)
					   Can't be used with -os
    -lang [LANG [LANG ...]] backup game files only for language(s) (ex. en fr de)
	-skiplang		   skip backup of game files for language(s)
					   Can't be used with -lang
--

``gogrepoc.py clean`` Clean your games directory of files not known by manifest. Moves files to the !orphaned folder.

    clean [-dryrun] [cleandir]
    cleandir    root directory containing gog games to be cleaned
    -dryrun     do not move files, only display what would be cleaned

--

``gogrepoc.py trash`` Permanently remove orphaned files in your game directory.

    trash [-dryrun] [-installersonly] [gamedir]
    gamedir    		root directory containing gog games
    -dryrun     	do not move files, only display what would be trashed
	-installersonly only delete file types used as installers

--

Other arguments:
	-h, --help  	show help message and exit. Used in all commands.
	-nolog 			don't write to log file gogrepo.log. Used in all commands.
	-v, --version	show version number and exit. Used in all commands.

Requirements
------------
* Python 2.7 / Python 3
* html5lib 0.99999 or later (https://github.com/html5lib/html5lib-python)
* requests
* pyOpenSSL
I recommend you use `pip` to install the above python modules.

  ``pip install html5lib html2text``

Optional
------------------------

* html2text 2015.6.21 or later (https://pypi.python.org/pypi/html2text) (optional, used for prettying up gog game changelog html)
*nix:
* dbus-python and required dependencies (*nix, optional, used to prevent suspend/sleep interrupts on *nix, where supported) (this will likely move to pydbus as it matures)
Mac:
* caffeinate support (optional, required to prevent suspend/sleep interrupts)


TODO
----
* ~~add ability to update and download specific games or new-items only~~
* ~~add 'clean' command to orphan/remove old or unexpected files to keep your collection clean with only the latest files
* support resuming manifest updating
* ~~add support for incremental manifest updating (ie. only fetch newly added games) rather than fetching entire collection information~~
* ability to customize/remap default game directory name
* add GOG movie support
* ... feel free to contact me with ideas or feature requests!
