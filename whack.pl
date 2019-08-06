#!/usr/bin/perl
use warnings;
use strict;
use CGI qw(:standard);

{
  my $start = param("start");                 # The time the game started
  my $score = param("score");                 # The score
  my $last = param("last");                   # The last mole whacked
  my $time = time();                          # The time now
  if (!defined($start)){                      # If start is not defined
                                              # That means the game just started
    $start = $time;                           # So reset the time
    $score = 0;                               # And the score
  }
  if ($time > $start + 60) {                  # If the time ran out
    show_end($score);                         # Show the end menu
  } else {                                    # Otherwise
    show_page($start, $time, $score, $last);  # Show the page
  }
}

###########################################
# show_page                               #
# Inputs:                                 #
#   The start time,                       #
#   The time now,                         #
#   The score,                            #
#   The position of the last mole whacked #
# Outputs:                                #
#   A page showing the moles              #
###########################################
sub show_page {
  
  my($start, $time, $score, $last) = @_;      # Read inputs
  start();                                    # Start the page
  print h1("Whack-A-Mole"), "\nScore: " .     # Print the title
        $score, "\n<br>\nTime Left: ".        # Print the score
        (60 + $start - $time);                # Print the time left
  my $mole = $last;
  # Repeat this until the mole chosen this time is different
  # Than the one chosen last time
  until (not $mole == $last){
    $mole = int(rand(16));
  }
  my $i = 0;
  print "\n<table style='background-color: #ffffff'><tr>\n";                    # Start the table
  foreach $i (0..15) {                        # Repeat 15 times
  if (int($i / 4) == $i / 4 and not $i == 0){ # Every 4 times not including the first time
    print "</tr><tr>\n"                       # Finish the row and start a new one
  }
  print "<td>\n";                             # Start a table item
    if ($i == $mole) {                        # if this is where the mole is
      $score = $score + 1;                    # Increase the score
      print a({-href=>"whack.pl?".            # Make a link to itself
                  "start=$start&".            # Pass the paramaters
                  "score=$score&".
                  "last=$mole"}),             # The last one is this time's
                   img {src=>"/static/whack_img/mole.bmp"};     # An image of a mole
    } else {                                  # Otherwise
      print img {src=>"/static/whack_img/hole.bmp"};            # Put an image of a hole
    }
    print "</td>\n";                          # End the table item
  }
  print "</tr></table>\n";                    # End the table
  end();                                      # End the page
}
#############################################
# show_end                                  #
# Inputs:                                   #
#   The Score                               #
# Outputs:                                  #
#   A webpage showing the score and a menu  #
#############################################
sub show_end {
  my $score = $_[0];                          # Read the score
  start();                                    # Start the page
  print h2("Your time ran out!"),"\n";        # Tell the user their time ran out
  print p("Score: " . $score),"\n";           # Show the score
  print a({-href=>"whack.pl"},"Play agian?"); # A link to itself for a new game
  print "\n<br>\n";                           # A newline
  print a({-href=>"/"},"Quit"),"\n"; # A blank page for Quit
  end();                                      # End the page
}
#################################
# start                         #
# Inputs:                       #
#   None                        #
# Outputs:                      #
#   The beginning of a web page #
#################################
sub start {
#  print "Content-type: text/html\n\n";
#  print `/usr/bin/php header.php Whack-A-Mole`
#  print header(), start_html("Whack-A-Mole"); # Start the page with the title "Whack-A-Mole"
#  print header(), start_html(-title=>"Whack-A-Mole", -style =>{-src=>["stylesheet.css"],-media=> 'all'});
}
###########################
# end                     #
# Inputs:                 #
#   None                  #
# Outputs:                #
#   The end of a web page #
###########################
sub end {
  print h6("Made by Johan");                  # Print a message
#  print end_html();                           # End the page
#  print `/usr/bin/php footer.php`
}
