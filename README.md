# MakeITWork Project 1 - De gezondheidszorg
### Student: Elmer van den Dries
<br>

# How to run the "build" folder?
### **ETL**
Run the below commands where \<env> is substituted by your chosen environment name:
```bash
conda create --name <env> --file conda_requirements.txt

conda activate <env>

python build/etl.py
```
### **Regression modeling**
Run the below commands where \<env> is substituted by your chosen environment name:
```bash
conda create --name <env> --file conda_requirements.txt

conda activate <env>

python build/regression.py
```
<br>

# How to run the "run" folder?
### **CLI app**
Run the below commands where \<env> is substituted by your chosen environment name:
```bash
conda create --name <env> --file conda_requirements.txt

conda activate <env>

python run/cli/cli.py
```

### **Flask app**
Run the below commands where \<env> is substituted by your chosen environment name:
```bash
conda create --name <env> --file conda_requirements.txt

conda activate <env>

cd run/flask && flask run
```

