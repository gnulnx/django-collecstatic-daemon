django-collectstatic-daemon
===========================

This is a simple daemon that will watch your project directory and collectstatic files whenever there is a change.
This is often times useful when you are working with node/npm project and you need to collectstatic files
after npm build/prod/watch converts the statis resources.


# Install

1)  Install the package

    ```pip install django-collectstatic-daemon```

2) Add 'watcher' to your list of INSTALLED_APPS in settings.py
    

    ```
    INSTALLED_APPS = [
        ...
        ...
        'watcher'
    ]
    ```

# Using

Using the command is as simple as running

    ./manage.py watcher
