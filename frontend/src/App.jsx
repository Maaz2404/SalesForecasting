import { useState,useEffect } from 'react'

import './App.css'

const PredictButton = () => {
  return(
  <button onClick={async () => {
    pass
    
  }}>
    Predict 
  </button>
  )
}


function App() {
  const [store,setStore] = useState("")
  const [days,setDays] = useState(0)
  const [sellPrice,setSellPrice] = useState(0.0)
  const stores = ["CA_1", "CA_2","CA_3","CA_4", "TX_1", "TX_2","TX_3" ,"WI_1", "WI_2","WI_3"]; 
  

  return (
  <> 
    <div>
      <h1>Sales Forecasting App</h1>
    </div>
    <div>  
      <label htmlFor="store">Store ID:
      <select onChange={(e) => setStore(e.target.value)} value={store}>
        {stores.map((store, index) => (
          <option key={index} value={store}>
            {store}
          </option>
        ))}
      </select>
      </label>
      <br />
      <br/>
    <label>
      Days to Forecast:
      <input type='number' value={days} onChange={(e) => setDays(e.target.value)} />
    </label>
    <br /><br />
    <label>
      Sell Price:
      <input type='number' value={sellPrice} onChange={(e) => setSellPrice(e.target.value)} />
    </label>  
    <br /><br />
    <PredictButton/>
    </div>
    </> 
  )
}

export default App
