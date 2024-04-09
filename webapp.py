import streamlit as st
import re
import sqlite3 
import pickle
import bz2
import pandas as pd
st.set_page_config(page_title="Heart Disease Prediction", page_icon="fevicon.png", layout="centered", initial_sidebar_state="auto", menu_items=None)

conn = sqlite3.connect('data.db')
c = conn.cursor()
# DB  Functions
def create_usertable():
    c.execute('CREATE TABLE IF NOT EXISTS userstable(FirstName TEXT,LastName TEXT,Mobile TEXT,City TEXT,Email TEXT,password TEXT,Cpassword TEXT)')
def add_userdata(FirstName,LastName,Mobile,City,Email,password,Cpassword):
    c.execute('INSERT INTO userstable(FirstName,LastName,Mobile,City,Email,password,Cpassword) VALUES (?,?,?,?,?,?,?)',(FirstName,LastName,Mobile,City,Email,password,Cpassword))
    conn.commit()
def login_user(Email,password):
    c.execute('SELECT * FROM userstable WHERE Email =? AND password = ?',(Email,password))
    data = c.fetchall()
    return data
def view_all_users():
	c.execute('SELECT * FROM userstable')
	data = c.fetchall()
	return data
def delete_user(Email):
    c.execute("DELETE FROM userstable WHERE Email="+"'"+Email+"'")
    conn.commit()


menu = ["Home","Login","SignUp"]
choice = st.sidebar.selectbox("Menu",menu)

if choice=="Home":
    st.markdown(
        """
        <h2 style="color:black">Welcome to Heart Disease Prediction</h2>
        <h1>    </h1>
        <p align="justify">
        <b style="color:black">The Heart Disease Prediction System with Python Webapp is a smart tool that uses advanced technology to check your heart health. It uses computer programs and a website to study different signs like cholesterol levels and blood pressure. By doing this, it can guess if you might have heart problems. The website makes it easy for you to put in your health information, and it quickly tells you if there’s a risk. It also gives you suggestions to stay healthy. This helps people and doctors keep an eye on heart health early on, making it easier to stop problems before they get worse. Overall, it helps prevent heart disease and keeps our hearts healthy, which is good for everyone and makes things easier for doctors too.</b>
        </p>
        """
        ,unsafe_allow_html=True)
    
if choice=="Login":
    Email = st.sidebar.text_input("Email")
    Password = st.sidebar.text_input("Password",type="password")
    b1=st.sidebar.checkbox("Login")
    if b1:
        regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        if re.fullmatch(regex, Email):
            create_usertable()
            if Email=='a@a.com' and Password=='123':
                st.success("Logged In as {}".format("Admin"))
                Email=st.text_input("Delete Email")
                if st.button('Delete'):
                    delete_user(Email)
                user_result = view_all_users()
                clean_db = pd.DataFrame(user_result,columns=["FirstName","LastName","Mobile","City","Email","password","Cpassword"])
                st.dataframe(clean_db)
            else:
                result = login_user(Email,Password)
                if result:
                    st.success("Logged In as {}".format(Email))
                    menu2 = ["K-Nearest Neighbors", "SVM",
                             "Decision Tree", "Random Forest",
                             "Naive Bayes","ExtraTreesClassifier","VotingClassifier"]
                    choice2 = st.selectbox("Select ML",menu2)

                    Age=float(st.slider('Age Value', 29, 77))
                    Sex=float(st.slider('Sex 0:Male 1:Female Value', 0, 1))
                    Chest_pain=float(st.slider('Chest Pain Value', 1, 4))
                    BP=float(st.slider('BP Value', 94, 200))
                    Cholesterol=float(st.slider('Cholestrol Value', 126, 564))
                    FBS=float(st.slider('FBS 0:No 1:Yes Value', 0, 1))
                    EKG=float(st.slider('EKG Value', 0, 2))
                    Max_HR=float(st.slider('HR Value', 71, 202))
                    Exercise_angina=float(st.slider('Exercise angina 0:No 1:Yes Value', 0, 1))
                    ST_depression=float(st.slider('ST depression Value', 0.0, 6.2))
                    Slope_ST=float(st.slider('Slope ST Value', 1, 3))
                    vessels_fluro=float(st.slider('No vessels fluro Value', 0, 3))
                    Thallium=float(st.slider('Thallium Value', 3, 7))
                    b2=st.button("Recommand")
                    sfile = bz2.BZ2File('model.pkl', 'r')
                    model=pickle.load(sfile)
                    tdata=[Age, Sex, Chest_pain, BP, Cholesterol, FBS,
                           EKG, Max_HR, Exercise_angina, ST_depression,
                           Slope_ST, vessels_fluro, Thallium]
                        
                    if b2:
                        if choice2=="K-Nearest Neighbors":
                            test_prediction = model[0].predict([tdata])
                            query=test_prediction[0]
                            st.success(query)
                        if choice2=="SVM":
                            test_prediction = model[1].predict([tdata])
                            query=test_prediction[0]
                            st.success(query)                 
                        if choice2=="Decision Tree":
                            test_prediction = model[2].predict([tdata])
                            query=test_prediction[0]
                            st.success(query)
                        if choice2=="Random Forest":
                            test_prediction = model[3].predict([tdata])
                            query=test_prediction[0]
                            st.success(query)
                        if choice2=="Naive Bayes":
                            test_prediction = model[4].predict([tdata])
                            query=test_prediction[0]
                            st.success(query)
                        if choice2=="ExtraTreesClassifier":
                            test_prediction = model[5].predict([tdata])
                            query=test_prediction[0]
                            st.success(query)
                        if choice2=="VotingClassifier":
                            test_prediction = model[6].predict([tdata])
                            query=test_prediction[0]
                            st.success(query)
                            
                else:
                    st.warning("Incorrect Email/Password")
        else:
            st.warning("Not Valid Email")
                
           
if choice=="SignUp":
    Fname = st.text_input("First Name")
    Lname = st.text_input("Last Name")
    Mname = st.text_input("Mobile Number")
    Email = st.text_input("Email")
    City = st.text_input("City")
    Password = st.text_input("Password",type="password")
    CPassword = st.text_input("Confirm Password",type="password")
    b2=st.button("SignUp")
    if b2:
        pattern=re.compile("(0|91)?[7-9][0-9]{9}")
        regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        if Password==CPassword:
            if (pattern.match(Mname)):
                if re.fullmatch(regex, Email):
                    create_usertable()
                    add_userdata(Fname,Lname,Mname,City,Email,Password,CPassword)
                    st.success("SignUp Success")
                    st.info("Go to Logic Section for Login")
                else:
                    st.warning("Not Valid Email")         
            else:
                st.warning("Not Valid Mobile Number")
        else:
            st.warning("Pass Does Not Match")
            
        

    