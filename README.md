# tk-onboarding-django
======================

### Summary
An implementation of a simple recipe REST API as part of the 
TravelPerk onboarding process.

=================================================================
### Requirements
python>=3.9

docker>=20.10

docker-compose>=2.10

=================================================================
### Run Unit Tests
.. code-block:: bash

    docker-compose run --rm app sh -c "python manage.py test"

=================================================================
### Run Server
.. code-block:: bash

    docker-compose up