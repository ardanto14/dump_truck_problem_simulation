from flask import Flask, render_template, request
from simulation import simulation
app = Flask(__name__)


@app.route('/')
def result():
   num_event = request.args.get('num_event')

   if num_event is None:
      num_event = 2

   loader_queue_count = request.args.get('loader_queue_count')

   if loader_queue_count is None:
      loader_queue_count = 6

   scaler_queue_count = request.args.get('scaler_queue_count')

   if scaler_queue_count is None:
      scaler_queue_count = 2
   

   num_event = int(num_event)
   loader_queue_count = int(loader_queue_count)
   scaler_queue_count = int(scaler_queue_count)

   simulator = simulation.DumpTruckSimulator(loader_queue_count, scaler_queue_count)

   

   result = simulator.run_simulation(num_event)



   
   return render_template('main.html', results = result, loader1 = result[-1][10] / result[-1][0],
      loader2 = result[-1][11] / result[-1][0],
      scaler = result[-1][12] / result[-1][0])


