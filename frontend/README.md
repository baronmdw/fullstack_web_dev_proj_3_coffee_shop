# Coffee Shop Frontend

## Setup to run the Frontend for the project submission

The frontend runs on Node 14.17.0 so please make sure with nvm to install the correct version of node and activate it.
If you're a Windows user, help for that step can be found here https://linuxhint.com/downgrade-node-version-windows/.
Mac Users find help here https://tecadmin.net/install-nvm-macos-with-homebrew/.

run 
```bash
npm install
```
to install all dependencies.

The frontend needs the backend to be up and running so make sure that you followed the [Backend instructions](../backend/README.md) and have a running backend before proceeding further.

After having set up the backend, run
```bash
ionic serve
```
to serve your frontend, the application should open in your browser. If not navigate to http://localhost:8100 to find the app.

In case of errors run
```bash
ionic repair
ionic serve
```