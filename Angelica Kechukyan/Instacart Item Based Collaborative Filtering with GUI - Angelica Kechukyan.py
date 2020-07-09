import pandas as pd
#pip install pandas-profiling
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import csv

from scipy.spatial.distance import cosine
from sklearn.metrics.pairwise import cosine_similarity
from scipy import sparse

from tkinter import *
from PIL import ImageTk,Image

orders = pd.read_csv('data/orders.csv')
products = pd.read_csv('data/products.csv')
departments = pd.read_csv('data/departments.csv')
aisles = pd.read_csv('data/aisles.csv')

order_products_train = pd.read_csv("data/order_products__train.csv")
order_products_prior = pd.read_csv("data/order_products__prior.csv")
#order_products_prior2 = pd.read_csv("data/order_products_prior2.csv")
#order_products_train2 = pd.read_csv("data/order_products__train2.csv")

##############################################################################
###Tranform the data####
# Compile data that I want to look at for now
compiled = pd.merge(order_products_train, orders[['order_id', 'user_id']], on='order_id', how='left')
compiled = pd.merge(compiled, products[['product_id', 'product_name', 'aisle_id','department_id']], on='product_id', how='left')
compiled = pd.merge(compiled, aisles[['aisle_id', 'aisle']], on='aisle_id', how='left' )
compiled = pd.merge(compiled, departments[['department_id', 'department']], on='department_id', how='left' )
compiled.dropna(inplace=True)

# Drop NA's from compiled data and remove all other attributes expect User and Product
UserProductName = compiled.drop(compiled[['add_to_cart_order', 'product_id', 'order_id', 'reordered','aisle_id','department_id', 'aisle', 'department']], 1)
UserProdAisleDept = compiled.drop(compiled[['add_to_cart_order','reordered', 'product_id','department_id', 'order_id', 'aisle_id']], 1)
UserAisle = compiled.drop(compiled[['add_to_cart_order','product_name','department','reordered', 'product_id','department_id', 'order_id', 'aisle_id']], 1)
ProductAisle = compiled.drop(compiled[['add_to_cart_order','reordered', 'user_id','department','product_name','department_id', 'order_id', 'aisle_id']], 1)

#UserId | Product_Name | Department
UserProductDept = compiled.drop(compiled[['add_to_cart_order', 'product_id', 'order_id', 'reordered','aisle_id','department_id', 'aisle']], 1)
UserFiltBakery = UserProductDept[UserProductDept['department'] == 'bakery']
##############################################################################
### Build Matrix out of User and Product Name columns ###
UserAisle_matrix = pd.get_dummies(UserAisle.set_index('user_id')['aisle']).max(level=0).sort_index()
UserBakery_matrix = pd.get_dummies(UserFiltBakery.set_index('user_id')['product_name']).max(level=0).sort_index()
##
###List of Column Names


##############################################################################
### What category are currently looking at? (Aisles? Which department?)

###***Make DYNAMIC***###
data_items = UserAisle_matrix


magnitude = np.sqrt(np.square(data_items).sum(axis=1))
data_items = data_items.divide(magnitude, axis='index')
def calculate_similarity(data_items):
    """Calculate the column-wise cosine similarity for a sparse
    matrix. Return a new dataframe matrix with similarities.
    """
    data_sparse = sparse.csr_matrix(data_items)
    similarities = cosine_similarity(data_sparse.transpose())
    sim = pd.DataFrame(data=similarities, index= data_items.columns, columns= data_items.columns)
    return sim
# Build the similarity matrix
data_matrix = calculate_similarity(data_items)
AisleNames = data_matrix.columns

##############################################################################
### What item or aisle are we currently looking ? ###
#print (data_matrix.loc['Wild Blueberry Muffins'].nlargest(10))
#print (data_matrix)
##############################################################################
##############################################################################
#                                 UI Design                                  #
##############################################################################

root = Tk()
root.title('Make Me A Recommendation')
###root.iconbitmap('c:/gui/codemy.ico')

# Creating a Label Widget
myLabel = Label(root, text="Welcome to my recommender system! \n", width=50, font=('Helvetica', 18))
# Image
my_img2 = Image.open("Instacart Cover Picture.png")
my_img2 = my_img2.resize((340,256))
my_img = ImageTk.PhotoImage(my_img2)
my_label = Label(image=my_img)
my_label.pack()

selectcat = Label(root, text="Please select an aisle\n", font=('Helvetica', 14))
# Shoving it onto the screen
myLabel.pack()
selectcat.pack(anchor=W)

### What are my lists?

LEVEL = [
	(AisleNames[0], (data_matrix.iloc[0].nlargest(10))),
    (AisleNames[20], (data_matrix.iloc[20].nlargest(10))),
    (AisleNames[9], (data_matrix.iloc[9].nlargest(10))),
    (AisleNames[120], (data_matrix.iloc[120].nlargest(10))),
    (AisleNames[70], (data_matrix.iloc[70].nlargest(10))),
    (AisleNames[100], (data_matrix.iloc[100].nlargest(10))),

]
###Radio
#########

catlevel = StringVar()
catlevel.set("Level")

for text, level in LEVEL:
	Radiobutton(root, text=text, variable=catlevel, value=level).pack(anchor=W)

def clicked(value):
	myLabel = Label(root, text=value)
	myLabel.pack()
#def clear():
#    label.config(text="")

myButton = Button(root, text="Make Recommendations", command=lambda: clicked(catlevel.get()))
myButton.pack()

#endButton = Button(root, text="Clear", command=clear).grid()
#endButton.pack()

spacer = Label(root, text="\n", font=('Helvetica', 1))
spacer.pack()

button_quit = Button(root, text="Exit Program", command=root.quit)
button_quit.pack()

spacer2 = Label(root, text="\n", font=('Helvetica', 1))
spacer2.pack()



#root.resizable(True, True) 
root.mainloop()
