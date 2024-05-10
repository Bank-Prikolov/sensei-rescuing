# PyGame "Sensei Rescuing"
An action platformer in the Roguelike and Metroidvania genre, dedicated to the confrontation between Python and PHP, which includes completing levels, defeating enemies and a boss, interesting gameplay, as well as an original story, music, design and interface

> [!NOTE]
> This project includes [another repository](https://github.com/mikhalexandr/Flask-Sensei-Rescuing-API) where **the API for interacting with the leaderboard** is implemented

<details>
<summary><b>📑 Detailed Description</b></summary>
<b>Game screens:</b>
  <ul>
    <li>game menu windows:</li>
      <ol type="1">
        <li>Game home screen</li>
        <li>The loading window, when displayed using multithreading loads the necessary resources</li>
        <li>Main menu window, which includes a list of recent updates, character selection and four buttons: start, settings, about us, exit (to get the second character you need to go
          via a link to our another product</li>
        <li>Settings window, which includes a sound settings section (music volume, sound volume) and video settings section (screen expansion and language selection)</li>
        <li>The information window about us is not available due to the rules of the competition</li>
        <li>Level selection window, which includes three buttons: level 1, level 2, level 3 (boss); located under the buttons information about the level, namely: record completion time level and number of stars   that correspond to the record time. "Records" of the level are displayed after it passing. Also, until the first level is completed, the secondwill be inactive; until the second level is completed, the third   will be inactive. At the top right there is a button, when you hover over it you can see the delineation of the number of stars in accordance with record time</li>
      </ol>
    <li>game windows:</li>
      <ol type="1">
        <li>The level window includes the gameplay itself: movement character, cutscenes, defeating enemies, overcoming obstacles (see below for details); in the upper left corner are the character's lives; in the upper right corner there is a pause button. The level is divided into sublevels (first level – 1 sublevel, second – 2 sublevels, third – 3 sublevels); at sublevel with boss at the top of the screen displays the boss's health bar</li>
        <li>The pause window includes statistics about the level: quantity lives, time from the start of the level, number remaining enemies on the sublevel; three buttons: continue, replay, go to the levels menu; management section; adjusting the volume of music and sounds</li>
        <li>The Game Over window is displayed when a character loses, includes GAME OVER animation and buttons: replay, go to the levels menu</li>
        <li>The Level Passed window is displayed when the character wins, includes animation LEVEL PASSED, buttons: replay, go to the levels menu; time during which it was passed level and number of stars corresponding to this time</li>
        <li>On a sublevel with a boss, when you lose, a window appears, which includes the opportunity to repeat the passage sublevel or refuse this opportunity and lose</li>
      </ol>
  </ul>
<b>Game mechanics:</b>
  <ul>
    <li>to complete the level you need to overcome all obstacles and defeat all enemies</li>
    <li>the game includes several cutscenes - dialog boxes that immerse the player in the lore of the game (Enter – scroll through the dialogue)</li>
    <li>the character can walk (keys a, d), shoot (key w), fall down (s key), interact with the exit (w key). In Game there are two characters with different unique animations and ammo
    <li>the character Hleb is on the first level, when talking with him the player learns about necessary further actions</li>
    <li>opponents:</li>
      <ol type="1">
        <li>Elephant PHP. Usually there are several of them at a sublevel, looking to the left – right in a chaotic order. If the elephant looks to the side and the character is in his line of sight, he begins to shoot. Health Amount: 3</li>
        <li>Boss Kowlad. Located on sublevel 3.2, moves from using teleportation to several positions: up left, up center, up right, down right, down left. He does it after the attack. He shoots felt-tip pens that bounce off several times from the walls. There are different types of attacks: attack from above, attack from different places, attack with 3 markers, fan attack and calling elephants. The boss has two phases: the first is easy (attacks easier), the second one starts after 10 hits on the boss, is more complex (attacks more difficult). For example, in the first phase There is no call for elephants, but on the second it appears. Amount of health: 20 (10 hp – first phase, 10 hp – second phase)</li>
      </ol>
    <li>textures:</li>
      <ol type="1">
        <li>Blocks for the sub-level floor</li>
        <li>Blocks for sub-level walls</li>
        <li>Blocks for delimitation at the sublevel, 2 types</li>
        <li>Transparent trap blocks</li>
        <li>Spikes, if hit by which the character dies at any number of lives</li>
        <li>Platforms for raising and lowering</li>
        <li>Teleport arrows: I teleport between sublevels</li>
        <li>Key: opens the teleport arrow</li>
        <li>Boss teleport: teleports to the boss sub-level</li>
        <li>Door EXIT: level final</li>
      </ol>
  </ul>
</details>

## 🛠️ Tech Stack
ㅤ![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![PyGame](https://img.shields.io/badge/pygame-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Screeninfo](https://img.shields.io/badge/screeninfo-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![SQLite](https://img.shields.io/badge/sqlite-%2307405e.svg?style=for-the-badge&logo=sqlite&logoColor=white)
![Aseprite](https://img.shields.io/badge/Aseprite-FFFFFF?style=for-the-badge&logo=Aseprite&logoColor=#7D929E)
![FL Studio](https://img.shields.io/badge/FL%20Studio-9933CC?style=for-the-badge&logo=apple-music&logoColor=white)

## 🎯 Quick Start
* Clone the project to your computer from Github using the command:
```
git clone https://github.com/mikhalexandr/PyGame-Sensei-Rescuing.git
```

* Install all required dependencies from `requirements.txt`
```
pip install requirements.txt
```

* Run `main.py`

## 👾 Download Game
* You can visit the game page on [itch.io](mikhalexandr.itch.io/sensei-rescuing) and download it from there
* You can download `Sensei Rescuing.zip` from [this directory](https://github.com/mikhalexandr/PyGame-Sensei-Rescuing/tree/main/project%20product) and after that run `Sensei Rescuing.exe`
* You can download the project and run `Sensei Rescuing.exe` from [this directory](https://github.com/mikhalexandr/PyGame-Sensei-Rescuing/tree/main/project%20product)
