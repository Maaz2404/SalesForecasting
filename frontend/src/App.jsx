import { useState } from 'react';
import predict from './routes/routes.js';
import './App.css';

import { Line } from 'react-chartjs-2';
import {
  Chart as ChartJS,
  LineElement,
  CategoryScale,
  LinearScale,
  PointElement,
  Tooltip,
  Legend,
} from 'chart.js';

ChartJS.register(LineElement, CategoryScale, LinearScale, PointElement, Tooltip, Legend);

const PredictButton = ({ store, days, sellPrice, setPredictions }) => {
  return (
    <button
      onClick={async () => {
        const newObject = {
          store_id: store,
          days_to_forecast: parseInt(days),
          sell_price: parseFloat(sellPrice),
        };
        try {
          const response = await predict(newObject);
          console.log(response);
          setPredictions(response.predictions); // 👈 assuming backend returns { predictions: [...] }
        } catch (err) {
          console.error('Prediction failed:', err);
        }
      }}
    >
      Predict
    </button>
  );
};

function App() {
  const stores = [
    'CA_1', 'CA_2', 'CA_3', 'CA_4',
    'TX_1', 'TX_2', 'TX_3',
    'WI_1', 'WI_2', 'WI_3',
  ];
  const [store, setStore] = useState('CA_1');
  const [days, setDays] = useState(0);
  const [sellPrice, setSellPrice] = useState(0.0);
  const [predictions, setPredictions] = useState([]);

  const chartData = {
    labels: predictions.map((_, i) => `Day ${i + 1}`),
    datasets: [
      {
        label: 'Predicted Sales',
        data: predictions,
        borderColor: 'blue',
        backgroundColor: 'rgba(0, 123, 255, 0.2)',
        tension: 0.4,
      },
    ],
  };

  return (
    <div className="container">
      <div className="forecast-box">
        <h1>Sales Forecasting App</h1>

        <label htmlFor="store">Store ID:</label>
        <select onChange={(e) => setStore(e.target.value)} value={store}>
          {stores.map((store, index) => (
            <option key={index} value={store}>
              {store}
            </option>
          ))}
        </select>

        <label>Days to Forecast:</label>
        <input
          type="number"
          value={days}
          onChange={(e) => setDays(e.target.value)}
        />

        <label>Sell Price:</label>
        <input
          type="number"
          value={sellPrice}
          onChange={(e) => setSellPrice(e.target.value)}
        />

        <PredictButton
          store={store}
          days={days}
          sellPrice={sellPrice}
          setPredictions={setPredictions}
        />

        {predictions.length > 0 && (
          <div style={{ marginTop: '2rem' }}>
            <h3>Forecast Chart</h3>
            <Line data={chartData} />
          </div>
        )}
      </div>
    </div>
  );
}

export default App;
