
# Item Catalog - Udacity
### Full Stack Web Development Nano Degree
_______________________
## About
This project is part of the full stack web development nano degree on Udacity. The project is an application that provides a list of items within a variety of categories as well as provide a user registration and authentication system. Registered users will have the ability to post, edit and delete their own items.

## Prerequisites
* Python 3 [Download it from python.org.](https://www.python.org/downloads/)
* VirtualBox 3 [You can download it from virtualbox.org, here.](https://www.virtualbox.org/wiki/Download_Old_Builds_5_1)
* Vagrant [Download it from vagrantup.com.](https://www.vagrantup.com/downloads.html)

## Installation

#### Download the VM configuration
There are a couple of different ways you can download the VM configuration:

You can download and unzip this file: [FSND-Virtual-Machine.zip](https://s3.amazonaws.com/video.udacity-data.com/topher/2018/April/5acfbfa3_fsnd-virtual-machine/fsnd-virtual-machine.zip) This will give you a directory called **FSND-Virtual-Machine**. It may be located inside your **Downloads** folder.

Note: If you are using Windows OS you will find a Time Out error, to fix it use the new [Vagrant file configuration](https://s3.amazonaws.com/video.udacity-data.com/topher/2019/March/5c7ebe7a_vagrant-configuration-windows/vagrant-configuration-windows.zip) to replace you current Vagrant file.

Alternately, you can use Github to fork and clone the repository [https://github.com/udacity/fullstack-nanodegree-vm](https://github.com/udacity/fullstack-nanodegree-vm).

Either way, you will end up with a new directory containing the VM files. Change to this directory in your terminal with `cd`. Inside, you will find another directory called **vagrant**. Change directory to the **vagrant** directory.

#### Start the virtual machine
From your terminal, inside the **vagrant** subdirectory, run the command `vagrant up`. This will cause Vagrant to download the Linux operating system and install it. This may take quite a while (many minutes) depending on how fast your Internet connection is.

When `vagrant up` is finished running, you will get your shell prompt back. At this point, you can run `vagrant ssh` to log in to your newly installed Linux VM!

Go to the shared folder with your machine using the command:
`cd /vagrant`

#### Creating the database if not exist
I am using sqllite database. To create the database, run the following command:
`python3 models.py`

#### Filling the Data if needed
To fill the database with basic data use the following command:
`python3 database_Datafill.py`

**Exploring the data**
The database includes three tables:
+ The `category` table includes all the categories used in the app.
+ The `category_item` table includes information about each category item.
+ The `user` table includes information about each user.

## Running The APP
1. Make sure to log into the VM as described above.
2. Place your source code in the `vagrant\catalog` directory.
3. Use the command `python application.py`
4. Go to your browser and open the url `http://localhost:8000/` to view the application home page.

## Code Design
The code includes five areas:
1. Database connection setup.
2. Authentication routes area for the user to log in and log out.
3. APIs endPoints area to enable the user to directly access the data.
4. App routes area where all the pages logic are constructed.
5. User functions area.