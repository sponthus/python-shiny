# python-shiny

## Description
<table>
      <a href="https://shiny.posit.co/py/">Python for Shiny</a> allows to create reactive apps im python for visualizing data. This repo has been created to learn its basics, using a <a href="https://datavaccin-covid.ameli.fr/explore/dataset/donnees-de-vaccination-par-commune/information/">dataset</a> from Ameli about COVID vaccination. 
</table>

## :memo: Status
<p align="center">
  <strong>Ongoing :</strong>
  <br>:star: Complete filtering UI
  <br>:star: Add graphical representations
</p>

## :cyclone: Clone
Clone the repository and enter it :
```shell
git clone https://github.com/sponthus/python-shiny
cd python-shiny
```

## 	:runner: Run
From the dashboard directory, create a virtual environment and set it up using :
```shell
python3 -m venv .venv
source .venv/bin/activate
(.venv) ➜ pip install -r requirements.txt
```
Then, run the Shiny app in browser with :
```shell
shiny run --reload --launch-browser app_dir/app.py
```

Be awarwe that this is a WIP, and not designed to be a finished product : I only do researches on various subjects !

:hugs: Thanx !
---
Made by sponthus
