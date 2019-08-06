#!/usr/bin/perl
use warnings;
use strict;
use CGI qw(:standard);

{
  my $doors = param("doors");
  my $rooms = param("rooms");
  my $current_room = param("current_room");
  my $door_choice = param("door_choice");
  my $offset = param("users");
  my @real_doors = decode_doors($offset);


  if (!defined($offset)){
    @real_doors = make_real_doors($rooms,$doors);
    $offset = int(rand(100));
    $current_room = 0;
    $door_choice = -1;
    show_page($rooms,$doors,$current_room,$door_choice,$offset,
    "Choose a door:",@real_doors);
  } elsif ($real_doors[$current_room]!=$door_choice){
    show_page($rooms,$doors,$current_room,$door_choice,$offset,
    "Wrong answer; choose another door:",@real_doors);
  } else {
    if ($current_room==$rooms - 1) {
    show_end();
    } else {
      $current_room++;
      $door_choice = -1;
      show_page($rooms,$doors,$current_room,$door_choice,$offset,
      "Right! You are in the next room. Choose another door:",
      @real_doors);
    }
  }
}
#print(join("<br>",@real_doors));
#print(join("<br>",encode_doors(2,3,3,2,3)));


####################
#                  #
# decode_doors     #
# Inputs:          #
#   the offset     #
# Outputs:         #
#   the real doors #
#                  #
####################
sub decode_doors {

  my ($offset) = @_;
  if (defined($offset)) {
    my $fake_doors = param("books");
    my @real_doors = split(/,/,$fake_doors);
    my $i = 0;
    my $rd = 0;
    foreach $rd (@real_doors){
      $rd = $rd - 7 * $i - $offset;
      $i++;
    }
    return @real_doors;
  } else {
      return (); # () is an empty array
                 # I returned an empty array
                 # because $fake_doors is empty
  }

}

#########################
#                       #
# make_real_doors       #
# Inputs:               #
#   the number of rooms #
#   the number of doors #
# Outputs:              #
#   the real doors      #
#                       #
#########################
sub make_real_doors {
  my($rooms,$doors) = @_;
  my @real_doors;
  until ($rooms == -1) {
    $real_doors[$rooms] = int(rand($doors));
    $rooms--;
  }
  return @real_doors;
}
####################
# encode_doors     #
# Inputs:          #
#   the offset and #
#   the real doors #
# Outputs:         #
#   the fake doors #
####################
sub encode_doors {
  my($offset,@real_doors) = @_;
  my $rd = 0;
  my $i = 0;
  my @fake_doors = ();
  foreach $rd (@real_doors) {
    my $fd = $rd + 7 * $i + $offset;
    $fake_doors[$i] = $fd;
    $i++;
  }
  return @fake_doors;  
}
##########################################################
# show_page                                              #
# Inputs:                                                #
#   The number of rooms,                                 #
#   the number of doors,                                 #
#   the current room,                                    #
#   the number of the door the user chose last,          #
#   the offset                                           #
#   a message that tells if the user got the door right, #
#   the real doors                                       #
##########################################################
sub show_page {
  
  my($rooms,$doors,$current_room,$door_choice,$offset,
     $message,@real_doors) = @_;
  start();
  my $user_current_room = $current_room + 1;
  print h1("The Maze"), p("you are in room ".$user_current_room 
  ." of ".$rooms), p($message);

  my $good_door = $real_doors[$current_room];
  my $i = 0;
  print "<table><tr>\n";
  foreach $i (0..$doors - 1) {
  print "<td>\n";
    if ($i==$door_choice and $door_choice!=$good_door) {
      # The door has been chosen and it is the wrong one
      print img {src=>"/static/blocked_door.jpg"}, p($i + 1);
    } else {
      # The door has not been chosen or it is the right one
      print a({-href=>"showmaze.pl?".
      "doors=$doors&".
      "rooms=$rooms&".
      "current_room=$current_room&".
      "door_choice=$i&".
      "users=$offset&".
      "books=".
        join(",",encode_doors($offset,@real_doors))
      }),
      img {src=>"/static/door.jpg"}, p($i + 1);
    }
    print "</td>\n";
  }
  print "</tr></table>\n";
  end();
}
##################################
# show_end                       #
# Inputs:                        #
#   none                         #
# Outputs:                       #
#   a web page with an open door #
##################################
sub show_end {
  start();
  print br, h2("The End");
  print img {src=>"/static/open_door.jpg"},"<br>";
  print a({-href=>"the_maze.php"},"Play agian?");
  print "<br>";
  print a({-href=>"../index.php"},"Quit");
  end();
}
#################################
# start                         #
# Inputs:                       #
#   none                        #
# Outputs:                      #
#   the beginning of a web page #
#################################
sub start {
#  print "Content-type: text/html\n\n";
#  print `/usr/bin/php ../header.php Maze`
#  print header(), start_html("The Maze");
#  print header(), start_html(-title=>"The Maze", -style =>{-src=>["../stylesheet.css"],-media=> 'all'});
}
###########################
# end                     #
# Inputs:                 #
#   none                  #
# Outputs:                #
#   the end of a web page #
###########################
sub end {
  print h6("Made by Johan");
#  print end_html();
#  print `/usr/bin/php ../footer.php`
}
