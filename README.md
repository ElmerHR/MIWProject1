# MakeITWork Project 1 - De gezondheidszorg
### Student: Elmer van den Dries
<br>

## How to run the build?
### **ETL**
Run the below commands where \<env> is substituted by your chosen environment name:
```bash
conda create --name <env> --file requirements.txt

conda activate <env>

python build/etl.py
```
### **Regression modeling**
Run the below commands where \<env> is substituted by your chosen environment name:
```bash
conda create --name <env> --file requirements.txt

conda activate <env>

python build/regression_train.py
```
