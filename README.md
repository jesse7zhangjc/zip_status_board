Zip Status Board Challenge
===========================
# Assumptions on Business Level

* Health Status
    * If  a zip has any remaining maintenance task, the zip is not healthy.
    * A zip is unhealthy does not necessarily means that a zip is being blocked to fly. (e.g. the remaining tasks are not blocking flight.)
* "An automated tool SHALL be able to perform all the same tasks as an operator"
    * To easily categorize the tasks, I assume all the problems we might be facing have been pre-defined as a list.

# Prerequisite
* MySQL
* Python 2
* Node.js

# Deployment
## Back End
* Update the MySQL credentials at
```
tornado_server/db_config/mysql_creds.py
```
* ```
cd ./tornado_server
```
* start server
```
python server.py
```

## Front End
* ```
cd ./react_ui
```
* Install all dependencies
    ```
    npm install
    ```
* Start in Development Mode
    ```
    npm start
    ```
* visit
    ```
    http://localhost:3000
    ```

# Directory Structure
## Back End Tornado Server
    tornado_server
    ├── application.py
    ├── db_config
    │   ├── __init__.py
    │   ├── data.xlsx
    │   ├── mysql_creds.py
    │   └── set_up_env.py
    ├── handlers
    │   ├── __init__.py
    │   ├── problems.py
    │   ├── tasks.py
    │   ├── zip.py
    │   └── zips.py
    ├── methods
    │   ├── __init__.py
    │   ├── crud_util.py
    │   └── host_ip.py
    ├── server.py
    └── url.py

## Front End React
    react_ui
    ├── package-lock.json
    ├── package.json
    ├── public
    │   ├── index.html
    │   └── logo
    │       └── logo.png
    └── src
        ├── App.js
        ├── App.test.js
        ├── assets
        │   └── logo
        │       └── logo.png
        ├── components
        │   ├── NewTaskSegment.js
        │   ├── OverviewSegment.js
        │   ├── TabularMenu.js
        │   ├── TaskHistory.js
        │   ├── TaskSegment.js
        │   ├── ZipModal.js
        │   └── ZipStatus.js
        ├── css
        ├── index.js
        ├── serviceWorker.js
        └── services
            └── fetch.js