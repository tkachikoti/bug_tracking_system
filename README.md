# Bug Tracking System

This repository contains the second part of a three part assignment of a Computer Science MSc at the University of Essex Online.


## Description

A Bug Tracking System (BTS) is a issue tracking system that is used to manage defects that may arise during the software development life cycle. Using a BTS, software defects are logged and tracked by both the end users and developers of software applications.

This repository contains a minimum viable product of a [Flask](https://github.com/pallets/flask) based BTS. The front end interface was built using [Bootstrap](https://github.com/twbs/bootstrap) and [Jinja](https://github.com/pallets/jinja).

https://github.com/tkachikoti/bug_tracking_system.git


## Installing and running the app

### Codio IDE (Ubuntu 18.04.3 LTS)

1. Clone the repository:

```
$ git clone https://github.com/tkachikoti/bug_tracking_system.git
```

2. Change directory:

```
$ cd bug_tracking_system
```

3. Configure the environment and install dependencies:

```
$ sudo apt-get update
$ sudo apt-get install python3-venv
$ python3 -m venv venv
$ source venv/bin/activate
$ pip install -U flask
$ pip install -U Flask-WTF
$ pip install -U pytest
$ pip install -U numpy
```

4. Run the app:

```
$ python app.py
```

5. On the menu bar, click on the downward pointing chevron to open the preview menu. Please ensure that the 'Box URL' and the 'New Browser Tab' options are selected.

![Codio configuration](https://tkachikoti.com/image/github/bug-tracking-system/codio_config_1.png)

6. Click the 'Box URL' button to open a browser tab running the app.

![Half-Edge Collapse](http://jcae.sourceforge.net/amibe-doc/org/jcae/mesh/amibe/ds/doc-files/AbstractHalfEdge-2.png)

Please refer to Codio's documentation to resolve any issues:
https://docs.codio.com/common/develop/ide/editing/preview.html

### Windows CMD

1. Download and install Python: https://www.python.org/downloads/

2. Clone the repository:

```
$ git clone https://github.com/tkachikoti/bug_tracking_system.git
```

3. Change directory:

```
$ cd bug_tracking_system
```

4. Configure the environment and install dependencies:

```
$ python3 -m venv venv
$ source venv/bin/activate
$ pip install -U flask
$ pip install -U Flask-WTF
$ pip install -U pytest
$ pip install -U numpy
```

5. Run the app:

```
$ python app.py
```

## Testing the app

1. After following the relevant installation process, tests are executed from the root directory by entering:

```
$ pytest
```

## Functionality overview


### 1. Create/Update Ticket

Users can create or update a ticket by interacting with the form and clicking the button labelled 'CREATE/UPDATE TICKET'. The form includes front end validation to ensure all fields contain data.

![Half-Edge Collapse](http://jcae.sourceforge.net/amibe-doc/org/jcae/mesh/amibe/ds/doc-files/AbstractHalfEdge-2.png)

Pseudo-code:

- Check if the form contains a key labelled 'component-name'
- Validate form data
- If form data is valid persist data in storage otherwise return to index page


### 2. View/Delete Ticket

Users can view or delete a ticket by referencing the unique identification number (uid) that is assigned to each ticket upon creation. A prompted appears on screen requesting users to confirm the deletion of a ticket prior to the execution of the command. This safeguards against the accidental deletion of a ticket.

![Half-Edge Collapse](http://jcae.sourceforge.net/amibe-doc/org/jcae/mesh/amibe/ds/doc-files/AbstractHalfEdge-2.png)

Pseudo-code:

- Check if the form contains a key labelled 'uid'
- Retrieve all data about tickets from persistent storage
- Find ticket data with a 'uid' that matches the one received via GET/POST request form
- Return ticket data

### 3. Search Ticket

Users can search for a ticket by filling a form on the search page. The search algorithm uses cosine similarity to find the ticket(s) which closely resemble the string that is received via search form.

![Half-Edge Collapse](http://jcae.sourceforge.net/amibe-doc/org/jcae/mesh/amibe/ds/doc-files/AbstractHalfEdge-2.png)

Pseudo-code:

- Check if the form contains a key labelled 'search_value'
- Retrieve all data about tickets from persistent storage
- Iterate through the list of tickets checking the cosine similarity between the ticket data and the 'search_value'
- If the cosine similarity is greater than zero the ticket data is appended to the 'search_results' list
- 'search_results' list is sorted in descending order (with respects to the similarity score)
- 'search results' are returned

## References


Gunawan, D., Sembiring, C. & Budiman, M. (2017) 'The Implementation of Cosine Similarity to Calculate Text Relevance between Two Documents', Journal of Physics: Conference Series. Medan, Indonesia, 28–30 November. Medan: IOP Publishing Ltd.