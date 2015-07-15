#!/usr/bin/perl

# Matthew Ireland, 11 July MMXV
# Strips LaTeX comments from $ARGV[0] and writes the new file to $ARGV[1].
# The file specified in $ARGV[1] shouldn't exist -- it's created by this script.

use strict;
use warnings;

my $in_filename = $ARGV[0] or die "No input file $!";
my $out_filename = $ARGV[1] or die "No output file $!";

open (my $INFH, '<', $in_filename) or die "Could not open '$in_filename' for reading $!";
open (my $OUTFH, '>', $out_filename) or die "Could not open '$out_filename' for writing $!";

while (my $line = <$INFH>) {
    if (!($line =~ /^%.*/)) {
	$line =~ s/\w*%.+$//g;
	print $OUTFH $line;
    }
}
