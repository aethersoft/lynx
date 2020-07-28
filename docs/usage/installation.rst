Installation
============

Prerequisites
-------------

1. PostgreSQL (https://www.postgresql.org/)
2. Redis (https://redis.io/)
3. Python 3.6+ (https://www.python.org/)
4. Git
5. Wget / Any other downloader
6. NodeJS (npm)

Setting Up
----------

1. Clone the repository from `https://github.com/aethersoft/lynx.git` and enter to `lynx` directory using following command.

.. code-block:: bash

    git clone https://github.com/aethersoft/lynx.git
    cd lynx

2. create instance configuration file like the example provided below. This should be placed inside a directory named
`instance`.

  - :download:`config.py <../_static/sample_config.py>`

.. code-block:: bash

    mkdir instance
    wget https://www.aethersoft.org/lynx/_downloads/515584c6ce2abf4c67c3631c96897d03/sample_config.py -O config.py

3. Create and activate new python virtual environment for Lynx repository using virtualenv.

.. code-block:: bash

    python3 -m pip install --user virtualenv
    python3 -m venv venv
    source venv/bin/activate

4. Install all required packages using ...

.. code-block:: bash

    pip install -r requirements.txt