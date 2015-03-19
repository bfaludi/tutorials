# Fejlesztői környezet telepítése

## **Fordító telepítése**:

### **Linux**:  
    	
    $ sudo apt-get install build-essential
    	
### **Fedora**: 
    		
    $ su
    $ yum groupinstall "Development Tools"
    
### **Mac**: Xcode


## Python Dev telepítése:

### **Linux**: 
    	
    $ sudo apt-get install python-dev
    
### **Fedora**: 
    
    $ yum install python-devel

## Setuptools telepítése: ( easy_install )

### **Linux**: 
    
    $ sudo apt-get install python-setuptools
    
### **Fedora**: 
    
    $ yum install python-setuptools


## Pip telepítése:

### **Linux**: 
    
    $ sudo apt-get install python-pip
    
### **Fedora**: 
    
    $ sudo yum install python-pip
    
### **Mac**: 
    
    	brew install pip

----- 
##virtualenv és virtualenv-wrapper telepítése ([autoenv](https://github.com/kennethreitz/autoenv))

### **Linux & Fedora & Mac**:
    
    $ pip install virtualenv & virtualenvwrapper
	$ nano ~/.bachrc
    
      export WORKON_HOME=$HOME/.virtualenvs
      export PROJECT_HOME=$HOME/<ProjectFolder>
      source /usr/local/bin/virtualenvwrapper.sh

#### Használata virtualenv wrapper-rel:
    
##### **virtualenv létrehozása**: 
   
    $ mkvirtualenv <virtualenv name>
       
##### **virtualenv törlése**: 
       		
    $ rmvirtualenv <virtualenv name>
   	
##### **belépés a virtualenvbe**: 
   	
   	$ workon <virtualenv name>
  
##### **kilépés a virtualenvből**:
   
   	$ deactivate

--------

#### Virtualenv wrapper nélkül:

    $ cd <project_folder>
   
##### **virtualenv létrehozása**: 
        		
    $ virtualenv <virtalenv name> (a projekt mappába hozza létre)
   	
##### **virtualenv törlése**: 
   			
   	$ rm <virtualenv name>
   	
##### **belépés a virtualenvbe**: 
   	
   	$ source <virtualenv name>/bin/activate
    
    
##### **kilépés a virtualenvből**: 
    	
    $ deactivate
   
   ------------

## PostgreSQL

### POSTGRESQL telepítése:

#### **Linux**: ([link](https://www.digitalocean.com/community/tutorials/how-to-install-and-use-postgresql-on-ubuntu-14-04))
    
    $ sudo apt-get install postgresql postgresql-contrib 
    	
 
    
#### **Fedora**: ([link](http://www.if-not-true-then-false.com/2012/install-postgresql-on-fedora-centos-red-hat-rhel/))
    	
    $ yum install postgresql94 postgresql94-server postgresql94-contrib 
    
#### **Mac**: ([link](http://www.moncefbelyamani.com/how-to-install-postgresql-on-a-mac-with-homebrew-and-lunchy/))
    		
    $ brew install postgresql 
    		

###  POSTGRESQL felhasználó és db létrehozása

	$ sudo su - postgres
	$ psql -d tempalte1
	
	#template1=# CREATE USER <username> WITH PASSWORD '<mypassword>';
	#template1=# CREATE DATABASE <database name>;
	#template1=# GRANT ALL PRIVILEGES ON DATABASE <database name> TO <username>;
	
	#template1=# \q
	
------

### Teszt projekt előkészítése:

    $ cd <project folder>
    $ mkvirtualenv <virtualenv name>
    $ pip install pyramid

### Projekt létrehozása:

    $ pcreate -s alchemy <project name>

### Követelmények hozzáadása és telepítése:
    	
    $ vi setup.py
    	
    
   **requires listához ezeket kell hozzáadni:** pyramid-sqlalchemy, pyramid-jinja2, psycopg2

	
#### **Telepítés**:
	
    $ python setup.py develop

### Development.ini kiegészítése:

#### **[app:main] alá**:

    sqlalchemy.url = postgresql://<username>:<password>@localhost:5432/<database name>


### init py kiegészítése:

#### **config = Configurator(settings=settings) alá:**
    
    config.include( 'pyramid_jinja2' )
    config.add_jinja2_extension('jinja2.ext.do')









