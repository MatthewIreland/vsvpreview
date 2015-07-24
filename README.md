LaTeX preview script
===================

Matthew Ireland, 11 July MMXV


Usage
-----
Ensure the vsvpreview directory is on your $PATH. Then run `vsvpreview <source_file.tex>` from the directory of the LaTeX source file. A pdf file will be generated for each frame, named `source_file_<left/right>_<frame num>.pdf` in the same directory.


Requirements and setup
---------------------
In FC22, run the following to make sure all requirements are installed and to perform the setup:

```
sudo yum update
sudo yum install python perl cpan python-pip pdftk
sudo pip install ply
sudo cpan install File::Slurp
cd <install directory|>
git clone TODO
echo 'PATH="${PATH}:<install directory>"' >> ~/.bash_profile
echo 'export PATH' >> ~/.bash_profile
. ~/.bash_profile
```

You will need access to the private repository on GitHub.


Supported syntax
----------------
TODO

Note that you can't have an empty timecode in a frame header, because the frame might overlap multiple segments!


Known bugs
----------
* Whitespace is needed before each vsv command. So `~ \vsvcorrect{...}` is correct, but `~\vsvcorrect{...}` is not.

* If writing a VSV to be played during a positive leap second, the 61st second in the minute will be rejected as invalid. The behaviour is undefined, since it largely depends on the video player. This is mitigated by the fact that a leap second will never take place during a VSV. Negative leap seconds should work just fine, subject to the occurrence of kernel panic.


Development TODOs
-----------------
* Parallelise frame processing (set up a thread pool)
* Stop spawning the Perl interpreter so much!
* Grey overlays for images


Support
-------
`mti20@cam.ac.uk` / 07921 137 653