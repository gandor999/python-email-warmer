<!-- GETTING STARTED -->
## Getting Started

### Prerequisites
You should have at least `Python 3.7` installed

### Installation

1. Clone the repo
   ```sh
   $ git clone https://github.com/gandor999/python-email-warmer.git
   ```
2. Make a python virtual environment
   ```sh
   $ python -m venv venv
   ```
3. Setup your [python interpeter](https://code.visualstudio.com/docs/python/environments#_manually-specify-an-interpreter) in you IDE or editor

4. Activate `activate.bat`
    ```sh
    $ venv\Scripts\activate.bat
    ```

5. Install dependencies
    ```sh
    $ pip install -r requirements.txt
    ```

6. Make a `emails.json` file and pattern the contents like this, notice that this is an array:
    ```json
    [
        {
            "email": "mockemail_0@gmail.com",
            "password": "<insert app password>"
        },
        {
            "email": "mockemail_1@gmail.com",
            "password": "<insert app password>"
        }
    ]
    ```

7. Setup the [ssl smtp port](https://support.google.com/a/answer/176600?hl=en) in `/.env`
   ```.env
    GOOGLE_SSL_PORT="<insert port>"
   ```

## Usage
### Writing Messages
Refer to `content.html` for what you want the content of the message to be.
```html
<html>
    <body>
        <p>Warmup email from content.html</p>
    </body>
</html>
```

### Sample Run
`$ python main.py`