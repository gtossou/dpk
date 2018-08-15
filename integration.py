import pandas as pd

class Integration(object):

    conso_csv_path = "C:/new_projects/dpk_project/df_conso.csv"
    dju_csv_path = "C:/new_projects/dpk_project/df_dju.csv"

    def pivot_conso(self):
        conso = pd.read_csv(self.conso_csv_path)
        #conso.dropna(subset=["conso"])
        print(conso)
        getbat = lambda x: x[-2:]
        keepid = lambda x: x[:-2]
        date_format = lambda x: x[:-3]
        conso["bat"]=conso["id_bat"].apply(getbat)
        conso["id_bat"]=conso["id_bat"].apply(keepid)
        conso.rename(columns={"id_bat": "id_site"}, inplace=True)
        conso=pd.pivot_table(conso, index=["id_site","date"], columns="bat",values= "conso").reset_index()
        conso["date"]=conso["date"].apply(date_format)
        print(conso)
        return conso

    def join(self, conso):
    	self.conso=conso
    	dju = pd.read_csv(self.dju_csv_path)
    	merged = pd.merge(conso, dju, left_on='date', right_on='month', how="left")
    	return merged.drop(columns=["month"])


integ=Integration()
conso_data=integ.pivot_conso()
print(integ.join(conso_data))
