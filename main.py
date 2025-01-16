import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd 


class NetflixRecommender:
    def __init__(self, screen):
        self.screen = screen
        self.screen.title("Netflix Recommender")
        self.screen.geometry("400x500")
        self.netflix_red = "#E50914"
        self.netflix_black = "#221f1f"
        self.netflix_grey = "#f5f5f1"
        self.screen.config(bg="#E50914")
        
        self.create_widgets()

    def create_widgets(self):
        style = ttk.Style()
        style.configure("TFrame", background=self.netflix_red)
        style.configure("TFrame", foreground=self.netflix_grey)

        ttk.Label(self.screen, text="Netflix serie/movie: ",
                  font=('Arial', 12), background=self.netflix_red).pack(pady=10)
        
        self.video_entry = ttk.Entry(self.screen, width=50)
        self.video_entry.pack(pady=5)
        
        ttk.Label(self.screen, text="Search by:", 
                 font=('Arial', 12), background=self.netflix_red).pack(pady=10)
        
        self.category_var = tk.StringVar()
        categories = ["Cast", "Director", "Imdb Score", "Production Country", "Genres","Release Date"]
        category_combo = ttk.Combobox(self.screen, textvariable=self.category_var, 
                                    values=categories, state="readonly", width=47)
        category_combo.pack(pady=5)
        category_combo.set("Categories")

        self.category_entry = ttk.Entry(self.screen, width=50)
        self.category_entry.pack(pady=5)
        self.update_category_entry()

        ttk.Button(self.screen, text="See recommendations", 
                  command=self.show_recommendations).pack(pady=20)
        
        self.recommendation_text = tk.Text(self.screen, height=20, width=60)
        self.recommendation_text.pack(pady=5)
    
    def update_category_entry(self):
        if self.category_var.get() == "Categories":
            self.category_entry.config(state="disable")
        else:
            self.category_entry.config(state="normal")
        self.screen.after(1000, self.update_category_entry)

    def show_recommendations(self):
        if self.category_var.get() == "Categories":
            messagebox.showwarning("Warning", "Please, select a category")
            return
            
        self.recommendation_text.delete(1.0, tk.END)
        self.recommendation_text.insert(tk.END, "Netflix recommendations:\n\n")

        data = self.data_Netflix() 
        '''
        for netflix_program in self.present_data(data):
            self.recommendation_text.insert(tk.END, (netflix_program + "\n"))
        '''
        print(data)

    def data_Netflix(self):
        try:
            data_netflix = pd.read_csv("netflixData.csv",sep=",") #data_netflix = dataframe (df)
            netflix_recommendation = pd.DataFrame()
            '''
            self.category_entry = dato
            self.category_var = columna
            '''
            filtered_data = data_netflix[self.category_var.get()].astype("str") == self.category_entry.get()
            # Ver como hacer para entrar int (creo que los recoje como int y por eso no lo identifica en pandas)
            # Diria que hay que saber diferencia entre tipos de category_var

            column_matches = filtered_data.where(filtered_data == True).dropna().index

            column_title = data_netflix.loc[column_matches, "Title"]
            column_search_result = data_netflix.loc[column_matches, self.category_var.get()]

            netflix_recommendation["Title"] = column_title
            netflix_recommendation[self.category_var.get()] = column_search_result
            return filtered_data
            #return netflix_recommendation

        except FileNotFoundError:
            self.recommendation_text.delete(1.0, tk.END)
            self.recommendation_text.insert(tk.END, "Data base not found.")
            return

    def present_data(self, data):
        data_pandas = pd.DataFrame()
                
        data_pandas = data["Title"] +" - "+ data[self.category_var.get()]

        if not data_pandas.empty:
            list_data = data_pandas.sample(n=5).to_numpy().tolist()

            return list_data
        else:
            self.recommendation_text.delete(1.0, tk.END)
            list_data = ["Could not find any result."]
            return list_data


if __name__ == "__main__":
    screen = tk.Tk()
    app = NetflixRecommender(screen)
    screen.mainloop()



