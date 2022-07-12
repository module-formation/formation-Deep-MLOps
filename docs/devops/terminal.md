# Just enough terminal knowledge to shine in society

* [The Missing Semester of Your CS Education](https://missing.csail.mit.edu/)
* [Great Practical Ideas in CS 2017](https://www.cs.cmu.edu/~15131/f17/)
* [Great Practical Ideas in CS 2021](https://www.cs.cmu.edu/~07131/f21/)

## curl

* [How to start using Curl and why: a hands-on introduction](https://www.freecodecamp.org/news/how-to-start-using-curl-and-why-a-hands-on-introduction-ea1c913caaaa/)

## httpie

[httpie](https://httpie.io) est un client en ligne de commande pour tester les API en http et https. Il possède une syntaxe simple et élégante, et se combine très bien avec l'outil suivant pour traiter les données JSON.

Suivant l'adresse sur laquelle on fait la requête, `httpie` détecte automatiquement si la requête demandée sera une requête `POST` ou `GET`.

!!! example "Exemple"

    Une requête `GET` sur mon API perso `fastapi.mathieuklimczak.com/inferences/` se fait alors simplement comme ça.

    ```shell
    https fastapi.mathieuklimczak.com/inferences/

    HTTP/1.1 200 OK
    Content-Length: 516
    Content-Type: application/json
    Date: Thu, 12 May 2022 14:37:47 GMT
    Server: uvicorn

    [
        {
            "confidence": 1.0,
            "id": 1,
            "inference_date": "2022-03-17",
            "inference_time": "12:50:02",
            "num_detections": 0
        },
        {
            "confidence": 1.0,
            "id": 2,
            "inference_date": "2022-03-17",
            "inference_time": "14:35:50",
            "num_detections": 0
        },
        {
            "confidence": 1.0,
            "id": 3,
            "inference_date": "2022-03-17",
            "inference_time": "14:35:50",
            "num_detections": 0
        },
        {
            "confidence": 1.0,
            "id": 4,
            "inference_date": "2022-03-17",
            "inference_time": "14:35:50",
            "num_detections": 0
        },
        {
            "confidence": 1.0,
            "id": 5,
            "inference_date": "2022-03-17",
            "inference_time": "14:35:50",
            "num_detections": 0
        }
    ]
    ```


## jq

[jq](https://stedolan.github.io/jq/) est une outil de parsing des données json dans le terminal. Il est capable de slicer, filtrer et transformer la données structurées de la même façon que `sed`, `awk` ou `grep`.

!!! example "Exemple"

    Pour ne récupérer que les données, sans le header de la requête, on peut alors combiner `httpie` et `jq`.

    ```shell
    ❯ https fastapi.mathieuklimczak.com/inferences/ | jq .

    [
      {
        "inference_date": "2022-03-17",
        "inference_time": "12:50:02",
        "num_detections": 0,
        "confidence": 1,
        "id": 1
      },
      {
        "inference_date": "2022-03-17",
        "inference_time": "14:35:50",
        "num_detections": 0,
        "confidence": 1,
        "id": 2
      },
      {
        "inference_date": "2022-03-17",
        "inference_time": "14:35:50",
        "num_detections": 0,
        "confidence": 1,
        "id": 3
      },
      {
        "inference_date": "2022-03-17",
        "inference_time": "14:35:50",
        "num_detections": 0,
        "confidence": 1,
        "id": 4
      },
      {
        "inference_date": "2022-03-17",
        "inference_time": "14:35:50",
        "num_detections": 0,
        "confidence": 1,
        "id": 5
      }
    ]
    ```

    Pour récupérer le premier élément de la liste, on tape la commande suivante.

    ```shell
    ❯ https fastapi.mathieuklimczak.com/inferences/ | jq ".[0]"

    {
      "inference_date": "2022-03-17",
      "inference_time": "12:50:02",
      "num_detections": 0,
      "confidence": 1,
      "id": 1
    }
    ```

    Pour avoir uniquement la date de l'inférence.

    ```shell
    ❯ https fastapi.mathieuklimczak.com/inferences/ | jq ".[0].inference_date"

    "2022-03-17"
    ```

    ```shell
    ❯ https fastapi.mathieuklimczak.com/inferences/ | jq  '.[] | {id : .id, date : .inference_date}'

    {
      "id": 1,
      "date": "2022-03-17"
    }
    {
      "id": 2,
      "date": "2022-03-17"
    }
    {
      "id": 3,
      "date": "2022-03-17"
    }
    {
      "id": 4,
      "date": "2022-03-17"
    }
    {
      "id": 5,
      "date": "2022-03-17"
    }

    ❯ https fastapi.mathieuklimczak.com/inferences/ | jq  '[.[] | {id : .id, date : .inference_date}]'

    [
      {
        "id": 1,
        "date": "2022-03-17"
      },
      {
        "id": 2,
        "date": "2022-03-17"
      },
      {
        "id": 3,
        "date": "2022-03-17"
      },
      {
        "id": 4,
        "date": "2022-03-17"
      },
      {
        "id": 5,
        "date": "2022-03-17"
      }
    ]
    ```
