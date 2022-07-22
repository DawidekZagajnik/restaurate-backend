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
That belong to user with given ID.

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