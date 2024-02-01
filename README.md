# Weather Forecast Web Application

## Description

This web-based weather application allows users to check real-time weather information for their selected cities.

## Technologies Used

- **Python:** Programming language used for backend development.
- **Django Framework:** High-level web framework for building web applications in Python.
- **Version Control System (Git):** Used for tracking changes in the project.
- **HTML, CSS, Bootstrap, Jinja:** Frontend technologies for building a responsive and visually appealing user interface.
- **API for Obtaining Real-time Data:** Utilized to fetch real-time weather information. Data is typically in JSON format.
- **Coroutines for Faster API Response | Asyncio Library:** Used asynchronous programming to speed up API responses.


## Installation

### Prerequisites

- Python 3
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
    cd weatherProject\weatherapp
    ```

    #2. **Open config.py:**
    
    You can try these options below:
    
    
    ***Linux/MacOS:*** 
    ```bash
    nano config.py
    ```

    ***Windows Command Prompt or Powershell:*** 
    ```bash
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

5. **Create a super user:**

    ```bash
    python manage.py createsuperuser
    ```
    ***Warning:*** Make sure that you choose a city on the account tab after running the server if you want to use the app with your superuser account. Otherwise, it will return an error, and this situation is only for superuser.

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


## Contributing
Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are greatly appreciated.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement". Don't forget to give the project a star! Thanks again!

### How to Contribute

We welcome contributions from the community! If you'd like to contribute to the project, follow these steps:

1. **Fork the Project:**

    Click on the "Fork" button on the top right corner of the repository.

2. **Create a Feature Branch:**
   ```bash
   git checkout -b feature/YourAmazingFeature
   ```

3. **Make Changes:**

    Make your changes and improvements to the code.

4. **Commit Your Changes:**
    ```bash
    git commit -m 'Add some AmazingFeature'
    ```

4. **Open a Pull Request:**

Create a new Pull Request from your forked repository to the main project repository. Please provide a detailed description of  your changes.
## License
This project is licensed under the [MIT License](https://opensource.org/licenses/MIT).

