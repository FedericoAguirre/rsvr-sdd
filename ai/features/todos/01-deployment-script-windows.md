# Create deployment instructions file for Windows 11 home

I want to create a deployment instructions file to deploy this system in a Windows 11 home
laptop.

The actual deploy does not consider having containers applications.

The deployment instructions file must include:

- Security prerequisites to install the software and support the web application
    usage
- The instructions must consider to deploy the web app to be available to all
    users, if posiible.
- Instructions to install the RDBMS manager
- Instructions to install and support the web app
- Instructions must include how to properly create a .env file
- The instructions must include a detailed process of commands to execute
- The instructions must include how to start the web app if the computer is
    turned off or restarted and make the service up and running again
- Add relevant link for each part of the process
- The deployment configuration must consider local storage for file uploading
- The file must be a markdown one
- The file must be saved in the docs folder with name windows11_deployment.md
- The README.md file must have a link to the docs/windows11_deployment.md file

## Acceptance criteria

- The README.md file has a link to the docs/windows11_deployment.md file.
- The docs/windows11_deployment.md exists.
- The deployment instructions allow to install the web system without using
    containers solution.
- The deployment instructions uses the minimal software to execute the web app.
- The instructions show how to enable port publishing to host the web app.
- The file has relevant links to install software prerequisites and configure
    tricky processes.
