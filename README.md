# DB (German Railways) JSON Station Board

This is a Station Board which works with the data from DB(Deutsche Bahn/ German Railways). The data needs to be delivered in JSON-Format. 
An example for a valid JSON: "https://dbf.finalrewind.org/LL.json?version=3" .

## Docker
The Docker-Image is located here: https://hub.docker.com/r/rsclub22/hafas-db-depature-board
The only Thing that is need to run this container is to expose the port `5000`. An example for running the Container would be: `docker run -p 5000:5000 rsclub22/hafas-db-depature-board`.
### Customization
For Customization (example: HTML): The HTML-Templates are located in the following directory in the container: `/app`
## Original Repository
The Repository on Github is only Mirror. Issues there are fixed. But the real Repository is located under following git-url: https://git.wagnersnetz.de/Rsclub2_2/Hafas-Depature-Board-DB.git