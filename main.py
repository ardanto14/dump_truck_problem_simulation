from flask import Flask, render_template
import simulation
app = Flask(__name__)


@app.route('/login',methods = ['POST', 'GET'])
def login():
   if request.method == 'POST':
      user = request.form['nm']
      return redirect(url_for('success',name = user))
   else:
      user = request.args.get('nm')
      return redirect(url_for('success',name = user))

@app.route('/')
def result():
   result = simulation.run_simulation()
   return render_template('main.html', results = result, loader1 = result[-1][10] / result[-1][0],
      loader2 = result[-1][11] / result[-1][0],
      scaler = result[-1][12] / result[-1][0])

if __name__ == '__main__':
   app.run()
