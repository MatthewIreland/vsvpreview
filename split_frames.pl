#!/usr/bin/perl

# Matthew Ireland, 11 July MMXV
# Takes a LaTeX file in $ARGV[0] and a working directory name in $ARGV[1].
# Splits each frame into a new .tex file in a new folder, ready for parsing.

my $in_filename = $ARGV[0] or die "No input file $!";
my $working_dir = $ARGV[1] or die "No working directory $!";

open ($INFH, '<', $in_filename) or die "Could not open '$in_filename' for reading $!";
my $OUTFH, my $frame_type, my $start_time, my $end_time, my $dir_name;

my $inframe = 0;
my $file_count = 0;

while (my $line = <$INFH>) {
    if ($inframe) {
	if ($line =~ /\\end{vsvframe}/) {
	    $inframe = 0;
	} else {
	    print $OUTFH $line;
	}
    } else {
	if ($line =~ /\\begin{vsvframe}{([\d\-:\.]+)}{([\d\-:\.]+)}{(left|right)}/) {
	    $frame_type = $3;  # left or right
	    $start_time = $1;
	    $end_time = $2;
	    $file_num = sprintf("%04d", $file_count);
	    open($OUTFH, '>', "${working_dir}/src_${file_num}_${start_time}_${end_time}_${frame_type}.tex") or die "Failure to open intermediate file for writing, $!";
	    $inframe = 1;
	    $file_count += 1;
	}
    }
}
