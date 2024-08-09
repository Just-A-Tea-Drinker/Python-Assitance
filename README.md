# Python-Assitance
This is a project to try and tackle computer control using voice commands currently only supported for Windows only.
This project is designed to be free and accessible as possible which is why features such as chat gpt haven't been included but a module can be easily implemented that does
## Operation
### Dependantcies
These are the libraries needed
```
pip install pyKey selenium spacy word2number python-Levenshtein librosa pygame sounddevice soundfile pygetwindow screeninfo pypiwin32
```
addition resources needed
```
python -m spacy download en_core_web_sm
```
To run the code simply run located in main program
```
main_shell.py
```
## Features
- The assistant a nice looking "face" a audio visualiser that dynamically chnages with speech inspired by: https://www.youtube.com/watch?v=Wm7jJGcH06o&t=1s
  
- The assistant is currently able to open shortcuts on your desktop that are in the format or .url or .lnk files
  
- Due to the limitations of traversing the internet using python the youtube feature uses selenium which uses Microsft edge (opera gx isnt supported yet from what i could gather) this means there will be ad which can be attempted to skipped (3 second ads can be skipped, but unskippable ads the page will attempt a refresh)
  
- From a provides list of contacts you can also send emails to people! This is a simple email and doesnt include attachments or CC or bCC imagine trying to say other email/contact name in additon to a file location

- App management, your assistant not only can open and close them, but is able to minimise, maximise, select and move them between monitors (if you have more than one, duh)

- This project uses a modular design meaning additional features can be bolted on with minimal changes to the main_frame

## Possible upgrades
- google tts is slow but accurate, some kind of audio stream processing would be better
- Adding more advanced LLM features like ChatGPT for more of a flexible use, for example searching for information. the weather etc.

# Command list:
Note: all commands must be activated by saying computer
## Main commands
| Command  | Actions |
| ------------- | ------------- |
| open  | This combined with an app name will open the application or game on the desktop  |
| close  | This combined with an app name will close the application or game currently running  |
| minimise  | This combined with one or more applications will minimise them |
| maximise  | This combined with one or more applications will maximise them |
| select/switch to/swap to  | This combined with application name will select that app and make it the main focus |
| send email  | This combined with a contact name will begin the process of filling out an email to a contact |

## Youtube Controls
Note: this is simply the youtube shortcuts, they are very useful so if you know what they are you know what to say
| Command  | Actions |
| ------------- | ------------- |
| search  | Simply say computer search xyz and the search bar will magically be filled  |
| close  | This will kill the Youtube feature and return to the main_frame  |
| play/pause  | This will play/pause the video  |
| un/mute  | This will activate or deactivate the sound to the media |
| fast forward 5/10  | Depending on the amount selected this will fastword the media by 5 or 10 seconds |
| rewinds backwards 5/10  | Depending on the amount selected this will rewind the media by 5 or 10 seconds |
| next/previous frame  | The video must be paused and this will go to either the previous or next frame |
| (speed up/slow down)/(increase playbac)  | Depending on the amount selected this will rewind the media by 5 or 10 seconds |
| beginning  | Mkaes the video start from the beginning |
| increase/decrease volume  | This will increase of decrease the playback volume accordingly |
| full screen  | Makes the video go into full screen mode |
| exit full screen  | This will make the video exit full screen mode |
| skip ad/advert skip  | This will attempt to skip the advert if its skippable if not the page refreshes |
| next video  | This will skip to the next video |
| previous video  | If currently within a playlist or mix this allows to go back |
| next/previous reel  | If currently viewing reels this will go to the next or previous reel |
| read video/reel titles  | This will begin to read the titles of either reels or vidoe titles |
| stop  | When the assistant is reading titles this will stop this process |
| click/select  | This is used to select or click on a video or reel of your choosing by saying its title |




# known bugs/Inconviences
- Launching the youtube feature uses a thread to activate, despite it being a thread this process seems to freeze the main program unitill the "computer close youtube" is said

