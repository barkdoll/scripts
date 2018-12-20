# Scripts for automating the daily monotony

## [Read a blog post about my automation revelation here](https://theguyjin.com/scripting-to-automate-tasks/)

As a self-proclaimed perfectionist whose attention to detail can sometimes stall my productivity _(read **OCD**)_, I found myself wanting to speed up a lot of the repetitive tedious tasks I was accumulating.

I have taken a series of small JavaScript hiatuses over my dev journey to branch off of my usual grind and learn something new. 

One of those things was **bash**.
Another one of those things was **python**.

Then I realized that scripting in these two languages was useful for system automation.

## And I was like OH YES.

This repo is just a list of scripts I have written to automate various productivity and data processing tasks. You can use them for reference or adapt them for your own automation needs. Also feel free to ask me questions about them if you are learning to script too. 

## Scripts Functionality Index

<dl>

  <dt>aac_192k_vbr.sh</dt>
  <dd>Convert current directory's <i><b>FLAC</b></i> files to <i><b>m4a</b> (192kbps, aac, lossy)</i> for playback and portability.  
  </dd>

  <dt>audio_raffle.py</dt>
  <dd>Select and open a random song from your music library for playback.<br>
    <b>requirements:</b><ol>
      <li>The <code>DATA_DIRS</code> variable must have at least one valid path to select music from. 
      <li>The <code>MEDIA_PLAYER</code> variable must contain the path to your media player's executable for playing back your music files (VLC is recommended).</li>
    </ol>
    <b>parameters:</b><ul>
      <li>(optional) add a genre as an argument to limit the search to a certain genre</li>
    </ul>
  </dd>


  <dt>bt_watch.sh / bt_watch_win10.sh</dt>
  <dd>Watch local IP for changes, and kill Bittorrent client on change.<br>
    <b>requirements:</b><ol>
        <li>(win10 version) The <code>BT_CLIENT</code> variable must be set to your torrent client's binary path (`*.exe`) containing the text files to be re-encoded.</li>
      </ol>
  </dd> 

  <dt>dupFinder.py</dt>
  <dd>Find and ouput file duplicates. Checks against file's content regardless of if file name differs.</dd>

  <dt>encode.py</dt>
  <dd>Re-encode a directory's text files to UTF-8.<br>
    <b>requirements:</b><ol>
      <li>The <code>DATA_DIR</code> variable must be set to a valid path containing the text files to be re-encoded. 
      <li>The <code>OUPUT_DIR</code> variable must be set as the output location for the newly encoded UTF-8 files.</li>
    </ol>
  </dd>
    

  <dt>ffmkv.sh</dt>
  <dd>Convert current directory's <b>Matroska files (*.mkv)</b> to <b>mp3</b> files for passive listening and daily language immersion.<br>
  <b>parameters:</b><ul>
      <li>(optional) a track number can be specified in the first argument (<code>$1</code>) to target a specific track to be re-encoded; if the file(s) have multiple audio tracks, and no track number is specified, the first audio track will be used by default</li>  
  </ul>
  
  </dd>

  <dt>ffmp4.sh</dt>
  <dd>Convert current directory's <b>*.mp4 / *.avi</b> files to <b>mp3</b> files for passive listening and daily language immersion.</dd>

  <dt>mux.sh - special script for AJATT/Japanese learners – contact me for usage info</dt>
  <dd>Multiplex two video files— the first containing your main audio and video stream, and the second containing your supplemental audio stream. I wrote this because some of the content I acquire has extra audio tracks and Matroska is so freakin' convenient for handling multiple audio tracks in video files.</dd>


  <dt>sentence_search.py</dt>
  <dd>Search a directory for all text files (must be UTF-8) containing a certain word and compile sentences into a single text file with filename references.</dd>

  <dt>video_raffle.py</dt>
  <dd>Select and open a random, video, movie, or series from your video library for playback.<br>
    <b>requirements:</b><ol>
      <li>The <code>DATA_DIRS</code> variable must contain at least one valid path with video files.</li>
      <li>The <code>SERIES_DIR_IDENTIFIER</code> must contain a string (usually the name of a subfolder) that identifies if the chosen file is in a series directory.</li>
      <li>The <code>MOVIE_DIR_IDENTIFIER</code> must contain a string (usually the name of a subfolder) that identifies if the chosen file is in a movie directory.</li>
      <li>The <code>MEDIA_PLAYER</code> variable must contain the path to your media player's executable for playing back your music files (VLC is recommended).</li>
    </ol>
    <b>parameters:</b><ul>
      <li>(optional) add the <code>--movie</code> flag if you would like to open a movie</li>
      <li>(optional) add the <code>--series</code> flag if you would like to open an entire series</li>
    </ul>
  </dd>
</dl>

