# fall_risk_db

## Accessing built server documentation
* Download this repository to C:/Users/Public/Documents
* Use the following link in any web browser `file:///C:/Users/Public/Documents/fall_risk_db-main/doc/build/html/index.html`

Server Contact: Matt Krol `mrk7339@rit.edu`

## Accessing the current server
* The current server resides at the following address: `fallriskdb-vm.main.ad.rit.edu`
* By design, the server can be accessed from any internet connected device.
* To log in to the server over SSH, use PuTTY or the command line in the following way:
  * use RIT username and password
  * SSH `ssh <RIT username>@fallriskdb-vm.main.ad.rit.edu`
  * PuTTY enter `fallriskdb-vm.main.ad.rit.edu` in the 'hostname' space and click 'open'. 
  * type the password when prompted. Note, the cursor will not move, but the password is still being sent as you type it. If you make a mistake, it's good to hold backspace for a few seconds to make sure you clear the whole password and start over. 
* See the docs for starting and stopping the server. 
  * The files are currently located under `/srv/www/fall_risk_db`
  * You can access them by using `cd`: `cd /srv/www/fall_risk_db`
  * The server is currently being run under docker
