# Coffee Shop Full Stack

## Project description

This project serves as a Web-App for the new Café at the Udacity campus.
Here everyone can check which drinks are currently on the menu and there is the possibility for managers and baristas to get access to the recipes (managers can edit the menu).
We have three roles: 
1. common visitors without any authentication - those can only see the drinks on the menu
2. baristas (authenticated via Auth0) - they can see rough and detailed recipes for the drinks
3. managers (also authenticated via Auth0) - they can add new drinks, change existing ones and drop drinks from the menu

## Run the project on your local machine

To set everything up you need your Flask-Backend and Angular-Frontend to be running.
How that is done is described in the respective Readmes:

1. [`./backend/`](./backend/README.md)
2. [`./frontend/`](./frontend/README.md)

## Endpoints

### DRINKS

#### GET-Endpoint

The GET drinks endpoint serves to get all drinks without details and is accessible with simple get request without any authentication to: http://localhost:5000/drinks
There are no inputs necessary. It responds with a JSON-object containing a successstatus flag and an array containing all drink objects from the database:

```JSON
{
    "drinks": [
        {
            "id": 2,
            "recipe": [
                {
                    "color": "blue",
                    "parts": 1
                }
            ],
            "title": "Water3"
        }
    ],
    "success": true
}
```

#### POST-Endpoint

The POST drink endpoint serves to create a new drink and is only accessible for manager roles and needs to be accessed with a post request to: http://localhost:5000/drinks 
The header must contain a JWT Bearer token in the "Authorization" field of the header. Also there needs to be a JSON object in the body containing the title of the drink as a string and the recipe as an array of content objects:

```JSON
{
    "title": "Water3",
    "recipe": {
        "name": "Water",
        "color": "blue",
        "parts": 1
    }
}
```

The response for a successful entry will contain a successflag as well as the object of the added drink:

```JSON
{
    "drinks": {
        "id": 2,
        "recipe": [
            {
                "color": "blue",
                "name": "Water",
                "parts": 1
            }
        ],
        "title": "Water3"
    },
    "success": true
}
```

#### PATCH-Endpoint

The PATCH drink endpoint serves to update the name or recipe of a drink and is only accessible for manager roles and needs to be accessed with a patch request to: http://localhost:5000/drinks/<id> where <id> is the id of the drink that shall be updated.
The header must contain a JWT Bearer token in the "Authorization" field of the header. Also there needs to be a JSON object in the body containing the title the recipe of the drink as a string and/or the recipe as an array of content objects:

```JSON
{
    "title": "Water5"
}
```

A successful response will contain a successflag as well as the updated object of the drink in an array:

```JSON
{
    "drinks": [
        {
            "id": 1,
            "recipe": [
                {
                    "color": "blue",
                    "name": "water",
                    "parts": 1
                }
            ],
            "title": "Water5"
        }
    ],
    "success": true
}
```

#### DELETE-Endpoint

The DELETE drink endpoint serves to delete a drink and is only accessible for manager roles and needs to be accessed with a delete request to: http://localhost:5000/drinks/<id> where <id> is the id of the drink that shall be deleted.
The header must contain a JWT Bearer token in the "Authorization" field of the header. Also there needs to be a JSON object in the body containing the title the recipe of the drink as a string and/or the recipe as an array of content objects. A successful request will result in a response cointaining a success-flag as well as the id of the deleted drink:

```JSON
{
    "delete": 1,
    "success": true
}
```



### DRINKS-DETAIL

#### GET-Endpoint

The GET-Endpint for drinks-detail is similar to the get drinks endpoint except for being only accessible for barista and manager roles which needs to be authenticated with a JWT Bearer token in the Authorization header.
It will respond with a JSON object, containing the success flag and the array of all drinks with the detailed recipes:

```JSON
{
    "drinks": [
        {
            "id": 2,
            "recipe": [
                {
                    "color": "blue",
                    "name": "Water",
                    "parts": 1
                }
            ],
            "title": "Water3"
        }
    ],
    "success": true
}
```
