# Rest API `V0.1.0`

## Event

The `Event` resource represents a scheduling event.

The following available request are

### `GET` _/api/v1/events_

Returns a list of all events.

#### Request

Example Request

```bash
curl -X 'GET' \
'http://localhost:8080/api/v1/events' \
-H 'accept: */*'
```

#### Response

- **200** OK

```json
[
  {
    "title": "Meeting with the team",
    "owner": "JohnDoe",
    "description": "We will discuss the new project",
    "location": "Zoom",
    "options": [
      {
        "date": "2021-01-01",
        "hour": 12,
        "minute": 30
      }
    ],
    "guests": [
      "MarkAnthony"
    ]
  }
]
```

### `POST` _/api/v1/events_

Creates a new event.

#### Request

Example Request

```bash
curl -X 'POST' \
  'http://localhost:8080/api/v1/schedule' \
  -H 'accept: */*' \
  -H 'Content-Type: application/json' \
  -d '{
  "title": "Meeting with the team",
  "owner": "John Doe",
  "description": "We will discuss the new project",
  "location": "Zoom",
  "options": [
    {
      "date": "2021-01-01",
      "hour": 12,
      "minute": 30
    }
  ],
  "guests": []
}'
```

- Request Body

```json
{
  "title": "Meeting with the team",
  "owner": "John Doe",
  "description": "We will discuss the new project",
  "location": "Zoom",
  "options": [
    {
      "date": "2021-01-01",
      "hour": 12,
      "minute": 30
    }
  ],
  "guests": []
}
```

#### Response

- **201** Created

```json
{
  "id": "643d9639f6607431b423ecdd",
  "options": [
    {
      "date": "2021-01-01",
      "hour": 12,
      "minute": 30
    }
  ],
  "attendees": []
}
```

### `GET` _/api/v1/events/{id}_

Returns the event with the given id.

#### Request

Example Request

```bash
curl -X 'GET' \
  'http://localhost:8080/api/v1/events/643d9639f6607431b423ecdd' \
  -H 'accept: */*'
```

#### Response

- **200** OK

```json
{
  "title": "Meeting with the team",
  "owner": "John Doe",
  "description": "We will discuss the new project",
  "location": "Zoom",
  "options": [
    {
      "date": "2021-01-01",
      "hour": 12,
      "minute": 30
    }
  ],
  "guests": []
}
```

- **404** Not Found

```json
{
  "message": "Event not found"
}
```

### `POST` _/api/v1/events/{id}/options_

Votes for an option to the event with the given id.

#### Request

Example Request

```bash
curl -X 'PATCH' \
  'http://localhost:8080/api/v1/events/643d9639f6607431b423ecdd/options' \
  -H 'accept: */*' \
  -H 'Content-Type: application/json' \
  -d '{
  "username": "JohnDoe",
  "date": "2021-01-01",
  "hour": 12,
  "minute": 30
}'
```

- Request Body

```json
{
  "username": "JohnDoe",
  "date": "2021-01-01",
  "hour": 12,
  "minute": 30
}
```

#### Response

- **200** OK

```json
{
  "id": "643d9639f6607431b423ecdd",
  "options": [
    {
      "date": "2021-01-01",
      "hour": 12,
      "minute": 30,
      "votes": [
        "JohnDoe"
      ]
    }
  ]
}
```

- **404** Not Found

```json
{
  "message": "No option with that date."
}
```

- **403** Forbidden

```json
{
  "message": "Voting is no longer available."
}
```

### `POST` _/api/v1/events/{id}/guests_

Adds a guest to the event with the given id.

#### Request

Example Request

```bash
curl -X 'PATCH' \
  'http://localhost:8080/api/v1/events/643d9639f6607431b423ecdd/guests' \
  -H 'accept: */*' \
  -H 'Content-Type: application/json' \
  -d '{
  "usernames": ["MarkAnthony"]
}'
```

- Request Body

```json
{
  "usernames": [
    "MarkAnthony"
  ]
}
```

#### Response

- **200** OK

```json
{
  "id": "643d9639f6607431b423ecdd",
  "owner": "JohnDoe",
  "guests": [
    "MarkAnthony"
  ]
}
```

- **404** Not Found

```json
{
  "message": "Event not found"
}
```

- **409** Conflict

```json
{
  "message": "User already added"
}
```

- **422** Unprocessable Entity

```json
{
  "message": "Invalid username"
}
``` 

### `DELETE` /api/v1/events/{id}/guests/{username}

Removes a guest from the event with the given id.

#### Request

Example Request

```bash
curl -X 'DELETE' \
  'http://localhost:8080/api/v1/events/643d9639f6607431b423ecdd/relationships/guests' \
  -H 'accept: */*' \
  -H 'Content-Type: application/json' \
  -d '{
  "usernames": ["MarkAnthony"]
  }'
```

- Request Body

```json
{
  "usernames": [
    "MarkAnthony"
  ]
}
```

#### Response

- **200** Ok

```json
{
  "id": "643d9639f6607431b423ecdd",
  "guests": []
}
```

- **404** Not Found

```json
{
  "message": "Event not found"
}
```

- **409** Conflict

```json
{
  "message": "User was not added"
}
```

- **422** Unprocessable Entity

```json
{
  "message": "Invalid username"
}
```

### `POST` _/api/v1/auth/users_

Creates a new user.

#### Request

Example Request

```bash
curl -X POST \
     --url 'http://localhost:8080/api/v1/auth/users'\
        --header 'Content-Type': 'application/x-www-form-urlencoded' \
        --data 'username=JohnDoe&password=123456&password2=123456&email=jd@mail.com'
```

Example Form

```
username=JohnDoe
password=123456
password2=123456
email=jd@mail.com
```

#### Response

- **201** Created

```json
{
  "id": "643d9639f6607431b423ecdd",
  "username": "JohnDoe",
  "email": "jd@mail.com"
}
```

- **422** Unprocessable Entity

```json
{
  "message": "Invalid password."
}
```

- **409** Conflict

```json
{
  "message": "Username already exists."
}
```

### `POST` _/api/v1/auth/token_

Returns a new access token.

#### Request

Example Request

```bash
curl -X POST \
  --url 'http://localhost:8080/api/v1/auth/token' \
  --header 'Content-Type': 'application/x-www-form-urlencoded' \
  --data 'username=JohnDoe&password=123456'
```

Example Form

```
username=JohnDoe
password=123456
```

#### Response

- **200** Ok

```json
{
  "accessToken": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c"
}
```

- **401** Unauthorized

```json
{
  "message": "Invalid username or password."
}
```