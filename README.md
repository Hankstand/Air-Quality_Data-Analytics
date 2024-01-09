# Air Quality - Proyek Analisis Data 
## File Structures
```
submission
├───dashboard
| ├───merge_data.csv
| └───dashboard.py
| └──Logo.png
├───data
| ├───PRSA_Data_Aotizhongxin_20130301-20170228.csv
| └───PRSA_Data_Changping_20130301-20170228.csv
| └───PRSA_Data_Dingling_20130301-20170228.csv
| └───PRSA_Data_Dongsi_20130301-20170228.csv
| └───PRSA_Data_Guanyuan_20130301-20170228.csv
| └───PRSA_Data_Gucheng_20130301-20170228.csv
| └───PRSA_Data_Huairou_20130301-20170228.csv
| └───PRSA_Data_Nongzhanguan_20130301-20170228.csv
| └───PRSA_Data_Shunyi_20130301-20170228.csv
| └───PRSA_Data_Tiantan_20130301-20170228.csv
| └───PRSA_Data_Wanliu_20130301-20170228.csv
| └───PRSA_Data_Wanshouxigong_20130301-20170228.csv
├───Proyek_analisis_data.ipynb
├───README.md
└───requirements.txt
```
## Setup environment
1. Install Python di [Situs Resmi](https://www.python.org/downloads/) atau [Microsoft Store](https://apps.microsoft.com/detail/9NRWMJP3717K?hl=en-US&gl=US)
2. Install Text Editor [Vscode](https://code.visualstudio.com/download) atau [Microsoft Store](https://apps.microsoft.com/detail/XP9KHM4BK9FZ7Q?hl=en-us&gl=US)
3. Ektensi di Vscode yang di perlukan 
    - [Python](https://marketplace.visualstudio.com/items?itemName-python.python)
    - [Jupyter](https://marketplace.visualstudio.com/items?itemName=ms-tool.jupyter)
4. Install library di dalam terminal atau install di sell kode jupyter notebook :
```python
pip install numpy 
pip install pandas
pip install matplotlib
pip install seaborn
pip install os
pip install streamlit
pip install plotly
```

## Jalankan aplikasi streamlit
```Python
streamlit run Dashboard.py
```