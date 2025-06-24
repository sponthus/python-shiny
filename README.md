# python-shiny

## Description
<table>
      <a href="https://shiny.posit.co/py/">Python for Shiny</a> allows to create reactive apps im python for visualizing data. This repo has been created to learn its basics, using a <a href="https://datavaccin-covid.ameli.fr/explore/dataset/donnees-de-vaccination-par-commune/information/">dataset</a> from Ameli about COVID vaccination through time. 
</table>

## :memo: Status
<p align="center">
      <strong>Functional 🆗 </strong>
      <br><strong>Possible improvements :</strong>
      <br>:star: Better data cleaning
      <br>:star: Better UI for city choice
        <br>:star: Add different graphical representations and data split
</p>

## :blue_book: Project composition
- data.py : From official data, completes a few missing data that can be deduced and exports it as modified-data.csv
- shared.py : Opens modified-data.csv
- app.py : Core app center, linking UI and server
- app_ui.py : Contains the UI components and their parameters
- app_server.py : Contains all the functional rendering, sent to UI

## :cyclone: Clone
Clone the repository and enter it :
```shell
git clone https://github.com/sponthus/python-shiny
cd python-shiny
```

## 	:runner: Run
From the dashboard directory, create a virtual environment and set it up using :
```shell
cd dashboard
python3 -m venv .venv
source .venv/bin/activate
(.venv) ➜ pip install -r requirements.txt
```
The modified data obtained with data.py is already exported in repo.
Then, run the Shiny app in browser with :
```shell
shiny run --reload --launch-browser app.py
```

Be awarwe that this is a proof of concept, and not designed to be a finished product : I only do researches on various subjects !

:hugs: Thanx !
---
Made by sponthus
