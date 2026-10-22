from tkinter import *
import requests
from tkinter import messagebox

class Main:
    def __init__(self,root):
        self.root =root
        self.root.state("zoomed")
        self.root.title("Products Manager")
        self.root.config(bg ="white")
        self.main_frame()

    def  create_product(self):
        self.create_window = Toplevel(self.frame1,bg="lightblue")
        self.create_window.geometry("500x400")
        self.create_window.title("Create Product")
        label1 = Label(self.create_window, text="Enter Product Name:")
        label1.pack()
        self.input1 = Entry(self.create_window)
        self.input1.pack()
        label2 = Label(self.create_window, text="Enter Product Color:")
        label2.pack()
        self.input2 = Entry(self.create_window)
        self.input2.pack()
        btn6 = Button(self.create_window, text="Create",command=self.create)
        btn6.pack()
          
    def create(self):
        name = self.input1.get()
        color = self.input2.get()
        try:
            products = {
                "name":name,
                "color":color
            }
            response = requests.post("http://127.0.0.1:8000/products",json=products)
            if response.status_code == 200:
                messagebox.showinfo("Sucessfull","Product sucessfully created!!")

            else:
                messagebox.showerror("Error","Product is not created!!!")


        except requests.RequestException as error:
            messagebox.showerror("Error",f"Backend Problem: {str(error)}")
            
    def show_products(self):
        self.products_window = Toplevel(self.frame1,bg="lightblue")
        self.products_window.geometry("500x400")
        self.products_window.title("Products")
        self.pull_products()
    def pull_products(self):
        
        try:
            response = requests.get("http://127.0.0.1:8000/products")
            data = response.json()
            if response.status_code == 200:
                for product in data:
                    label2 = Label(self.products_window, text=f"Id:{product['id']} Name:{product['name']} Color:{product['color']}")
                    label2.pack()
            else:
                messagebox.showerror("Error","Something went wrong!!!")

        except requests.RequestException as error:
            messagebox.showerror("Error",str(error))
    def update_product(self):
        self.update_window = Toplevel(self.frame1)
        self.update_window.title("Update Product")
        self.update_window.geometry("500x400")
        self.update_window.config(bg="lightblue")
        label1 = Label(self.update_window,text="Enter in Number which product you want to edit:")
        label1.pack()
        self.input3 = Entry(self.update_window)
        self.input3.pack()
        btn7 = Button(self.update_window,text="Search",command=self.search_product)
        btn7.pack()
    def main_search(self):       
        self.input4 = Entry(self.update_window)
        self.input4.pack()
        self.input5 = Entry(self.update_window)
        self.input5.pack()
        self.input4.insert(0,self.data["name"])
        self.input5.insert(0,self.data["color"])
        
        btn8 = Button(self.update_window, text="Save", command= self.save)
        btn8.pack()
        
    def save(self):
        name = self.input4.get()
        color = self.input5.get()

        if name == self.data["name"] and color == self.data["color"]:
            messagebox.showerror("Error","Please Make any changes before saving")
            return
        if name =="" or color =="":
            messagebox.showerror("Error","Please Fill the details!!!")
            return

        try:
            products={
                "name":name,
                "color":color
            }
            response = requests.patch(f"http://127.0.0.1:8000/products/{self.product_id}",json=products)
            if response.status_code ==200:
                messagebox.showinfo("Successful","Successfully updated product!!!")
        except requests.RequestException as error:
            messagebox.showerror("Error",f"{str(error)}")
            
        

    def search_product(self):
        input3_val = self.input3.get()
        if input3_val =="":
            messagebox.showerror("Error","Please provide the number!!")
            return
        try:
            self.product_id = self.input3.get()
            response = requests.get(f"http://127.0.0.1:8000/products/{self.product_id}")
            self.data = response.json()
            if response.status_code ==200:
             self.main_search()
            else:
                messagebox.showerror("Error","Could not found product!!!")
            
        except requests.RequestException:
            messagebox.showerror("Error","Failed to search!!")

    def exit(self):
        self.root.destroy()
    def main_frame(self):
        self.frame1 = Frame(self.root)
        self.frame1.pack()
        btn1 = Button(self.frame1,text="Create",command=self.create_product)
        btn1.pack()
        btn2= Button(self.frame1, text="update", command=self.update_product)
        btn2.pack()
        btn3= Button(self.frame1,text="Delete")
        btn3.pack()
        btn4= Button(self.frame1, text="Show Products",command=self.show_products)
        btn4.pack()
        btn5= Button(self.frame1, text="Exit", command=self.exit)
        btn5.pack()

root = Tk()
app = Main(root)
root.mainloop()