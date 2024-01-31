## Installation

### Prerequisites

- Python 3.9.6
- Pip
- Git
- [Weather API Key](https://www.weatherapi.com/)
### Setup

1. **Clone the Repository:**

    ```bash
    git clone https://github.com/farukkamcici/WeatherAppDjango.git
    cd WeatherAppDjango/weatherProject
    ```

2. **Create and Activate Virtual Environment:**

    #1.**Install Pipenv:**
   ```bash
   pip install pipenv
   ```

    #2. **Create virtual environment:**
   ```bash
   pipenv shell
   ```
    
    #3. **Install dependencies:**
   ```bash
   pipenv install 
   ```

3. **API Integration:**

    #1.**Get your API key:**
    
    Please visit [Weather API website](https://www.weatherapi.com).

    #1. **Open weatherapp folder:**
    ```bash
    cd weatherapp
    ```

    #2. **Open config.py:**
    
    You can try these options below:
    
    ```bash
    *Linux/MacOS* 

    nano config.py
    ```

    ```bash
    *Windows Command Prompt or Powershell* 
    
    notepad config.py

    ```
    #3. **Provide your key:**
    
    Paste your API key as below and do not forget to save your changes:

    ```bash
    api_key = "YOUR_API_KEY"
    ```

4. **Run Migrations:**

    ```bash
    python manage.py migrate
    ```

5. **Start the Development Server:**

    ```bash
    python manage.py runserver
    ```

6. **Open the Application in Your Browser:**

    [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

## Usage

### Home Page

- Upon accessing the home page, the application fetches real-time weather information for six big cities.
- With the use of coroutines, the data retrieval time has been significantly reduced for an improved user experience.

### Search for Cities

- Users can use the search functionality to get real-time weather information for a specific city.
- The application displays detailed information about the city, including current weather conditions, daily forecasts, and hourly forecasts.

### User Authentication

- The application provides user authentication, allowing users to create accounts, log in, and log out.
- Authenticated users can customize their experience by setting their default city.

### Change Password and City

- Authenticated users have the option to change their password or set a new default city.

