---
layout: page
title: Bugs and Problems
permalink: /bugs-and-problems/
---

## General Notes

*The tips in this page were created for the owners of "Hype - The Time Quest"
working copies that are having compatibility issues and other bugs related to
the game. You'll still need a cd after following the steps.*

*The following fixes and instructions were elaborated to work with Hype The Time
Quest (English version). We are currently working on fixes for the other
versions as well, so keep checking back. Polish version added to the end of the
page.*

## Running Hype Under Windows 7 - 32 bit

If you try running the regular Hype executable file, you may experience problems
like black artifacts covering the screen, or the game not working at all.
However, this can be solved by playing the game using the other executable in
Hype's folder, the one that works with Glide drivers instead of Direct X ones.
To do this, you'll need to emulate a glide graphic board:

1. Download and install nGlide 0.96 (wrapper\emulator of the graphic card and
   the version that added support to Hype)\\
   <https://www.zeus-software.com/downloads/nglide>
2. Then find the file **glide3x.dll** inside your *"C:\Windows\System32"*
   folder and copy it to Hype's installation directory (Default is
   *C:\Ubi Soft\Hype - The time quest*)
3. Then, right-click the "MaiDFXvr_bleu.exe" file and select "proprierties"
4. Set the compatibility to **"Windows 95 or 98\me"**
5. Check all the boxes in the compatibility tab, specially "Run as
   Administrator"

Following these steps, Hype The Time Quest should now work perfectly. If
something fails, try changing the default settings on the nGlide configurator...
and you can always look for help in "[The Inn]({{ "/forum/" | relative_url }})"
(the archive of the old forum on this site).

This is it. Thank you a lot, Zeus for creating this amazing software.

## Running Hype Under Newer Systems - Things to Try

If you still can't start the game after using nGlide, you may want to try some
other things out.

### Patch

This patch can help you play Hype - The Time Quest on newer OS.

[hype_patch.zip]({{ "/assets/downloads/hype_patch.zip" | relative_url }})

Extract all the contents to your Hype - The Time Quest installation folder
(Default is *C:\Ubisoft\Hype - The Time Quest*).
Run the file PatchInstall.bat from there (Just double-click it).
You should be able to play Hype with no problems.

### Modifying the ubi.ini

If you can't get past the first movies in the game (or can't even get to the
movies) before the main menu, you may use this.

Open your ubi.ini file, that is located in *C:\Windows\UbiSoft*.
Find the line below `[Hype - The Time Quest]` that reads

```
playvideo = 1
```

and change it to

```
playvideo = 0
```

## Savegame Error

**UPDATE 26/03/2016**

Our member Spardo has pointed out a correct fix for this problem. When you
download install folders from hypeforever, you might have installed your fileds
somewhere else than *C:\Ubisoft\Hype - The Time Quest*. If that's the case, you
must goto *C:\Windows\UbiSoft* and change the line "Directory" (under
`[Hype - The Time Quest]`) to your current directory. Thanks Spardo, for this
fix!

## Installing Hype on 64-Bit Systems

If you own a 64 bit system, Hype installer will probably not install the game or
run correctly. It happens because the installer was developed in a 16-bit
environment, that was supported in 32 bit systems, but not in 64 ones. To be
able to run Hype, you must copy a installation folder from a 32 bit computer.

"But how do I do this?"

Install Hype in a Windows XP (or below) OS then copy the folder
**C:\Ubisoft\Hype - The Time Quest\\** to a cd\dvd\pendrive and paste it in the
same location in your computer.

After you get the folder in the correct place, download and install **nGlide**
(as explained above - the same process for Windows 7-32 bit).

**Note: In 64-bit systems, you'll find the glide3x.dll file in the following
folder *C:\Windows\SysWOW64\\***

## Video Tutorial - Installing Hype (Windows 7)

Our member, wimbertolf, was kind enough to make a video tutorial to aid everyone
having troubles while installing Hype. Thank you, wimbertolf! : )

{% include youtube.html id="2Y25Ui3VT2Q" title="Hype-The Time Quest Installation-Tutorial for Windows 7" %}

## Hype The Time Quest - German Version

Our member Marin (Enost) uploaded some save folders, that you can save over if
you get the savegame error in the German version:
[SaveGame.rar]({{ "/assets/downloads/savegames/german-savegame.rar" | relative_url }})

## Hype The Time Quest - Polish Version

Our memeber Spardo has created and uploaded a complete version of Hype - The
Time Quest installation folders for those who want to play it. It's a complete
install with nGlide, patches, savegame fix and all - although you'll still need
the cd to play it. Please visit this thread for more information. Also, be kind
and thank Spardo for the awesome work!

[Installation folders for foreign languages]({{ "/forum/topics/12376812-installation-folders-for-foreign-languages/" | relative_url }})

Our member Darnok_PL has created a savegame pack for those having troubles when
it comes to saving the game in the Polish version of Hype. You can download
those savegame files and write over them to fix your problem. You'll find the
files in the "[Downloads]({{ "/downloads/" | relative_url }})" section.

## Hype Under Mac / Linux

Member Grizzly Bear has kindly posted a tutorial on how to play under Mac /
Linux using Wineskin. You can check all the inf o on his
[original post]({{ "/forum/topics/9286503-hype-the-time-quest-on-mac/" | relative_url }}).

Don't forget to thank Mr. Grizzly Bear for his work!
