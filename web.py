import test1
from flask import *

app=Flask(__name__)

@app.route('/filter')
def filtering():
    if request.method=="POST":
        keyword=request.form["keyword"]
        rc=int(request.form['retweet_count'])
        rc_opr=request.form['retweet_opr']
        fc=int(request.form['favorite_count'])
        fc_opr=request.form['favorite_opr']
        flc=int(request.form['follower_count'])
        flc_opr=request.form['follower_opr']
        sort=request.form["sort"]
        if sort=="":
            sort=None
        order=int(request.form["order"])
        since=request.form["since"]
        till=request.form["till"]    
        tweets=filterr(retweet_count=rc,retweet_opr=rc_opr,favorite_count=fc,favorite_opr=fc_opr,follower_count=flc,follower_opr=flc_opr,since=since,till=till,keyword=keyword,sort=sort,order=order)
        render_template("filtered.html",tweets=tweets)