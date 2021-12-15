# fall_risk_db

## Accessing built server documentation
* Download this repository to C:/Users/Public/Documents
* Use the following link in any web browser `file:///C:/Users/Public/Documents/fall_risk_db-main/doc/build/html/index.html`

Server Contact: Matt Krol `mrk7339@rit.edu`

## Accessing the current server
* The current server resides at the following address: `fallriskdb-vm.main.ad.rit.edu`
* By design, the server can be accessed from any internet connected device.
* For the following instructions, the term `run` is used to refer to typing in a command and hitting enter into the command prompt. For example, to 'run' ssh, type `ssh` into the command prompt and hit enter. The commands are also blocked out `like this`. When told to run a command, type everything `in the block`. 
* To log in to the server over SSH, use PuTTY or the command line in the following way:
  * use RIT username and password
  * SSH `ssh <RIT username>@fallriskdb-vm.main.ad.rit.edu`
  * PuTTY enter `fallriskdb-vm.main.ad.rit.edu` in the 'hostname' space and click 'open'. 
  * type the password when prompted. Note, the cursor will not move, but the password is still being sent as you type it. If you make a mistake, it's good to hold backspace for a few seconds to make sure you clear the whole password and start over. 
* Starting the server. 
  * The files are currently located under `/srv/www/fall_risk_db`
  * You can access them by using `cd`: `cd /srv/www/fall_risk_db`
  * The server is currently being run under docker in tmux. Run `tmux` to start a tmux session which allows you to log off and keep the server running
  * run `docker-compose up` to start the server
  * Log off by typing `Ctrl-b` at the same time, then `d` to 'detach' from tmux and return to a normal command prompt. You can log off with `exit`. 
  * To re-attach to the server, type `tmux attach` after logging back in. 
  * To stop the server, type `Ctrl-c` at the same time. 
  * Note: to run the server, you must be a member of the `docker` group. If you see the issue `ERROR: Couldn't connect to Docker daemon`, you can run the following command to add yourself to the docker group: `sudo usermod -aG docker <username>` log out and log back in for the changes to take effect
  * Note: The docker daemon must also be running. Use `systemctl status docker` to check if docker is `active`. If it is not, use `systemctl start docker` to start the docker daemon.

## Adding Server Users
Any RIT student can login with their RIT username/password. However, students must be explicitely set up on the server in order to be able to run the docker, change code, or even create directories. To do so, run the following commands:
* Gain root: `sudo su`
  * This allows you to do the rest of the commands
* Make a user home directory: `mkhomedir_helper <username>` 
  * This allows the user to login to a private folder where they can create files, change their user settings, etc.
* Add user to the relevant groups:
  * `usermod -aG docker <username>`
  * `usermod -aG fallguys <username>` 
  * `usermod -aG fall_risk_devs <username>`
* By default, developers do not have admin/root access. To grant a user admin access, add them to the 'wheel' group.
  * `usermod -aG wheel <username>`
  * Note: be careful with granting users this access. It should be restricted to only those who absolutely need it. 

## Extras
* More information about docker can be found here: [docker documentation](https://docs.docker.com/)
* More information about tmux can be found here: [tmux documentation](https://linuxize.com/post/getting-started-with-tmux/)
* It would also be helpful to be familiar with how Linux manages file permissions. See the following article for an intro on users and groups: [Linux user management](https://www.redhat.com/sysadmin/linux-user-group-management)
