# Restaurate Flask back-end
This is a backend for RestauRate, which is Flask-React-MySQL-Redis project of app for rating restaurants.

## API docs
### Auth endpoints
#### POST `/login`
Example data:
```json
{
  "username": "user123",
  "password": "pass123"
}
```
Returns token if login action was successful, or 401 error otherwise.

### Restaurant endpoints
#### GET `/restaurant/<id>`
Returns restaurant with given ID, or 404 if it was not found.
Example response:
```json
{
  "owner": "<owners-name>",
  "id": "<given-id>",
  "name": "<name-of-the-restaurant>",
  "description": "<description-of-the-restaurant>",
  "address": "<address-info-of-the-restaurant>",
  "ownerId": "<id-of-restaurants-owner>"
}
```

#### DELETE `/restaurant/<id>`
Deletes restaurant with given ID. Returns 404 if it was not found, or 409 if
the user is trying to delete restaurant that does not belong to them.

#### POST `/restaurant`
Example data:
```json
{
  "name": "<restaurant-name> max 30 characters",
  "address": "<restaurant-address> max 50 characters",
  "description": "<restaurant-description> max 200 characters"
}
```
Returns 422 in case of validation error, 409 if restaurant with given name already
exists, or `{"inserted": 1}` if the action was successful.

#### GET `/restaurants`
Returns array of objects looking like this:
```json
{
  "owner": "<owners-name>",
  "id": "<restaurant-id>",
  "name": "<name-of-the-restaurant>",
  "description": "<description-of-the-restaurant>",
  "address": "<address-info-of-the-restaurant>",
  "ownerId": "<id-of-restaurants-owner>"
}
```
Takes `page`, `pagesize` and `query` parameters. `query` is for matching by 
restaurant's name.

#### GET `/restaurants/user/<id>`
Returns array of restaurant objects:
```json
{
  "owner": "<owners-name>",
  "id": "<restaurant-id>",
  "name": "<name-of-the-restaurant>",
  "description": "<description-of-the-restaurant>",
  "address": "<address-info-of-the-restaurant>",
  "ownerId": "<id-of-restaurants-owner>"
}
```
That belong to user with given ID, and `has_more` flag:
```json
{
  "has_more": false,
  "result": [...]
}
```

### User endpoints
#### GET `/user/<id>`
Returns user with given ID, or 404 if it was not found. Example response:
```json
{
  "username": "<users-username>",
  "id": "<users-id>"
}
```

#### GET `/my-account`
Returns information about currently logged-in user:
```json
{
  "id": 1,
  "passHash": "<password-hash>",
  "review_count": 1,
  "salt": "<salt>",
  "username": "<username>"
}
```

#### DELETE `/user/<id>`
Deletes user with given ID. Returns 404 if user with given ID was not found, or
409 if user is trying to delete account that does not belong to them.

#### POST `/user`
Registers new user. Example data:
```json
{
  "username": "<username>",
  "password": "<password>"
}
```
Throws 422 in case of validation error, or 409 if user with given username 
already exists.

### Review endpoints
#### DELETE `/review/<id>`
Deletes review with current ID. Throws 404 if the review was not found, or
409 if user is trying to delete review that does not belong to them.

#### POST `/review`
Example payload to be posted:
```json
{
  "content": "<review-content-here>",
  "restaurantId": "<id-of-reviewed-restaurant>",
  "rate": "<integer-between-0-and-5>"
}
```
Throws 422 in case of validation error.

#### GET `/reviews/<restaurant-id>`
Returns array of reviews (check below) for restaurant with given ID and `has_more` flag.
```json
{
  "has_more": true,
  "result": [
    {
      "user": "<username>",
      "timestamp": "2022-07-23 15:21",
      "id": "<review-id>",
      "userId": "<id-of-user>",
      "content": "<review-content>",
      "rate": "<integer-between-0-and-5>",
      "restaurantId": "<given-restaurant-id>"
    },
    ...
  ]
}
```
Takes `page` and `pagesize` parameters.

#### GET `/my-reviews`
Returns array of reviews that have been added by current user, and `has_more` flag.
Takes `page` and `pagesize` parameters.
```json
{
  "has_more": false,
  "result": [
    {
      "user": "<username-of-current-user>",
      "timestamp": "2022-08-21 16:11",
      "id": "<review-id>",
      "userId": "<id-of-current-user>",
      "content": "<review-content>",
      "rate": "<integer-between-0-and-5>",
      "restaurantId": "<restaurant-id>"
    },
    ...
  ]
}
```
