#!/usr/bin/perl

use warnings;
use strict;
use CGI qw(:standard);

my $num_questions = param("questions");

start();

my $num_right = 0;
print '<table border="0">',"\n";

for(my $i = 1; $i <= $num_questions; $i++) {
  # the problem
  my $p = param("p".$i);
  # the answer the user gave
  my $a = param("a".$i);

  if (not $p =~/(\d{1,2})\s(\+|\-)\s(\d{1,2})/ ) {
    print "</table>";
    print h3("Input Error!"),"<br>","The program is now stopping.";
    end();
    exit(0);
  }

  # the real answer
  my $real_a = eval $1.$2.$3;
  # show the problem and answer...
  print "<tr><td>$p</td><td>=</td><td>$a</td><td>";
  # check to see if the answer was right or wrong
  if ($a == $real_a and $a !~/[^0-9]/) {
    # tell the user that he got it right, and record it
    print "Correct\!";
    $num_right++;
  } else {
    # tell the user that he got it wrong
    print "Incorrect\!</td><td>correct answer:$real_a";
  }
  print "</td></tr>\n";
}

print "</table>";

# find the user's score and print it
my $score = int($num_right / $num_questions * 100 + 0.5);
print "score: ",$score,"\%";

print '<br><a href="math">Play Again?</a>',"\n";
print '<br><a href="/">Quit</a>',"\n";

end();

#################################
# start                         #
# Inputs:                       #
#   None                        #
# Outputs:                      #
#   The beginning of a web page #
#################################
sub start {
#  print "Content-type: text/html\n\n";
#  print `/usr/bin/php ../header.php`
#  print header(), start_html("The Math game");
#  print header(), start_html(-title=>"The Math Game", -style =>{-src=>["../stylesheet.css"],-media=> 'all'});
}
###########################
# end                     #
# Inputs:                 #
#   None                  #
# Outputs:                #
#   The end of a web page #
###########################
sub end {
  print h6("Made by Johan");
#  print `/usr/bin/php ../footer.php`
#  print end_html();
}
