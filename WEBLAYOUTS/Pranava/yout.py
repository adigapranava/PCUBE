from flask import Flask , render_template,request, url_for, redirect, session, flash, jsonify

app = Flask(__name__, template_folder="Templates")
app.secret_key = 'random string'
#app.permanent_session_lifetime = timedelta(hours = 5) #save section for x mins/hours

@app.route('/')
@app.route('/home')
def index():
   return render_template('index.htm')


@app.route("/get_name", methods=['GET', 'POST'])
def get_name():
   name = request.form['name']
   print(name)
   return redirect(url_for('index'))

if __name__ == "__main__":
   print("hai")
   app.run(debug = True)