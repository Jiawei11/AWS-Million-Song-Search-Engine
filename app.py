#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import psycopg
import pandas as pd

conn = psycopg.connect(
    host="project-postgres.cswxevh2otkt.us-west-2.rds.amazonaws.com", #change to rds
    port='5432',
    dbname="postgres",  #change to the final one
    user="postgres",
    password="Pswd_2022")

# create a cursor
cur = conn.cursor()


# In[ ]:


from flask import redirect, Flask, request, render_template, url_for

app = Flask("MyApp")

# Homepage
@app.route('/')
def home():
    return render_template('home.html')

# Search for song information
@app.route('/getsong', methods=['POST'])
def getsong():
    val = request.form['find'] # Input
    selected = request.form['select'] # Search criteria  (tag,year,title,artist)
    querystr = "SELECT id,title, tag, year,artist,views from music where "+selected
    if selected == 'artist' or selected == 'title':
        querystr += " like '%"+val+"%'"
    else:
        querystr += " = '"+val+"'"
    
    querystr += ' limit 100'
    print("sql:"+querystr)
    cur.execute(querystr)
    querySongs = pd.DataFrame(cur.fetchall(),columns=["id","title","tag","year","artist","views"]).sort_values('views',ascending=False)

    # Search in the dataframe
    #records = df[df[selected].str.contains(val.lower(),na=False)]
    
    return render_template('getsong.html', tables=[querySongs.to_html(classes='data')])

# Top 100 songs page
@app.route('/top100',methods=['GET'])
def top100(): 
    # SQL query to get top 100 songs by views
    query1 = """
            SELECT id,title, tag, year,artist,views,
            DENSE_RANK() OVER ( 
            ORDER BY views DESC) song_rank
            FROM music 
            ORDER BY views DESC
            LIMIT 100;
        """
    # Execute the statement and get the results
    cur.execute(query1)
    
    # Add the information to the dataframe
    top100songs = pd.DataFrame(cur.fetchall(),columns=["id","title","tag","year","artist","views","song_rank"]).sort_values('views',ascending=False)
    
    # Return the webpage
    return render_template('top100.html', tables=[top100songs.to_html(classes='data')])

# Add song page
@app.route('/addnew',methods=['GET','POST'])
def addnew():
    
    # Input the song information
    if request.method == 'POST':
        newtitle = request.form['title']
        newartist = request.form['artist']
        newyear = str(request.form['year'])
        newtag = request.form['selectgenre']
        
        # Add the information to the dataframe
        insert_statement = """INSERT INTO music (title,artist,year,tag) VALUES (%s,%s,%s,%s)"""
        record_to_insert = (newtitle,newartist,newyear,newtag)
        cur.execute(insert_statement,record_to_insert)
        #new_value.to_sql(name='music', con=engine, if_exists='append', index=False)
        
        return redirect(url_for('addsuccess'))
    
    return render_template('addnew.html')

# Add song success page
@app.route('/addsuccess')
def addsuccess():
    return render_template('addsuccess.html')

# Get the artists with most views
@app.route('/topartist')
def topartist():
    # SQL query to get top 20 artist name, sum of views and ranking
    query2 = """
            SELECT artist, Sum(views) AS cumulative_views,
            DENSE_RANK() OVER ( 
            ORDER BY SUM(views) DESC) ranking
            FROM music 
            GROUP BY artist
            ORDER BY ranking 
            LIMIT 20;
        """
    # Execute the statement and get the results
    cur.execute(query2)
    
    # Add the information to the dataframe
    topartist = pd.DataFrame(cur.fetchall(),columns=["artist","cumulative_views",'ranking']).sort_values('ranking',ascending=True)
    
    # Return the webpage
    return render_template('topartist.html',tables=[topartist.to_html(classes='data')])


# In[ ]:


app.run(host='0.0.0.0', port=5003)


# In[ ]:




